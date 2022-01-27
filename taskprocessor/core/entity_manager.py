from __future__ import annotations

import six

if six.PY2:
    from pathlib2 import Path
else:
    from pathlib import Path

import taskprocessor.utils.path_utils as path_utils
import taskprocessor.core as core


class EntityManager(object):

    def __init__(self):
        self.entities: [core.Entity] = []
        pass

    def set_entities(self, paths: [str | Path]):
        files = []
        for p in paths:
            files.extend(path_utils.list_files(p, recursive=True))

        self.entities = []
        for f in files:
            self.entities.append(core.Entity(f))

    def add_entity(self, path: [str | Path]):
        files = path_utils.list_files(path)
        for f in files:
            self.entities.append(f)

    def remove_entity(self, path: [str | Path]):
        path = Path(path)
        self.entities.remove(path.absolute())

    def get_entity_extensions(self) -> set:
        extensions = set()
        for e in self.entities:
            extensions.add(e.get_extension())
        return extensions

