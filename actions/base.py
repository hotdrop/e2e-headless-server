from abc import ABC, abstractmethod

class BaseAction(ABC):
    def __init__(self, step: dict):
        self.step = step

    @abstractmethod
    def execute(self, page):
        pass