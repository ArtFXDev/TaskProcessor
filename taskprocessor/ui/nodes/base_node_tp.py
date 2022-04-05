from __future__ import annotations

from NodeGraphQt import BaseNode
from taskprocessor.ui import (ActionDataType, ActionDefinition, ActionRuntime)
from taskprocessor.ui.nodes import (NODE_COLORS, NODE_IO_TYPE_COLORS)


def node_prototype_constructor(self):
    super(self.__class__, self).__init__()
    self.action: ActionRuntime | None = None
    # self.initialize_node()
    # self.initialize_inputs()
    # self.initialize_outputs()


class BaseNodeTP(BaseNode):
    __identifier__ = 'taskprocessor'

    NODE_NAME = 'Base Node TP'

    ACTION_NAME = 'base_node_tp'

    def __init__(self):
        super(BaseNodeTP, self).__init__()
        self.action: ActionRuntime | None = None
        self.is_initialized: bool = False

    @staticmethod
    def create_node_class_from_def(action_def: ActionDefinition):
        class_name = action_def.name.title().strip().replace('_', '')
        node_color = NODE_COLORS[action_def.get_main_engine()]
        node_class = type(class_name, (BaseNodeTP,), {
            "__init__": node_prototype_constructor,

            "NODE_NAME": action_def.label,
            "ACTION_NAME": action_def.name
        })
        return node_class

    def initialize(self, action: ActionRuntime):
        self.action = action

        self.set_name(str(action.id).title().replace('_', ' '))

        node_color = NODE_COLORS[action.definition.get_main_engine()]
        self.set_color(node_color[0], node_color[1], node_color[2])

        for (index, i) in enumerate(action.definition.inputs):
            name = str(action.get_input_id(index))
            self.add_input(name=name, color=NODE_IO_TYPE_COLORS[i.type], display_name=False)
            if i.type == ActionDataType.Path:
                self.add_file_input(name, i.label, i.value)
            elif i.type == ActionDataType.String:
                self.add_text_input(name, i.label, i.value)
            elif i.type == ActionDataType.Float:
                self.add_float_input(name, i.label, i.value)
            elif i.type == ActionDataType.Integer:
                self.add_int_input(name, i.label, i.value)
            elif i.type == ActionDataType.Boolean:
                self.add_checkbox(name, i.label, i.value)

        for (index, o) in enumerate(action.definition.outputs):
            name = str(action.get_output_id(index))
            self.add_output(name=name, color=NODE_IO_TYPE_COLORS[o.type], display_name=False)

        self.draw()
        self.is_initialized = True
