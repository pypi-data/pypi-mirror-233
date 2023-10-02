from abc import ABC, abstractmethod


class BaseAction(ABC):
    @classmethod
    @abstractmethod
    def exec(cls):
        pass
