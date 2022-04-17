from __future__ import annotations
from typing import Any

import taskprocessor.core as core
import taskprocessor.utils.json_utils as json_utils
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

        self.id: core.ID | None = None
        if self.definition is not None:
            self.id = core.IdProvider.generate_action_id(self.definition.name)

        self.exec_code: str = ""

        if self.definition is not None:
            self.__init_exec_code()

    def to_json(self, include_def: bool = True, include_init_code: bool = False) -> str:
        inputs = []
        for (i_id, value) in self.input_params.items():
            if type(value) == core.ActionDataValueVariable:
                value = value.name
            elif type(value) == tuple:
                value = {'connected_action_output_id': str(value[0]), 'connected_action_id': str(value[1].id)}
            i_dict = {'id': str(i_id), 'value': value}
            inputs.append(i_dict)

        outputs = []
        for (o_id, value) in self.output_params.items():
            o_dict = {'id': str(o_id), 'value': value}
            outputs.append(o_dict)

        action_dict = {'id': str(self.id)}
        if include_def:
            action_dict['definition'] = json_utils.json_to_dict(self.definition.to_json())
        else:
            action_dict['definition'] = self.definition.filepath
        action_dict['inputs'] = inputs
        action_dict['outputs'] = outputs
        if include_init_code:
            action_dict['exec_code'] = self.exec_code
        else:
            action_dict['exec_code'] = ""

        return json_utils.dict_to_json(action_dict)

    @staticmethod
    def from_json(json_data: str) -> ActionRuntime:
        action_dict = json_utils.json_to_dict(json_data)

        action_def = action_dict['definition']
        if type(action_def) == str:
            action_def = path_utils.read_file(action_def)
        elif type(action_def) == dict:
            action_def = json_utils.dict_to_json(action_def)

        action_def = core.ActionDefinition.from_json(action_def)

        action = ActionRuntime()
        action.id = core.ID(action_dict['id'])
        action.definition = action_def

        inputs = {}
        for i in action_dict['inputs']:
            i_id = core.ID(i.get('id'))
            value = i.get('value')
            if type(value) == dict:
                value = (core.ID(value.get('connected_action_output_id')),
                         value.get('connected_action_id'))
            else:
                value = next((var for var in core.ActionDataValueVariable if value == var.name), value)
            inputs[i_id] = value
        action.input_params = inputs

        outputs = {}
        for o in action_dict['outputs']:
            outputs[core.ID(o.get('id'))] = o.value
        action.output_params = outputs

        action.exec_code = action_dict['exec_code']
        return action

    def __str__(self) -> str:
        return self.to_json(include_def=False, include_init_code=False)

    # Initializes executable code by substituting variable names.
    # Variable names will have the form <action_runtime_id>_<input/output_name>
    def __init_exec_code(self):
        exec_file_path = path_utils.get_absolute_path(self.definition.exec_path, self.definition.filepath)
        self.exec_code = path_utils.read_file(exec_file_path)

        sub_var_names = []
        for i in self.definition.inputs:
            input_id = core.IdProvider.generate_io_id(True, self.definition.name, i.name)
            self.input_params[input_id] = i.value
            if i.type is not core.ActionDataType.Empty:
                sub_var_names.append(str(input_id))
        for o in self.definition.outputs:
            output_id = core.IdProvider.generate_io_id(False, self.definition.name, o.name)
            self.output_params[output_id] = o.value
            if o.type is not core.ActionDataType.Empty:
                sub_var_names.append(str(output_id))

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

    def get_input_id(self, input_index: int) -> core.ID:
        return list(self.input_params.keys())[input_index]

    def get_input_index(self, input_id: core.ID) -> int:
        return list(self.input_params.keys()).index(input_id)

    def get_input_id_index(self, input_id: int | core.ID | str) -> tuple[int, core.ID]:
        i_id: core.ID | None = None
        i_index: int = -1
        if type(input_id) is int:
            i_index = input_id
            i_id = self.get_input_id(i_index)
        elif type(input_id) is core.ID:
            i_id = input_id
            i_index = self.get_input_index(i_id)
        elif type(input_id) is str:
            i_id = core.ID(input_id, transform=False)
            i_index = self.get_input_index(i_id)

        return i_index, i_id

    def get_output_id(self, output_index: int) -> core.ID:
        return list(self.output_params.keys())[output_index]

    def get_output_index(self, output_id: core.ID) -> int:
        return list(self.output_params.keys()).index(output_id)

    def get_output_id_index(self, output_id: int | core.ID | str) -> tuple[int, core.ID]:
        i_id: core.ID | None = None
        i_index: int = -1
        if type(output_id) is int:
            i_index = output_id
            i_id = self.get_output_id(i_index)
        elif type(output_id) is core.ID:
            i_id = output_id
            i_index = self.get_output_index(i_id)
        elif type(output_id) is str:
            i_id = core.ID(output_id, transform=False)
            i_index = self.get_output_index(i_id)

        return i_index, i_id

    # Links the value of an input with its input_id
    def set_input(self, input_id: int | core.ID | str, value: str | int | float | bool) -> bool:
        (i_index, i_id) = self.get_input_id_index(input_id)
        if i_index >= len(self.definition.inputs):
            print(f"Input index out of range: {i_index}. Max: {len(self.definition.inputs)}")
            return False
        # if not ActionRuntime.__is_value_of_type(value, self.definition.inputs[input_index].type):
        #     return False

        if self.definition.inputs[i_index].type == core.ActionDataType.Object:
            # TODO: Add error logging
            print(f"Setting input of type: {self.definition.inputs[i_index].type.name} is not allowed")
            return False

        self.input_params[i_id] = value
        self.definition.inputs[i_index].value = value
        return True

    def get_input_value(self, input_id: int | core.ID | str) -> str | int | float | bool | None:
        (i_index, i_id) = self.get_input_id_index(input_id)
        if i_index >= len(self.definition.inputs):
            print(f"Input index out of range: {i_index}. Max: {len(self.definition.inputs)}")
            return None

        if type(self.input_params[i_id]) is core.ActionDataValueVariable:
            return None
        if type(self.input_params[i_id]) is tuple:
            return None

        return self.input_params[i_id]

    # Resets the value of an input to its default value
    def reset_input(self, input_id: int | core.ID | str) -> bool:
        (i_index, i_id) = self.get_input_id_index(input_id)
        if i_index >= len(self.definition.inputs):
            print(f"Input index out of range: {i_index}. Max: {len(self.definition.inputs)}")
            return False

        self.input_params[i_id] = self.definition.inputs[i_index].value
        return True

    # Links the output_id of the other action to the input_id of this action.
    # This function is used to link output of one node as an input to this node.
    def link_input(self,
                   input_id: int | core.ID | str,
                   output_action: ActionRuntime,
                   output_id: int | core.ID | str) -> bool:

        (i_index, i_id) = self.get_input_id_index(input_id)
        (o_index, o_id) = output_action.get_output_id_index(output_id)

        if i_index >= len(self.definition.inputs):
            print(f"Input index out of range: {i_index}. Max: {len(self.definition.inputs)}")
            return False
        if o_index >= len(output_action.definition.outputs):
            print(f"Output index out of range: {o_index}. Max: {len(output_action.definition.outputs)}")
            return False
        if self.definition.inputs[i_index].type != output_action.definition.outputs[o_index].type:
            print("Input and output type does not match. Input Type: {} Output Type: {}"
                  .format(self.definition.inputs[i_index].type,
                          output_action.definition.outputs[o_index].type))
            return False

        self.input_params[i_id] = (o_id, output_action)
        return True

    # Remove the input link
    def unlink_input(self, input_id: int | core.ID | str) -> bool:
        (i_index, i_id) = self.get_input_id_index(input_id)
        if i_index >= len(self.definition.inputs):
            print(f"Input index out of range: {i_index}. Max: {len(self.definition.inputs)}")
            return False
        return self.reset_input(i_id)

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
            if value is None:
                continue

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
