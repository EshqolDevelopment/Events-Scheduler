from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import App


class BaseTask(ABC):
    action: str

    @abstractmethod
    def config(self, gui: "App"):
        pass

    @abstractmethod
    def run(self, content: dict[str, str]):
        pass

