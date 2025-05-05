from abc import ABC, abstractmethod
from hashlib import sha256
from typing import Protocol

from utils import auto_repr


__all__ = ("AbstractHashingService", "HashingService", "HashAlgorithm", "Sha256Algorithm")


class HashAlgorithm(Protocol):
    """ Hashing algorithms must implement the following methods: """
    def hash(self, input_: str) -> str: ...
    def verify(self, input_: str, hash_: str) -> bool: ...


class Sha256Algorithm:
    def hash(self, input_: str) -> str:
        return sha256(input_.encode("utf-8")).hexdigest()

    def verify(self, input_: str, hash_: str) -> bool:
        hashed_input = self.hash(input_)
        return hashed_input == hash_


@auto_repr(hide="pepper")
class AbstractHashingService(ABC):
    def __init__(self, *, algorithm: HashAlgorithm, pepper=None):
        super().__init__()
        self.algorithm = algorithm
        self.pepper = pepper

    @abstractmethod
    def hash(self, input_: str) -> bool:
        """ to be used in conjunction with 'pepper' (if provided) """

    @abstractmethod
    def verify(self, input_: str, hash_: str) -> bool:
        """ to be used in conjunction with 'pepper' (if provided) """


class HashingService(AbstractHashingService):
    def hash(self, input_: str) -> str:
        input_ = input_ if self.pepper is None else input_ + self.pepper
        return self.algorithm.hash(input_)

    def verify(self, input_: str, hash_: str) -> bool:
        input_ = input_ if self.pepper is None else input_ + self.pepper
        return self.algorithm.verify(input_, hash_)
