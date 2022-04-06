from __future__ import annotations

from pathlib import Path

from NodeGraphQt import Port, BaseNode
from taskprocessor.ui import CoreManager, Entity, ID
from taskprocessor.ui.nodes import BaseNodeTP


class UIManager(object):

    def __init__(self):
        self._node_action_data: dict[str, ID] = {}
        self._core = CoreManager()

    def set_engine(self, engine_name: str) -> bool:
        return self._core.set_engine(engine_name)

    def get_current_engine(self):
        return self._core.get_current_engine()

    def add_entity(self, entity: str | Path):
        self._core.add_entity(entity)

    def remove_entity(self, entity: str | Path):
        self._core.remove_entity(entity)

    def get_entities(self) -> list[Entity]:
        return self._core.get_entities()

    def get_node_classes(self) -> list[BaseNodeTP]:
        actions = self._core.get_action_definitions(filter_by=self._core.ActionFilterType.EngineName,
                                                    filter_value=self.get_current_engine())
        node_classes = []
        for a in actions:
            node_classes.append(BaseNodeTP.create_node_class_from_def(a))
        return node_classes

    def create_node(self, node: BaseNodeTP) -> bool:
        if not issubclass(type(node), BaseNodeTP) or node.is_initialized:
            return False

        action = self._core.create_action(node.ACTION_NAME)

        if action is None:
            return False

        self._node_action_data[node.id] = action.id
        node.initialize(action)
        return True

    def delete_action(self, action_id: ID) -> bool:
        return self._core.delete_action(action_id)

    def delete_nodes(self, node_ids: list[str]):
        for i in node_ids:
            self.delete_action(self._node_action_data[i])
            self._node_action_data.pop(i)

    def connect_nodes(self, input_port: Port, output_port: Port) -> bool:
        in_node = input_port.node()
        out_node = output_port.node()

        if not issubclass(type(input_port.node()), BaseNodeTP) and not issubclass(type(output_port.node()), BaseNodeTP):
            return False

        is_linked = self._core.link_input(in_node.action.id, input_port.name(),
                                          out_node.action.id, output_port.name())

        if is_linked:
            input_widget = in_node.get_widget(input_port.name())
            if input_widget is not None:
                input_widget.widget().setDisabled(True)
        else:
            input_port.disconnect_from(output_port)

        return is_linked

    def disconnect_nodes(self, input_port: Port, output_port: Port) -> bool:
        in_node = input_port.node()

        is_unlinked = self._core.unlink_input(in_node.action.id, input_port.name())

        if is_unlinked:
            input_widget = in_node.get_widget(input_port.name())
            if input_widget is not None:
                input_widget.widget().setDisabled(False)

        return is_unlinked

    def change_node_input(self, node: BaseNodeTP, input_name: str, input_value: object) -> bool:
        if not issubclass(type(node), BaseNodeTP):
            return False

        widget = node.get_widget(input_name)
        if widget is None:
            return False
        self._core.set_input(node.action.id, input_name, input_value)
        return True
