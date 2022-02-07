from __future__ import annotations
from typing import Any

from pathlib import Path

import taskprocessor.core as core
import taskprocessor.utils.path_utils as path_utils


class ActionRuntime(object):
    # A dictionary with the action name as key and a counter as value.
    # The counter is used to generate ID.
    __id_dict: dict[str, int] = {"dummy": 0}

    def __init__(self, definition: core.ActionDefinition = None):
        self.definition: core.ActionDefinition = definition

        self.input_params: dict[str, Any] = {}
        self.output_params: dict[str, Any] = {}

        self.id: str = ""
        if self.definition is not None:
            self.__gen_id()

        self.exec_code: str = ""

        if self.definition is not None:
            self.__init_exec_code()

    # Generates ID for each ActionRuntime instance.
    # ID will have the form <action_name>_<count>
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
        exec_file_path = path_utils.get_absolute_path(self.definition.exec_path, self.definition.filepath)
        self.exec_code = path_utils.read_file(exec_file_path)

        sub_var_names = []
        for i in self.definition.inputs:
            input_id = self.get_input_output_id(i.name)
            sub_var_names.append(input_id)
            self.input_params[input_id] = i.value
        for o in self.definition.outputs:
            output_id = self.get_input_output_id(o.name)
            sub_var_names.append(output_id)
            self.output_params[output_id] = o.value

        self.exec_code = self.exec_code.format(*sub_var_names)

    @staticmethod
    def __is_value_of_type(value: Any, expected_type: core.ActionDataType) -> bool:
        if expected_type == core.ActionDataType.Path:
            if type(value) == Path or type(value) == str:
                return True
        elif expected_type == core.ActionDataType.Boolean:
            if type(value) == bool:
                return True
        elif expected_type == core.ActionDataType.Float:
            if type(value) == float:
                return True
        elif expected_type == core.ActionDataType.Integer:
            if type(value) == int:
                return True
        elif expected_type == core.ActionDataType.Empty:
            return True
        return False

    # Links the value of an input with its input_id
    def set_input(self, input_index: int, value) -> bool:
        if input_index >= len(self.definition.inputs):
            return False
        if not ActionRuntime.__is_value_of_type(value, self.definition.inputs[input_index].type):
            return False

        input_id = self.get_input_output_id(self.definition.inputs[input_index].name)
        self.input_params[input_id] = value
        return True

    # Resets the value of an input to its default value
    def reset_input(self, input_index: int) -> bool:
        if input_index >= len(self.definition.inputs):
            return False

        input_id = self.get_input_output_id(self.definition.inputs[input_index].name)
        self.input_params[input_id] = self.definition.inputs[input_index].value
        return True

    # Links the output_id of the other action to the input_id of this action.
    # This function is used to link output of one node as an input to this node.
    def link_input(self, input_index: int, link_action: ActionRuntime, link_output_index: int) -> bool:
        if input_index >= len(self.definition.inputs):
            print("Input Index out of bounds")
            return False
        if link_output_index >= len(link_action.definition.outputs):
            print("Output Index out of bounds")
            return False
        if self.definition.inputs[input_index].type != link_action.definition.outputs[link_output_index].type:
            print("Input and output type does not match. Input Type: {} Output Type: {}"
                  .format(self.definition.inputs[input_index].type,
                          link_action.definition.outputs[link_output_index].type))
            return False

        input_id = self.get_input_output_id(self.definition.inputs[input_index].name)
        self.input_params[input_id] = link_action.get_input_output_id(
            link_action.definition.outputs[link_output_index].name)
        return True

    # Remove the input link
    def unlink_input(self, input_index: int) -> bool:
        if input_index >= len(self.definition.inputs):
            return False
        self.reset_input(input_index)
        return True

    # Gets the final executable code with properly substituted variables names and values.
    def get_exec_code(self) -> str:
        # print("Code before substitution: \n{}".format(self.exec_code))

        # Replace all inputs in code with linked output variable names
        for (param_id, value) in self.input_params.items():
            self.exec_code = self.exec_code.replace(param_id, str(value))

        # print("Code after substitution: \n{}".format(self.exec_code))
        return self.exec_code
