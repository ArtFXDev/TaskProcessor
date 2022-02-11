from __future__ import annotations

import taskprocessor.core as core
import taskprocessor.utils.path_utils as path_utils


class ActionManager(object):

    def __init__(self, def_provider: core.ActionDefinitionProvider):
        self.__def_provider: core.ActionDefinitionProvider = def_provider
        self.actions: [core.ActionRuntime] = [core.ActionRuntime()]

    def create_action(self, action_name: str) -> core.ActionRuntime | None:
        if len(self.actions) == 1 and self.actions[0].definition is None:
            self.actions.clear()

        action_def = self.__def_provider.get_by_name(action_name)
        if action_def is None:
            return None

        action = core.ActionRuntime(action_def)
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
