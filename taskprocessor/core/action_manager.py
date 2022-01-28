from __future__ import annotations

import taskprocessor.core as core
import taskprocessor.utils.path_utils as path_utils


class ActionManager(object):
    # A dictionary with action definition path as key and ActionDefinition as value
    action_definitions: dict[str, core.ActionDefinition] = {"dummy/path": core.ActionDefinition()}
    __filtered_actions: dict[str, core.ActionDefinition] = {"dummy/path": core.ActionDefinition()}

    def __init__(self, action_paths: list[str]):
        self.action_paths: list[str] = action_paths
        self.actions: [core.ActionRuntime] = [core.ActionRuntime()]
        self.__init_action_definitions()

    def __init_action_definitions(self):
        json_files = []
        # List all json files from given list of paths
        for p in self.action_paths:
            json_files.extend(path_utils.list_files(p, extensions=["json"]))
        # Convert json files to action definition objects
        ActionManager.action_definitions = {}
        for j in json_files:
            json_data = path_utils.read_file(j)
            action_def = core.ActionDefinition.from_json(json_data)
            ActionManager.action_definitions[j] = action_def

        ActionManager.__filtered_actions = ActionManager.action_definitions

    def set_current_engine(self, engine_name):
        ActionManager.__filtered_actions = {}
        for (path, action_def) in ActionManager.action_definitions.items():
            if engine_name.lower() in action_def.supported_engines:
                ActionManager.__filtered_actions[path] = action_def

    def get_action_definition_by_name(self, name: str) -> core.ActionDefinition:
        return next((ad for (p, ad) in ActionManager.action_definitions.items() if name.lower() in ad.label.lower()),
                    None)

    def get_all_action_definitions(self) -> [core.ActionDefinition]:
        definitions = []
        for (path, action_def) in ActionManager.action_definitions.items():
            definitions.append(action_def)
        return definitions

    def get_action_definitions_by_engine(self, engine_name: str) -> [core.ActionDefinition]:
        definitions = []
        for (path, action_def) in ActionManager.action_definitions.items():
            if engine_name.lower() in action_def.supported_engines:
                definitions.append(action_def)
        return definitions

    def create_action(self, action_name: str) -> core.ActionRuntime | None:
        if len(self.actions) == 1 and self.actions[0].definition is None:
            self.actions.clear()

        action_path_def_pair = next(
            ((p, a) for (p, a) in ActionManager.__filtered_actions.items() if action_name == a.name),
            None)

        if action_path_def_pair is None:
            return None

        action = core.ActionRuntime(action_path_def_pair[0], action_path_def_pair[1])
        self.actions.append(action)

        return action

    def delete_action(self, action_id: str) -> bool:
        action = self.get_action_by_id(action_id)

        if action is None:
            return False

        self.actions.remove(action)
        del action
        return True

    def set_input(self, action_id: str, input_index: int, value) -> bool:
        action = self.get_action_by_id(action_id)
        if action is None:
            return False
        return action.set_input(input_index, value)

    def reset_input(self, action_id: str, input_index: int) -> bool:
        action = self.get_action_by_id(action_id)
        if action is None:
            return False
        return action.reset_input(input_index)

    def link_input(self, current_action_id: str,
                   current_input_index: int,
                   source_action_id: str,
                   source_output_index: int) -> bool:
        curr_action = self.get_action_by_id(current_action_id)
        if curr_action is None:
            return False
        src_action = self.get_action_by_id(source_action_id)

        return curr_action.link_input(current_input_index, src_action, source_output_index)

    def unlink_input(self, action_id: str, input_index: int) -> bool:
        action = self.get_action_by_id(action_id)
        if action is None:
            return False

        return action.unlink_input(input_index)

    def get_action_by_id(self, action_id: str) -> core.ActionRuntime:
        return next((a for a in self.actions if action_id == a.id), None)

    def get_actions_by_name(self, name: str) -> [core.ActionRuntime]:
        return [a for a in self.actions if name in a.definition.name]

    def get_actions_by_names(self, names: [str]) -> [core.ActionRuntime]:
        actions = []
        for n in names:
            actions.extend(self.get_actions_by_name(n))
        return actions
