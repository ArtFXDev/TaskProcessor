from __future__ import annotations

from typing import Any
import taskprocessor.utils.path_utils as path_utils


class Entity(object):

    def __init__(self, path: str = "dummy/path"):
        self.path: str = path
        self.label: str = path_utils.get_name_from_path(path)
        self.filename: str = self.label[:self.label.find('.')]
        # Task input data which varies per entity
        self.task_data: dict[str, Any] = {}

    def add_task_data(self, input_id: str, value: Any):
        self.task_data[input_id] = value

    def get_extension(self) -> str:
        return path_utils.get_extension(self.path)
