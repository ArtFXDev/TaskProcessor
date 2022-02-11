from __future__ import annotations

from pathlib import Path

import taskprocessor.utils.path_utils as path_utils
import taskprocessor.core as core


class EntityManager(object):

    def __init__(self):
        self.entities: [core.Entity] = [core.Entity("dummy")]
        self.extensions: list[str] = ["*"]

    def set_entities(self, paths: [str | Path]):
        files = []
        for p in paths:
            files.extend(path_utils.list_files(p, recursive=True, extensions=self.extensions))

        self.entities: [core.Entity] = []
        for f in files:
            self.entities.append(core.Entity(f))

    def add_entity(self, path: [str | Path]):

        if len(self.entities) == 1 and self.entities[0].path == "dummy":
            self.entities.clear()

        files = path_utils.list_files(path, recursive=True, extensions=self.extensions)
        for f in files:
            self.entities.append(core.Entity(f))

    def remove_entity(self, path: [str | Path]):
        path = Path(path)
        rm_entity = next((e for e in self.entities if e.path == str(path.absolute())), None)
        self.entities.remove(rm_entity)

    def get_entity_extensions(self) -> set:
        extensions = set()
        for e in self.entities:
            extensions.add(e.get_extension())
        return extensions

