import operator
from enum import Enum, auto, unique
from typing import Literal


# key = value
class AutoName(Enum):
    @staticmethod
    def _generate_next_value_(name: str, *_) -> str:
        return name


class CompareToStrEnum(str, Enum):
    """
    to be inherited (child class should have numbers as a values for proper comparison)
    -> for comparison enum member against provided string (string should be a valid attribute of an enumeration)

    -> example:
        if:
            UserRole.moderator.value -> 2
            UserRole.admin.value -> 3
        then:
            "moderator" < UserRole.admin -> true
    """

    # @total_ordering can't be used (due to multiple inheritance -> str, Enum)
    def __lt__(self, other):
        return self._compare_by_operator(other, operation="lt")

    def __le__(self, other):
        return self._compare_by_operator(other, operation="le")

    def __gt__(self, other):
        return self._compare_by_operator(other, operation="gt")

    def __ge__(self, other):
        return self._compare_by_operator(other, operation="ge")

    def __eq__(self, other):
        return self._compare_by_operator(other, operation="eq")

    def __ne__(self, other):
        return self._compare_by_operator(other, operation="ne")

    def _compare_by_operator(self, other, *, operation=Literal["lt", "le", "gt", "ge", "eq", "ne"]):
        """ helper function """

        comparison_operation = getattr(operator, operation)

        if isinstance(other, type(self)):
            return comparison_operation(self.value, other.value)

        if isinstance(other, str):
            other = getattr(type(self), other)  # eventual AttributeError will be logged
            return comparison_operation(self.value, other.value)

        return NotImplemented


@unique
class UserRole(CompareToStrEnum):
    user = auto()
    moderator = auto()
    admin = auto()
    master_admin = auto()
