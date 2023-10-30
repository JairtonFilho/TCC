from abc import ABC, abstractmethod


class Movement(ABC):
    @abstractmethod
    def move_robot(self, **kwargs):
        pass
