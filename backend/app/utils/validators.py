import re
from functools import partial
from typing import Callable


def check_against_pattern(input_: str, *, pattern: str) -> bool:
    return re.match(pattern, input_) is not None


is_uppercase = partial(check_against_pattern, pattern="[A-Z]")
is_digit = partial(check_against_pattern, pattern=r"\d")


def is_strong_password(
        input_: str, *,

        # key: validator, value: min num of characters that must go over validation successfully
        validators_dict: dict[Callable, int],
        min_length: int,
        error_msg_if_fail_over_validators: str) -> dict[str, str | bool]:

    validators_dict = dict(validators_dict)

    if len(input_) < min_length:
        return {
            "valid": False,
            "message": f"length of the password must be at least {min_length} characters"
        }

    for character in input_:
        for validator, count in validators_dict.items():
            if validator(character):
                validators_dict[validator] -= 1  # character went over validation successfully

    # not enough characters went over validation successfully
    if any(num > 0 for num in validators_dict.values()):
        return {
            "valid": False,
            "message": error_msg_if_fail_over_validators
        }

    return {
        "valid": True,
        "message": "valid"
    }


at_least_one_uppercase_and_one_digit_password = partial(
    is_strong_password,
    validators_dict={is_uppercase: 1, is_digit: 1},
    min_length=8,
    error_msg_if_fail_over_validators="password must contain at least one uppercase letter and one digit"
)
