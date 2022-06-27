from enum import Enum, auto, unique


# key = value
class AutoName(Enum):
    @staticmethod
    def _generate_next_value_(name: str, *_) -> str:
        return name


@unique
class UserRole(str, AutoName):
    user = auto()
    moderator = auto()
    admin = auto()
    master_admin = auto()
