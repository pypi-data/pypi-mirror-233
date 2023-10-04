"""Shared data between the exposed fixtures"""

from abc import ABCMeta
from importlib.metadata import entry_points
from typing import Generic

import pytest
from porringer_core.plugin_schema.environment import EnvironmentT
from porringer_core.schema import PluginT
from synodic_utilities.utility import canonicalize_type


class BaseTests(Generic[PluginT], metaclass=ABCMeta):
    """Shared testing information for all plugin test classes."""

    @pytest.fixture(name="plugin_type", scope="session")
    def fixture_plugin_type(self) -> type[PluginT]:
        """A required testing hook that allows type generation"""

        raise NotImplementedError("Override this fixture")

    @pytest.fixture(name="todo", scope="session")
    def fixture_todo(self) -> None:
        """A required testing hook that allows type generation"""


class BaseIntegrationTests(Generic[PluginT], metaclass=ABCMeta):
    """Integration testing information for all plugin test classes"""

    def test_entry_point(self, plugin_type: type[PluginT]) -> None:
        """Verify that the plugin was registered

        Args:
            plugin_type: The type to register
        """
        group = canonicalize_type(plugin_type).group

        types = []
        for entry in list(entry_points(group=f"porringer.{group}")):
            types.append(entry.load())

        assert plugin_type in types

    def test_name(self, plugin_type: type[PluginT]) -> None:
        """Verifies the the class name allows name extraction

        Args:
            plugin_type: The type to register
        """
        normalized = canonicalize_type(plugin_type)

        assert normalized.group != ""
        assert normalized.name != ""


class BaseUnitTests(Generic[PluginT], metaclass=ABCMeta):
    """Unit testing information for all plugin test classes"""

    def test_information(self, plugin_type: type[PluginT]) -> None:
        """_summary_

        Args:
            plugin_type: _description_
        """

        assert plugin_type.information()

    def test_plugin_construction(self, plugin: PluginT) -> None:
        """Verifies that the plugin being tested can be constructed

        Args:
            plugin: The data plugin fixture
        """
        assert plugin


class PluginTests(BaseTests[PluginT], Generic[PluginT], metaclass=ABCMeta):
    """Testing information for basic plugin test classes."""

    @staticmethod
    @pytest.fixture(
        name="plugin",
        scope="session",
    )
    def fixture_plugin(
        plugin_type: type[PluginT],
    ) -> PluginT:
        """Overridden plugin generator for creating a populated data plugin type

        Args:
            plugin_type: Plugin type
        Returns:
            A newly constructed provider
        """

        plugin = plugin_type()

        return plugin


class PluginIntegrationTests(BaseIntegrationTests[PluginT], Generic[PluginT], metaclass=ABCMeta):
    """Integration testing information for basic plugin test classes"""


class PluginUnitTests(BaseUnitTests[PluginT], Generic[PluginT], metaclass=ABCMeta):
    """Unit testing information for basic plugin test classes"""


class EnvironmentTests(PluginTests[EnvironmentT], Generic[EnvironmentT], metaclass=ABCMeta):
    """Shared functionality between the different testing categories"""
