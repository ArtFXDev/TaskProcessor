from __future__ import annotations


import taskprocessor.core as core
import taskprocessor.utils.path_utils as path_utils


class ActionManager(object):
    # A dictionary with action definition path as key and ActionDefinition as value
    action_definitions = {}

    def __init__(self, action_paths: [str]):
        self.action_paths = action_paths
        self.actions = []
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

    def create_action(self, action_name: str) -> core.ActionRuntime:

        action_path_def_pair = next((a for a in ActionManager.action_definitions.items() if action_name == a[1].name),
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

    def get_actions_by_engine(self, engine: str) -> [core.ActionRuntime]:
        return [a for a in self.actions if engine in a.definition.supported_engines]

    def get_actions_by_entity_extensions(self, extensions: [str]) -> [core.ActionRuntime]:
        # TODO: Filter actions by the entity extensions supported by the engine
        return []
