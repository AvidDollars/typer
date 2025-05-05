import asyncio
from datetime import timedelta, datetime, timezone
from fastapi import APIRouter, Response
from functools import partial, wraps
from secrets import token_hex
from random import choices
from time import sleep
from typing import Callable
from uuid import uuid4


__all__ = (
    "generate_registration_token",
    "action_on_success",
    "timedelta_is_less_than",
    "register_routes",
    "uuid4_bugfix",
    "refresh_token_cookies",
    "random_sleep",
    "datetime_utc_now",
)


def generate_random_hex_token(*, n_bytes: int):
    return token_hex(n_bytes)


generate_registration_token = partial(generate_random_hex_token, n_bytes=32)


# TODO: experimental decorator... dont forget to add "@wraps"
#   tobe used as:
#       @action_on_success(send_email, email="abc.def@ghi.jkl")
#       def some_func(...): ...
#
def action_on_success(action_fn, *action_args, **action_kwargs):
    def after_action(func: Callable):
        async def helper(func, *args, **kwargs):
            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            return func(*args, **kwargs)

        async def wrapper(*args, **kwargs):
            try:
                result = await helper(func, *args, **kwargs)

                if asyncio.iscoroutinefunction(action_fn):
                    await action_fn(*action_args, **action_kwargs)
                else:
                    action_fn(*action_args, **action_kwargs)

                return result

            except Exception as ex:
                raise ex  # will be logged

        return wrapper
    return after_action


def timedelta_is_less_than(dt: datetime, *, hours: int) -> bool:
    """
    Compares if current datetime minus provided datetime is less than provided timedelta (in hours).
    Adds "tzinfo=timezone.utc" to provided input if missing.
    """

    # must both have/miss timezone info, otherwise TypeError is raised
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    return (datetime.now(timezone.utc) - dt) < timedelta(hours=hours)


def register_routes(router: APIRouter, *routes: APIRouter) -> None:
    """
    helper function for registering routes to APIRouter
    """
    for route in routes:
        router.include_router(route)


def uuid4_bugfix():
    """
    temporal bug-fix for "ValueError: badly formed hexadecimal UUID string" issue
    see: https://github.com/tiangolo/sqlmodel/issues/25
    """
    val = uuid4()
    while val.hex[0] == '0':
        val = uuid4()
    return val


"""
Helper method for setting JWT refresh token cookies.

Usage:
    refresh_token_cookies(response: Response, value: str = JWT_refresh_token)
"""
refresh_token_cookies = partial(
    Response.set_cookie,
    key="refresh_token",
    httponly=True,
    path="/", # TODO: "/login;/refresh" ???
    secure=True,
    samesite="none", #TODO: policy to be changes for better security ???
    max_age=60 * 60 * 24
)


# TODO: type hints not working on decorated functions. Improve type definitions.
def random_sleep(callable: Callable) -> Callable:
    """
    Sleeps random amount of time before provided callable is executed (min time: 0ms, max time: 99ms).
    Random element is taken from weighted population -> more likely are picked lower values.

    Where to use it:
        on all places where the code execution is vulnerable to timing attack

    Resources on timing attack:
        https://www.youtube.com/watch?v=XThL0LP3RjY

    Example of usage:

        @random_sleep
        def login_user(user: User) -> token:
            ...
    """

    population = range(100)
    random_delay = partial(choices, population=population, weights=population[::-1])
    random_delay_ms = lambda: random_delay()[0] / 1000 # noqa

    @wraps(callable)
    async def async_inner(*args, **kwargs):
        await asyncio.sleep(random_delay_ms())
        return await callable(*args, **kwargs)
    
    @wraps(callable)
    def inner(*args, **kwargs):
        sleep(random_delay_ms())
        return callable(*args, **kwargs)
        
    return async_inner if asyncio.iscoroutinefunction(callable) else inner


# timezone-aware utc now time
datetime_utc_now = partial(datetime.now, timezone.utc)
