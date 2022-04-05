from __future__ import annotations
from typing import Any, Callable

from enum import Enum
from pathlib import Path
import taskprocessor.core as core
import taskprocessor.core.engine as engine


class CoreManager(object):
    _action_def_paths = ["../../actions"]
    _engine_config_path = "../../resources/configs/config_engine.json"

    class ActionFilterType(Enum):
        All = 0,
        Name = 1,
        EngineName = 2

    def __init__(self):
        self._engine = engine.Engine(CoreManager._engine_config_path)
        self._action_def_provider = core.ActionDefinitionProvider(CoreManager._action_def_paths)
        self._entity_manager = core.EntityManager()
        self._action_manager = core.ActionManager(self._action_def_provider)
        self._processor = core.Processor(self._engine)

    def set_engine(self, engine_name: str) -> bool:
        engine_name = engine_name.lower().replace(' ', '_')
        is_set = self._engine.set_current_engine(engine_name)
        if not is_set:
            print("Engine not found")
            return False
        else:
            self._entity_manager.extensions = self._engine.current_engine.extensions
            return True

    def get_current_engine(self) -> str:
        return self._engine.current_engine.name

    def add_entity(self, entity: str | Path):
        self._entity_manager.add_entity(entity)

    def remove_entity(self, entity: str | Path):
        self._entity_manager.remove_entity(entity)

    def get_entities(self) -> list[core.Entity]:
        return self._entity_manager.entities

    def get_action_definitions(self,
                               filter_by: ActionFilterType = ActionFilterType.All,
                               filter_value: str = "") -> list[core.ActionDefinition]:
        if filter_by is self.ActionFilterType.All:
            return self._action_def_provider.get_all()
        elif filter_by is self.ActionFilterType.Name:
            return [self._action_def_provider.get_by_name(filter_value)]
        elif filter_by is self.ActionFilterType.EngineName:
            return self._action_def_provider.get_by_engine(filter_value)

    def create_action(self, name: str) -> core.ActionRuntime | None:
        action = self._action_manager.create_action(name)
        return action

    def delete_action(self, action_id: core.ID) -> bool:
        return self._action_manager.delete_action(action_id)

    def set_input(self, action_id: core.ID, index: int, value: Any) -> bool:
        return self._action_manager.set_input(action_id, index, value)

    def reset_input(self, action_id: core.ID, index: int) -> bool:
        return self._action_manager.reset_input(action_id, index)

    def link_input(self,
                   action_id: core.ID,
                   input_index: int,
                   incoming_action_id: core.ID,
                   incoming_output_id: int) -> bool:
        return self._action_manager.link_input(action_id, input_index, incoming_action_id, incoming_output_id)

    def unlink_input(self,
                     action_id: core.ID, input_index: int) -> bool:
        return self._action_manager.unlink_input(action_id, input_index)

    def set_on_process_listeners(self,
                                 start_callback: Callable[[str], None] | None = None,
                                 progress_callback: Callable[[str, str, float, float, str], None] | None = None,
                                 error_callback: Callable[[str], None] | None = None,
                                 completed_callback: Callable[[bool, str], None] | None = None):
        if start_callback is not None:
            self._processor.add_on_start_listener(start_callback)
        if progress_callback is not None:
            self._processor.add_on_progress_listener(progress_callback)
        if error_callback is not None:
            self._processor.add_on_error_listener(error_callback)
        if completed_callback is not None:
            self._processor.add_on_completed_listener(completed_callback)

    def remove_on_process_listeners(self,
                                    start_callback: Callable[[str], None] | None = None,
                                    progress_callback: Callable[[str, str, float, float, str], None] | None = None,
                                    error_callback: Callable[[str], None] | None = None,
                                    completed_callback: Callable[[bool, str], None] | None = None):
        if start_callback is not None:
            self._processor.remove_on_start_listener(start_callback)
        if progress_callback is not None:
            self._processor.remove_on_progress_listener(progress_callback)
        if error_callback is not None:
            self._processor.remove_on_error_listener(error_callback)
        if completed_callback is not None:
            self._processor.remove_on_completed_listener(completed_callback)

    def run(self):
        node_graph = core.NodeGraph(self._action_manager.actions)
        self._processor.create_job(self._entity_manager.entities, node_graph.get_actions())
        self._processor.start()
