from __future__ import annotations

from enum import Enum

import taskprocessor.core as core
import taskprocessor.utils.path_utils as path_utils
import taskprocessor.utils.json_utils as json_utils


class ActionDataType(Enum):
    Empty = 0,
    Boolean = 1,
    String = 2,
    Integer = 3,
    Float = 4,
    Path = 5


class ActionData(object):
    # current_count = 0

    def __init__(self,
                 label: str,
                 data_type: ActionDataType = ActionDataType.Empty,
                 value=None):
        self.label = label
        self.name = path_utils.get_name_from_label(self.label)
        # self.id = self.name + "_" + str(ActionData.current_count)
        self.type = data_type
        self.value = value

        # ActionData.current_count += 1

    # Covert current ActionData object from dict to string
    def __str__(self):
        data = self.__dict__
        # Convert ActionDataType enum to string
        data['type'] = self.type.name
        return json_utils.dict_to_json(data)

    # Get json string from current ActionData object
    def to_json(self) -> str:
        return self.__str__()

    # Get a ActionData object from json string
    @staticmethod
    def from_json(json_data) -> ActionData:
        # TODO: Throw exceptions on fail
        json_dict = json_utils.json_to_dict(json_data)
        action_data = ActionData(json_dict['label'],
                                 ActionDataType[json_dict['type']],
                                 json_dict['value'])

        return action_data
