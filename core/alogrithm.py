from abc import ABC, abstractmethod


class Algorithm(ABC):
    @abstractmethod
    def __call__(self, cluster, clock):
        pass
