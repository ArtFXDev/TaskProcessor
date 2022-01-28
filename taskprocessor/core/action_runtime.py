from __future__ import annotations
from typing import Any
import six

if six.PY2:
    from pathlib2 import Path
else:
    from pathlib import Path

import taskprocessor.core as core
import taskprocessor.utils.path_utils as path_utils


class ActionRuntime(object):
    # A dictionary with the action name as key and a counter as value.
    # The counter is used to generate ID.
    __id_dict: dict[str, int] = {"dummy": 0}

    def __init__(self, definition_path: str = "dummy/path", definition: core.ActionDefinition = None):
        self.definition_path: str = definition_path
        self.definition: core.ActionDefinition = definition

        self.id: str = ""
        if self.definition_path != "dummy/path" and self.definition is not None:
            self.__gen_id()

        self.linked_io: dict[str, Any] = {}
        self.exec_code: str = ""

        if self.definition_path != "dummy/path" and self.definition is not None:
            self.__init_exec_code()

    # Generates ID for each ActionRuntime instance.
    # ID will be have the form <action_name>_<count>
    def __gen_id(self):
        if self.definition.name in ActionRuntime.__id_dict:
            count = ActionRuntime.__id_dict[self.definition.name]
            count += 1
            self.id = self.definition.name + "_" + str(count)
            ActionRuntime.__id_dict[self.definition.name] = count
        else:
            self.id = self.definition.name
            ActionRuntime.__id_dict[self.definition.name] = 0

    def get_input_output_id(self, input_output_name) -> str:
        return self.id + "_" + input_output_name

    # Initializes executable code by substituting variable names.
    # Variable names will have the form <action_runtime_id>_<input/output_name>
    def __init_exec_code(self):
        exec_file_path = path_utils.get_absolute_path(self.definition.exec_path, self.definition_path)
        self.exec_code = path_utils.read_file(exec_file_path)

        sub_var_names = []
        for i in self.definition.inputs:
            sub_var_names.append(self.get_input_output_id(i.name))
        for o in self.definition.outputs:
            sub_var_names.append(self.get_input_output_id(o.name))

        self.exec_code = self.exec_code.format(*sub_var_names)

    # Links the value of an input with its input_id
    def set_input(self, input_index: int, value) -> bool:
        input_id = self.get_input_output_id(self.definition.inputs[input_index].name)
        self.linked_io[input_id] = value
        return True

    # Resets the value of an input to its default value
    def reset_input(self, input_index: int) -> bool:
        input_id = self.get_input_output_id(self.definition.inputs[input_index].name)
        self.linked_io[input_id] = self.definition.inputs[input_index].value
        return True

    # Links the output_id of the other action to the input_id of this action.
    # This function is used to link output of one node as an input to this node.
    def link_input(self, input_index: int, link_action: ActionRuntime, link_output_index: int) -> bool:
        input_id = self.get_input_output_id(self.definition.inputs[input_index].name)
        # TODO: Check if the given input exists in the action
        # TODO: Check if the link to be made have same action data type
        self.linked_io[input_id] = link_action.get_input_output_id(link_action.definition.outputs[link_output_index].name)
        return True

    # Remove the input link
    def unlink_input(self, input_index: int) -> bool:
        input_id = self.get_input_output_id(self.definition.inputs[input_index].name)
        # TODO: Check if the given input exists in the action
        self.linked_io.pop(input_id)
        return True

    # Gets the final executable code with properly substituted variables names and values.
    def get_exec_code(self) -> str:
        # print("Code before substitution: \n{}".format(self.exec_code))

        # Replace all inputs in code with linked output variable names
        for input_id in self.linked_io.keys():
            self.exec_code = self.exec_code.replace(input_id, str(self.linked_io[input_id]))

        # print("Code after substitution: \n{}".format(self.exec_code))
        return self.exec_code
