import asyncio
from datetime import timedelta, datetime
from functools import partial
from secrets import token_hex
from typing import Callable

from fastapi import APIRouter

__all__ = ("generate_registration_token", "action_on_success", "timedelta_is_less_than", "register_routes")


def generate_random_hex_token(*, n_bytes: int):
    return token_hex(n_bytes)


generate_registration_token = partial(generate_random_hex_token, n_bytes=32)


# TODO: experimental decorator...
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
    compares if current datetime minus provided datetime
    is less than provided timedelta (in hours)
    """
    return (datetime.now() - dt) < timedelta(hours=hours)


def register_routes(router: APIRouter, *routes) -> None:
    """
    helper function for registering routes to APIRouter
    """
    for route in routes:
        router.include_router(route)
