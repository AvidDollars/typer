import json
from logging import Logger
from uuid import UUID


__all__ = ("CustomJSONEncoder", )


class CustomJSONEncoder(json.JSONEncoder):
    """
    Custom JSON encoder for serialization of JWT tokens.
    To be customized in 'default' method for the types that cannot be serialized to JSON by default.

    Usage:
    ```python

    import jwt
    from functools import partial
    from utils import CustomJSONEncoder
    
    json_encoder = partial(CustomJSONEncoder, logger=logger)
    jwt.encode(payload, secret_key, algorithm, json_encoder=json_encoder)
    ```
    """

    def __init__(self, *args, logger: Logger,  **kwargs):
        self.logger = logger
        super().__init__(*args, **kwargs)

    def default(self, item):
        """ Item will be encoded to a string if default JSON encoder fails. """

        if isinstance(item, UUID):
            return str(item)
        
        try:
            return super().default(item)

        except TypeError as err:
            encoded_to_string = str(item)
            self.logger.warning(
                f"Failed to serialize '{item}' item. \
Argument will be converted to a string. Original error: '{err}'.\
Consider providing custom serialization logic for '{type(item)}' type.")    
            return encoded_to_string
