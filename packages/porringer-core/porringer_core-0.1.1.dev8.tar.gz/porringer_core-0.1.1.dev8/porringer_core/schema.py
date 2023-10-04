"""Schema for Porringer"""

from abc import abstractmethod
from typing import NewType, Protocol, TypeVar

from pydantic import BaseModel


class PorringerModel(BaseModel):
    """The base model to use for all CPPython models"""

    model_config = {"populate_by_name": False}


PackageName = NewType("PackageName", str)


class Package(BaseModel):
    """Package definition"""

    name: PackageName
    version: str


class SupportedFeatures(PorringerModel):
    """Plugin feature support"""


class Information(PorringerModel):
    """Plugin information that complements the packaged project metadata"""


class Plugin(Protocol):
    """Porringer plugin"""

    @staticmethod
    @abstractmethod
    def features() -> SupportedFeatures:
        """Broadcasts the shared features of the plugin to Porringer

        Returns:
            The supported features
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def information() -> Information:
        """Retrieves plugin information that complements the packaged project metadata

        Returns:
            The plugin's information
        """
        raise NotImplementedError


PluginT = TypeVar("PluginT", bound=Plugin)
