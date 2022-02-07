from __future__ import annotations

import taskprocessor.core as core
import taskprocessor.utils.path_utils as path_utils


class ActionDefinitionProvider(object):

    def __init__(self, action_paths: list[str]):
        # A dictionary with action definition path as key and ActionDefinition as value
        self.__action_definitions: list[core.ActionDefinition] = []
        self.action_paths: list[str] = action_paths
        self.__init_action_definitions()

    def __init_action_definitions(self):
        json_files = []
        # List all json files from given list of paths
        for p in self.action_paths:
            json_files.extend(path_utils.list_files(p, extensions=["json"]))
        # Convert json files to action definition objects
        self.__action_definitions = []
        for j in json_files:
            json_data = path_utils.read_file(j)
            action_def = core.ActionDefinition.from_json(json_data)
            action_def.filepath = j
            self.__action_definitions.append(action_def)

    def get_all(self) -> list[core.ActionDefinition]:
        return self.__action_definitions

    def get_by_name(self, name: str) -> core.ActionDefinition | None:
        return next((a for a in self.__action_definitions if name.lower() in a.name.lower()), None)

    def get_by_engine(self, engine_name: str) -> [core.ActionDefinition]:
        definitions = []
        for a in self.__action_definitions:
            if engine_name.lower() in a.supported_engines:
                definitions.append(a)
        return definitions
