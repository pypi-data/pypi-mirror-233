"""
Create the exception class while executing the `raise` statement, you no longer
need to define an exception class in advance, Convenient and Fast.

    >>> import gqylpy_exception as ge
    >>> raise ge.AnError(...)

    @version: 2.1
    @author: 竹永康 <gqylpy@outlook.com>
    @source: https://github.com/gqylpy/gqylpy-exception

────────────────────────────────────────────────────────────────────────────────
Copyright (c) 2022, 2023 GQYLPY <http://gqylpy.com>. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import logging

from typing import Type, Optional, Union, Tuple, Dict, Callable, Any

ExceptionTypes    = Union[Type[Exception], Tuple[Type[Exception], ...]]
ExceptionLogger   = Union[logging.Logger, 'gqylpy_log']
ExceptionCallback = Callable[[Exception, Callable, '...'], None]


class GqylpyError(Exception):
    """
    All exception classes created with `gqylpy_exception` inherit from it, you
    can use it to handle any exception created by `gqylpy_exception`.
    """
    msg: Any


__history__: Dict[str, Type[GqylpyError]]
# All the exception classes you've ever created are here.
# this dictionary is read-only.


def __getattr__(ename: str) -> Type[GqylpyError]:
    """
    Create an exception type called `ename` and return it.

    The created exception type will be stored to the dictionary `__history__`,
    and when you create an exception type with the same name again, directly get
    the value from this dictionary, rather than being created repeatedly.

    For Python built-in exception types, returned directly, are not repeatedly
    creation, and not stored to dictionary `__history__`.
    """
    return __history__.setdefault(ename, type(ename, (GqylpyError,), {}))


def __getitem__(ename: str) -> Type[GqylpyError]:
    return __getattr__(ename)


def TryExcept(
        etype:      ExceptionTypes,
        *,
        silent_exc: Optional[bool]              = None,
        raw_exc:    Optional[bool]              = None,
        logger:     Optional[ExceptionLogger]   = None,
        ereturn:    Optional[Any]               = None,
        ecallback:  Optional[ExceptionCallback] = None,
        eexit:      Optional[bool]              = None
) -> Callable:
    """
    `TryExcept` is a decorator (is an additional function of `gqylpy_exception`
    ), handles exceptions raised by the function it decorates.

        >>> @TryExcept(ValueError)
        >>> def func():
        >>>    int('a')

    @param etype:      Which exceptions to handle.
    @param silent_exc: If true, exception are processed silently without output,
                       default False.
    @param raw_exc:    If true, output the raw exception information directly,
                       default False. Note priority lower than parameter
                       `silent_exc`.
    @param logger:     By default, exception information is output to terminal
                       by `sys.stderr`. You can specify this parameter, if you
                       want to output exception information using your logger,
                       it will call the logger's `error` method.
    @param ereturn:    If not None, it is returned after an exception is raised.
    @param ecallback:  Receives a callable object and called it after an
                       exception is raised. The callable object receive multiple
                       parameters, raised exception object, function decorated
                       and its arguments.
    @param eexit:      If ture, will exit the program after the exception is
                       triggered, exit code is 4. Default false.
    """


def Retry(
        etype:      Optional[ExceptionTypes]    = None,
        *,
        count:      Optional[int]               = None,
        cycle:      Optional[Union[int, float]] = None,
        silent_exc: Optional[bool]              = None,
        raw_exc:    Optional[bool]              = None,
        logger:     Optional[ExceptionLogger]   = None
) -> Callable:
    """
    `Retry` is a decorator (is an additional function of `gqylpy_exception`),
    retries exceptions raised by the function it decorates. When an exception is
    raised in function decorated, try to re-execute the function decorated.

        >>> @Retry(count=3, cycle=1)
        >>> def func():
        >>>     int('a')

        >>> @TryExcept(ValueError)
        >>> @Retry(count=3, cycle=1)
        >>> def func():
        >>>     int('a')

    @param etype:      Which exceptions to retry, default try all exceptions to
                       `Exception` and its subclasses.
    @param count:      The retry count, 0 means infinite, default infinite.
    @param cycle:      The retry cycle, default 0.
    @param silent_exc: If true, exception are processed silently without output,
                       default False.
    @param raw_exc:    If true, output the raw exception information directly,
                       default False. Note priority lower than parameter
                       `silent_exc`.
    @param logger:     By default, exception information is output to terminal
                       by `sys.stderr`. You can specify this parameter, if you
                       want to output exception information using your logger,
                       it will call the logger's `warning` method.
    """


async def ATryExcept(
        etype:      ExceptionTypes,
        *,
        silent_exc: Optional[bool]              = None,
        raw_exc:    Optional[bool]              = None,
        logger:     Optional[ExceptionLogger]   = None,
        ereturn:    Optional[Any]               = None,
        ecallback:  Optional[ExceptionCallback] = None,
        eexit:      Optional[bool]              = None
) -> Callable:
    """`ATryExcept` is a decorator (is an additional function of
    `gqylpy_exception`), handles exceptions raised by the asynchronous function
    it decorates."""
    return TryExcept(
        etype,
        silent_exc=silent_exc,
        raw_exc   =raw_exc,
        logger    =logger,
        ereturn   =ereturn,
        ecallback =ecallback,
        eexit     =eexit
    )


async def ARetry(
        etype:      Optional[ExceptionTypes]    = None,
        *,
        count:      Optional[int]               = None,
        cycle:      Optional[Union[int, float]] = None,
        silent_exc: Optional[bool]              = None,
        raw_exc:    Optional[bool]              = None,
        logger:     Optional[ExceptionLogger]   = None
) -> Callable:
    """`ARetry` is a decorator (is an additional function of `gqylpy_exception`
    ), retries exceptions raised by the asynchronous function it decorates."""
    return Retry(
        etype,
        count     =count,
        cycle     =cycle,
        silent_exc=silent_exc,
        raw_exc   =raw_exc,
        logger    =logger
    )


async def TryExceptAsync(etype: ExceptionTypes, **kw) -> Callable:
    warnings.warn(
        f'will be deprecated soon, replaced to {ATryExcept}.',
        DeprecationWarning
    )
    return await ATryExcept(etype, **kw)


async def RetryAsync(
        etype: ExceptionTypes              = None,
        *,
        count: Optional[int]               = None,
        cycle: Optional[Union[int, float]] = None,
        **kw
) -> Callable:
    warnings.warn(
        f'will be deprecated soon, replaced to {ARetry}.', DeprecationWarning
    )
    return await ARetry(etype, count=count, cycle=cycle, **kw)


class _xe6_xad_x8c_xe7_x90_xaa_xe6_x80_xa1_xe7_x8e_xb2_xe8_x90_x8d_xe4_xba_x91:
    import sys

    if sys.platform != 'linux' or \
            logging.__file__[:-20] == __file__[:-len(__name__) - 27]:

        gpack = globals()
        gpath = f'{__name__}.g {__name__[7:]}'
        gcode = __import__(gpath, fromlist=...)

        ge = gcode.GqylpyException()

        for gname in gpack:
            if gname[0] != '_':
                try:
                    gfunc = getattr(gcode, gname)
                    assert gfunc.__module__ == gpath
                except (AttributeError, AssertionError):
                    continue
                gfunc.__module__ = __package__
                setattr(ge, gname, gfunc)
            elif not hasattr(ge, gname):
                setattr(ge.__class__, gname, gpack[gname])

        setattr(ge, __package__, ge.__class__)

        ge.__doc__  = __doc__
        ge.__name__ = __package__

        ge.__class__.__qualname__ = __package__
        ge.__class__.__module__   = __package__

        ge.__history__ = gcode.__history__

        ge.ATryExcept = ge.TryExceptAsync = ge.TryExcept
        ge.ARetry     = ge.RetryAsync     = ge.Retry

        sys.modules[__name__] = ge
