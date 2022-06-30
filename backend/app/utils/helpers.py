from secrets import token_hex
from functools import partial


def generate_random_hex_token(*, n_bytes: int):
    return token_hex(n_bytes)


generate_registration_token = partial(generate_random_hex_token, n_bytes=32)
