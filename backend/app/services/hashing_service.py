from abc import ABC, abstractmethod


__all__ = ("AbstractHashingService", "HashingService")


class AbstractHashingService(ABC):
    def __init__(self, *, algorithm, pepper):
        self.algorithm = algorithm
        self.pepper = pepper

    @abstractmethod
    def hash(self, input_: str):
        """ to be used with conjunction with 'pepper' """

    @abstractmethod
    def verify(self, input_: str, hash_: str):
        """ to be used with conjunction with 'pepper' """


class HashingService(AbstractHashingService):
    def hash(self, input_: str):
        return self.algorithm.hash(input_ + self.pepper)

    def verify(self, input_: str, hash_: str):
        return self.algorithm.verify(input_ + self.pepper, hash_)
