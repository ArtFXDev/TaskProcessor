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

    def delete_action(self, action_id: core.ID) -> bool:
        action = self.get_action_by_id(action_id)

        if action is None:
            return False

        self.actions.remove(action)
        del action
        return True

    def set_input(self, action_id: core.ID, input_id: int | core.ID | str, value) -> bool:
        action = self.get_action_by_id(action_id)
        if action is None:
            return False
        return action.set_input(input_id, value)

    def get_input_value(self, action_id: core.ID, input_id: int | core.ID | str) -> str | int | float | bool | None:
        action = self.get_action_by_id(action_id)
        if action is None:
            return None
        return action.get_input_value(input_id)

    def reset_input(self, action_id: core.ID, input_id: int | core.ID | str) -> bool:
        action = self.get_action_by_id(action_id)
        if action is None:
            return False
        return action.reset_input(input_id)

    def link_input(self, input_action_id: core.ID,
                   input_id: int | core.ID | str,
                   output_action_id: core.ID,
                   output_id: int | core.ID | str) -> bool:
        input_action = self.get_action_by_id(input_action_id)
        if input_action is None:
            return False
        output_action = self.get_action_by_id(output_action_id)

        return input_action.link_input(input_id, output_action, output_id)

    def unlink_input(self, action_id: core.ID, input_id: int | core.ID | str) -> bool:
        action = self.get_action_by_id(action_id)
        if action is None:
            return False

        return action.unlink_input(input_id)

    def get_action_by_id(self, action_id: core.ID) -> core.ActionRuntime:
        return next((a for a in self.actions if action_id == a.id), None)

    def get_actions_by_name(self, name: str) -> [core.ActionRuntime]:
        return [a for a in self.actions if name in a.definition.name]

    def get_actions_by_names(self, names: [str]) -> [core.ActionRuntime]:
        actions = []
        for n in names:
            actions.extend(self.get_actions_by_name(n))
        return actions
