"""Typer Helper functions and Decorators."""
import functools
import inspect
import logging
import os
import sys
from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Union

import typer
from typer.models import ParameterInfo

LOGGER = logging.getLogger(__name__)


def get_type_from_default(*annotation_source):  # type: ignore
    """Decorate function, getting type annotations by Dataclass default values.

    Used to tell typer CLI about the Argument types if they are applied via a Dataclass.

    Default values are being searched on the dataclasses provided by *args.
    If they are found, adds type to function annotations so that typer can read them later.

    Parameters
    ----------
    *annotation_source :
        one or many dataclasses on which to search for default values
    """

    def decorator(fun):  # type: ignore
        def wrapper():  # type: ignore
            fun_params = inspect.signature(fun).parameters
            missing_annot = []
            for param_name, param_val in fun_params.items():
                param_default = param_val.default
                if hasattr(param_default, "default") and isinstance(param_default.default, type(...)):
                    # Disable "default" in --help when Arg is required
                    param_default.show_default = False
                if param_name not in fun.__annotations__:
                    missing_annot.append((param_name, param_default))

            for param_name, param_default in missing_annot:
                for source_class in annotation_source:
                    if source_param_name := next(
                        (k for k, v in source_class.__dict__.items() if v == param_default),
                        None,
                    ):
                        if typ := source_class.__annotations__.get(source_param_name):
                            fun.__annotations__[param_name] = typ
                            break
            return fun

        return wrapper()

    return decorator


def typer_retuner(ret: Any) -> Any:
    """Exit Typer command with return code, if parent of calling function is not the typer_unpacker wrapper.

        Will just return ret if ret is either not an integer, or the parent function was another python func.
        Ensures, that we exit the CLI with a return code, only if the function is the CLI base command.

    Parameters
    ----------
    ret : Any
        Value to either return or Exit

    Raises
    -------
    typer.Exit
        when the calling function is the typer Source command. Exit CLI with return code.

    Returns
    -------
    Any
        return of value, if not exiting python completely
    """
    parent_func = sys._getframe(1).f_code.co_name  # pylint: disable=protected-access
    if isinstance(ret, int):
        parent_name = sys._getframe(2).f_code.co_name  # pylint: disable=protected-access
        if parent_name != "typer_unwrapper":
            LOGGER.debug("Exiting Typer Command: %s with code %s", parent_func, ret)
            if ret > 255:
                LOGGER.debug("Capping exit code to 255")
                ret = 255
            raise typer.Exit(code=ret)
    LOGGER.debug("Returning Typer Command: %s", parent_func)
    return ret


def _get_first_env_var(typer_env_spec: Union[List[str], str]) -> str:
    """Get Envvar by Name or first from List of Names.

    Parameters
    ----------
    typer_env_spec : Union[List[str], str]
        List of Env Vars or Env Var

    Returns
    -------
    str
        Env Var Value
    """
    if isinstance(typer_env_spec, str):
        return str(os.getenv(typer_env_spec))

    for ev_name in typer_env_spec:
        env_var = os.getenv(ev_name)
        if env_var:
            return str(env_var)
    return ""


def typer_unpacker(funct: Callable[..., Any]) -> Callable[..., Any]:
    """Decorate function with Typer Arguments or Options to make it callable from python, respecting the default Values.

    Extended Version of: https://github.com/tiangolo/typer/issues/279#issuecomment-893667754

    Parameters
    ----------
    funct : Callable
        Function

    Returns
    -------
    Callable[..., Any]
        the function with resolved default values

    Raises
    ------
    TypeError
        Environment variable Type mismatch
    ValueError
        Missing Required Argument
    """

    @functools.wraps(funct)
    def typer_unwrapper(*args, **kwargs):  # type: ignore
        # Get the default function argument that aren't passed in kwargs via the
        # inspect module: https://stackoverflow.com/a/12627202
        missing_default_values = {
            k: (v.default, v.annotation)
            for k, v in inspect.signature(funct).parameters.items()
            if v.default is not inspect.Parameter.empty and k not in kwargs
        }

        for name, (func_default, target_type) in missing_default_values.items():
            # If the default value is a typer.Option or typer.Argument, we have to
            # pull either the .default attribute and pass it in the function
            # invocation, or call it first.
            if isinstance(func_default, ParameterInfo):
                if env_spec := func_default.envvar:
                    env_var = _get_first_env_var(env_spec)
                    try:
                        if env_res := target_type(env_var) if target_type else env_var:
                            kwargs[name] = env_res
                            continue
                    except TypeError as type_err:
                        raise TypeError(
                            f"Type mismatch in Env Var: '{env_spec}' Expected: '{target_type}' Got: '{type(env_var)}"
                        ) from type_err
                if callable(func_default.default):
                    kwargs[name] = func_default.default()
                else:
                    if func_default.default is Ellipsis:
                        raise ValueError(f"Missing required Argument for: {name}")
                    kwargs[name] = func_default.default

        # Call the wrapped function with the defaults injected if not specified.
        return funct(*args, **kwargs)

    return typer_unwrapper


@dataclass
class LoggingCliArgs:
    """Common Typer Arguments for Logging."""

    verbose: Optional[bool] = typer.Option(False, "--verbose", "-v", help="Verbose Logging with Error stacktraces")


class CommonCLI:
    """Common Typer CLI Class.

    self.typer_returner Can be used to correctly terminate a CLI Program with an exit code.
    self.typer_unpacker Is a decorator that makes functions with typer args callable from python.
    self.arg_annotator Decorated typer function so that the arg types can be inferred from self variables.

    """

    def __init__(self) -> None:
        """Typer CLI Base Class.

        Inherit this Class and add Dataclasses to self.
        Then decorate typer function with @self.arg_annotator.
        All arguments that are written like: function_argument=self.mycustomargs.common_argument
        will get the annotated type of mycustomargs.common_argument, so that typer can do it's magic.
        """
        self.logging = LoggingCliArgs
        self.returner = typer_retuner
        self.unpacker = typer_unpacker

    @property
    def arg_annotator(self) -> Callable[..., Any]:
        """Add type annotations by checking default attribute Types.

        Returns
        -------
        Callback
            Annotator function with CommonCLI Props as arguments
        """
        my_args = self.__dict__
        return get_type_from_default(*list(my_args.values()))
