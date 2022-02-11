from __future__ import annotations

import taskprocessor.core as core
import taskprocessor.utils.json_utils as json_utils
import taskprocessor.utils.path_utils as path_utils


class Task(object):

    def __init__(self, entity: core.Entity = None,
                 actions: list[core.ActionRuntime] = None,
                 label: str = "Sample Task"):
        self.label: str = label
        self.id: str = path_utils.get_name_from_label(label)
        self.entity: core.Entity | None = entity
        self.actions: list[core.ActionRuntime] | None = actions

    def to_json(self, include_action_def: bool = True, include_action_init_code: bool = False) -> str:
        task_dict = {'id': self.id,
                     'label': self.label}
        actions = []
        for a in self.actions:
            actions.append(json_utils.json_to_dict(a.to_json(include_action_def, include_action_init_code)))
        task_dict['actions'] = actions

        return json_utils.dict_to_json(task_dict)

    @staticmethod
    def from_json(json_data: str) -> Task:
        task_dict = json_utils.json_to_dict(json_data)

        task = Task(label=task_dict['label'])

        actions = []
        for a in task_dict['actions']:
            action_json = json_utils.dict_to_json(a)
            action = core.ActionRuntime.from_json(action_json)
            actions.append(action)

        task.actions = actions

        return task

    def __str__(self):
        return self.to_json(include_action_def=False, include_action_init_code=False)

    def get_code(self):
        final_code = ""
        for action in self.actions:
            final_code += "\n" + action.get_exec_code(self.entity)
        return final_code
