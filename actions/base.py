from abc import ABC, abstractmethod

class BaseAction(ABC):
    def __init__(site_id: str, self, step: dict):
        self.site_id = site_id
        self.step = step

    @abstractmethod
    def execute(self, page):
        pass
