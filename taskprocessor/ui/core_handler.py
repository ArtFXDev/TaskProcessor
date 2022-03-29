import taskprocessor.core as core
import taskprocessor.ui.nodes as nodes


class CoreHandler(object):

    def __init__(self):
        # Initialize Action definition provider
        action_paths = ["../../actions"]
        adp = core.ActionDefinitionProvider(action_paths)

        self.nodes = []
        for a in adp.get_all():
            self.nodes.append(nodes.BaseNodeTP.create_node_class_from_def(a))
