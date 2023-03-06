from abc import ABC, abstractmethod


class BaseDemo(ABC):
    """
    Base class for all demos. All demo classes must inherit from this class and
    implement the run() method.
    """

    def __init__(self, api_key: str, name: str) -> None:
        self.api_key = api_key
        self.name = name


    @abstractmethod
    def run(self) -> None:
        pass


    def __str__(self) -> str:
        return self.name


    def __repr__(self) -> str:
        return self.name 