from abc import ABC, abstractmethod


class Connection(ABC):
    @abstractmethod
    def connect_robot(self):
        pass

    @abstractmethod
    def disconnect_robot(self):
        pass
