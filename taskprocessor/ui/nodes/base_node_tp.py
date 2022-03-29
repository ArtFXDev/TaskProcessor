from __future__ import annotations

import taskprocessor.ui.nodes as nodes
from taskprocessor.core import ActionDefinition, ActionRuntime


def node_prototype_constructor(self):
    super(self.__class__, self).__init__()
    self.action_runtime: ActionRuntime | None = None
    self.initialize_node()
    self.initialize_inputs()
    self.initialize_outputs()


class BaseNodeTP(nodes.BaseNode):
    __identifier__ = 'taskprocessor'

    NODE_NAME = 'Base Node TaskProcessor'

    def __init__(self):
        super(BaseNodeTP, self).__init__()
        self.action_runtime: ActionRuntime | None = None
        self.add_input()

    @staticmethod
    def create_node_class_from_def(action_def: ActionDefinition):
        node_name = action_def.name.title().replace('_', '')
        node_color = nodes.NODE_COLORS[action_def.get_main_engine()]
        node_class = type(node_name, (BaseNodeTP,), {
            "__init__": node_prototype_constructor,

            "NODE_NAME": action_def.label,

            "initialize_node": lambda self: self.set_color(node_color[0], node_color[1], node_color[2]),
            "initialize_inputs": lambda self: [
                self.add_input(name=i.label, color=nodes.NODE_IO_TYPE_COLORS[i.type], data_type=i.type.name) for i in
                action_def.inputs],
            "initialize_outputs": lambda self: [
                self.add_output(name=o.label, color=nodes.NODE_IO_TYPE_COLORS[o.type], data_type=o.type.name) for o in
                action_def.outputs]
        })
        return node_class
