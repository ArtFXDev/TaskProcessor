from __future__ import annotations
from typing import Any

import taskprocessor.core as core
import taskprocessor.utils.path_utils as path_utils


class ActionRuntime(object):

    def __init__(self, definition: core.ActionDefinition = None):
        self.definition: core.ActionDefinition = definition
        # input_params is a dictionary with id of input as key and any value.
        # If the input to action comes from another action, we store a tuple of output index of the other action,
        # and the reference to the other action.
        self.input_params: dict[
            core.ID, str | int | float | bool | core.ActionDataValueVariable | tuple[core.ID, core.ActionRuntime]] = {}
        self.output_params: dict[core.ID, str | int | float | bool] = {}

        self.id: str = ""
        if self.definition is not None:
            self.id = core.IdProvider.generate_action_id(self.definition.name)

        self.exec_code: str = ""

        if self.definition is not None:
            self.__init_exec_code()

    # Initializes executable code by substituting variable names.
    # Variable names will have the form <action_runtime_id>_<input/output_name>
    def __init_exec_code(self):
        exec_file_path = path_utils.get_absolute_path(self.definition.exec_path, self.definition.filepath)
        self.exec_code = path_utils.read_file(exec_file_path)

        sub_var_names = []
        for i in self.definition.inputs:
            input_id = core.IdProvider.generate_io_id(True, self.definition.name, i.name)
            sub_var_names.append(str(input_id))
            self.input_params[input_id] = i.value
        for o in self.definition.outputs:
            output_id = core.IdProvider.generate_io_id(False, self.definition.name, o.name)
            sub_var_names.append(str(output_id))
            self.output_params[output_id] = o.value

        self.exec_code = self.exec_code.format(*sub_var_names)

    @staticmethod
    def __is_value_of_type(value: Any, expected_type: core.ActionDataType) -> bool:
        if expected_type == core.ActionDataType.Empty:
            return True
        elif expected_type == core.ActionDataType.Boolean:
            if type(value) == bool:
                return True
        elif expected_type == core.ActionDataType.Integer:
            if type(value) == int:
                return True
        elif expected_type == core.ActionDataType.Float:
            if type(value) == float:
                return True
        elif expected_type == core.ActionDataType.String or expected_type == core.ActionDataType.Path:
            if type(value) == str:
                return True
        elif expected_type == core.ActionDataType.Vector2:
            if type(value) == list and len(value) == 2:
                return True
        elif expected_type == core.ActionDataType.Vector3:
            if type(value) == list and len(value) == 3:
                return True
        elif expected_type == core.ActionDataType.Vector4:
            if type(value) == list and len(value) == 4:
                return True
        elif expected_type == core.ActionDataType.Object:
            return True
        return False

    # Links the value of an input with its input_id
    def set_input(self, input_index: int, value) -> bool:
        if input_index >= len(self.definition.inputs):
            return False
        # if not ActionRuntime.__is_value_of_type(value, self.definition.inputs[input_index].type):
        #     return False

        if self.definition.inputs[input_index].type == core.ActionDataType.Object:
            # TODO: Add error logging
            print("Setting input of type: {} is not allowed".format(self.definition.inputs[input_index].type.name))
            return False

        input_id = list(self.input_params.keys())[input_index]
        self.input_params[input_id] = value
        return True

    # Resets the value of an input to its default value
    def reset_input(self, input_index: int) -> bool:
        if input_index >= len(self.definition.inputs):
            return False

        input_id = list(self.input_params.keys())[input_index]
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

        input_id = list(self.input_params.keys())[input_index]
        output_id = list(link_action.output_params.keys())[link_output_index]
        self.input_params[input_id] = (output_id, link_action)
        return True

    # Remove the input link
    def unlink_input(self, input_index: int) -> bool:
        if input_index >= len(self.definition.inputs):
            return False
        self.reset_input(input_index)
        return True

    @staticmethod
    def __get_value_from_variable(entity: core.Entity, variable: core.ActionDataValueVariable):
        if variable == core.ActionDataValueVariable.ENTITY_PATH:
            return entity.path
        elif variable == core.ActionDataValueVariable.ENTITY_NAME:
            return entity.filename

    # Gets the final executable code with properly substituted variables names and values.
    def get_exec_code(self, entity: core.Entity) -> str:
        # print("Code before substitution: \n{}".format(self.exec_code))

        # Replace all inputs in code with linked output variable names
        tmp_code = str(self.exec_code)
        for (param_id, value) in self.input_params.items():
            code_val = value

            if type(value) == tuple:
                code_val = value[0]
            elif type(value) == core.ActionDataValueVariable:
                code_val = ActionRuntime.__get_value_from_variable(entity, value)
            elif type(value) == str and value.find('$') > -1:
                # Find all the variables present in the value
                found_variables: list[core.ActionDataValueVariable] = []
                for var in core.ActionDataValueVariable:
                    if var.name in value:
                        found_variables.append(var)
                # Replace each variable with its actual value
                for v in found_variables:
                    value = value.replace(f'${v.name}', ActionRuntime.__get_value_from_variable(entity, v))
                code_val = value

            # Make sure all string values are converted to literals (with "" quotes)
            if type(code_val) == str:
                code_val = path_utils.get_str_literals(code_val)

            # Replace all input variables by their values or reference to other variables
            tmp_code = tmp_code.replace(str(param_id), str(code_val))

        # print("Code after substitution: \n{}".format(tmp_code))
        return tmp_code
