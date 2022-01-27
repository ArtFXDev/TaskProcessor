import taskprocessor.utils.path_utils as path_utils


class Entity(object):

    def __init__(self, path):
        # TODO: Replace the path by processor data type.
        self.path = path
        self.id = "Entity" + str(id(self))
        self.label = path_utils.get_name_from_path(path)
        print("Init entity: {} \nIn path: {} \nid: {}".format(self.label, self.path, self.id))
        pass
