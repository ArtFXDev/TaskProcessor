from __future__ import annotations

import taskprocessor.utils.path_utils as path_utils


class Entity(object):

    def __init__(self, path: str = "dummy/path"):
        self.path: str = path
        self.label: str = path_utils.get_name_from_path(path)

    def get_extension(self) -> str:
        return path_utils.get_extension(self.path)
