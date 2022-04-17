from __future__ import annotations

import os
from pathlib import Path


class ConfigManager(object):

    def __init__(self):
        self._main_dir = Path(__file__).parent.parent

        self._builtin_actions_dir = self._main_dir / "actions"

        self._resources_dir = self._main_dir / "resources"
        self._configs_dir = self._resources_dir / "configs"
        self._engine_config_path = self._configs_dir / "config_engine.json"
        self._example_entities_dir = self._resources_dir / "example_entities"
        self._example_maya_entities_dir = self._resources_dir / "example_maya_entities"
        self._ui_files_dir = self._resources_dir / "qt_ui"

        self._build_dir = self._main_dir / "build"

    def get_builtin_actions_dir(self) -> str:
        return self._builtin_actions_dir.resolve().as_posix()

    def get_engine_config_path(self) -> str:
        return self._engine_config_path.resolve().as_posix()

    def get_example_entities_dir(self) -> str:
        return self._example_entities_dir.resolve().as_posix()

    def get_example_maya_entities_dir(self) -> str:
        return self._example_maya_entities_dir.resolve().as_posix()

    def get_qt_ui_file_path(self, ui_name: str) -> str | None:
        if not ui_name.endswith(".ui"):
            ui_name += ".ui"
        return next((f.resolve().as_posix() for f in self._ui_files_dir.rglob("*.ui") if f.name == ui_name), None)

    def get_build_dir(self) -> str:
        return self._build_dir.resolve().as_posix()
