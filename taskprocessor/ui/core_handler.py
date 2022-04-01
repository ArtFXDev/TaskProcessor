import taskprocessor.core as core
import taskprocessor.ui.nodes as nodes


class CoreHandler(object):

    def __init__(self):
        # Initialize Action definition provider
        action_paths = ["../../actions"]
        adp = core.ActionDefinitionProvider(action_paths)
        self.actionManager = core.ActionManager(adp)
        self.action_defs = adp.get_all()
        self.nodes = []
        for a in self.action_defs:
            self.nodes.append(nodes.BaseNodeTP.create_node_class_from_def(a))

    def init_node(self, node: nodes.BaseNodeTP):
        print(issubclass(type(node), nodes.BaseNodeTP))
        if not issubclass(type(node), nodes.BaseNodeTP) or node.is_initialized:
            print("Node not of type TaskProcessor")
            return

        action_def = next((a for a in self.action_defs if a.label == node.name()), None)

        if action_def is not None:
            action = self.actionManager.create_action(action_def.name)
            node.initialize(action)
