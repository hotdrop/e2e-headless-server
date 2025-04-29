from abc import ABC, abstractmethod

class BaseAction(ABC):
    def __init__(self, site_id: str, step: dict): 
        self.site_id = site_id # site_id をインスタンス変数として保持
        self.step = step

    @abstractmethod
    def execute(self, page):
        pass
