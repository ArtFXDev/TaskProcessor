from __future__ import annotations

import taskprocessor.utils.path_utils as path_utils


class ID(object):
    def __init__(self, name: str, transform: bool = True):
        self.name = path_utils.get_name_from_label(name) if transform else name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other: ID) -> bool:
        return self.name == other.name

    def __str__(self) -> str:
        return self.name


class IdProvider(object):
    # A dictionary with the action name as key and a counter as value.
    # The counter is used to generate ID.
    __action_ids: dict[str, int] = {}
    __action_io_ids: dict[str, int] = {}

    def __init__(self):
        pass

    @staticmethod
    def generate_action_id(action_name: str) -> ID:
        """
        Generates new ID for ActionRuntime with each call.
        ID will have the form <action_name>_<count>
        :param action_name: name of ActionRuntime
        :return: ID object
        """

        count = IdProvider.__action_ids.get(action_name, -1)
        count += 1

        curr_id = str(action_name)
        if count > 0:
            curr_id += "_" + str(count)

        IdProvider.__action_ids[action_name] = count

        return ID(curr_id)

    @staticmethod
    def generate_io_id(is_input: bool, action_name: str, io_name: str) -> ID:
        """
        Generates unique ID for input/output ActionData with each call
        :param is_input: Indicate if it's an input or output ActionData
        :param action_name: name of the ActionRuntime this input/output ActionData belongs to
        :param io_name: name of the input/output ActionData
        :return: ID object
        """
        key_params = [action_name, ('i' if is_input else 'o'), io_name]
        key = '_'.join(key_params)

        count = IdProvider.__action_io_ids.get(key, -1)
        count += 1

        curr_id = str(key)
        if count > 0:
            curr_id += "_" + str(count)

        IdProvider.__action_io_ids[key] = count

        return ID(curr_id)
