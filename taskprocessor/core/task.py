from __future__ import annotations

import taskprocessor.core as core


class Task(object):

    def __init__(self, entity: core.Entity, actions: list[core.ActionRuntime]):
        self.id: str = ""
        self.name: str = ""
        self.label: str = ""
        self.entity: core.Entity = entity
        self.actions: list[core.ActionRuntime] = actions

    def get_code(self):
        final_code = ""
        for action in self.actions:
            final_code += "\n" + action.get_exec_code(self.entity)
        return final_code
