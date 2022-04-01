from __future__ import annotations

import random
import unittest
import taskprocessor.core as core
import taskprocessor.core.engine as engine


class MyTestCase(unittest.TestCase):
    def test_action_manager(self):
        print("<----RUNNING ACTION MANAGER TEST---->")

        action_paths = ["./taskprocessor/resources",
                        "C:/Users/suraj/Documents/taskprocessor"]

        am = core.ActionManager(action_paths)
        print("All Actions:")
        for a in am.actions:
            print(a.definition.name)

        search_criteria = "example"
        print("Actions containing name: {0}:".format(search_criteria))
        for a in am.get_actions_by_name(search_criteria):
            print(a.definition.name)

        print("<----COMPLETED ACTION MANAGER TEST---->")

    def create_maya_example_actions(self, am: core.ActionManager):
        action_open_file = am.create_action("open_file")
        if action_open_file is None:
            print("Failed to create node: open_file")
            return False
        action_create_sphere = am.create_action("create_sphere")
        if action_create_sphere is None:
            print("Failed to create node: create_sphere")
            return False
        action_random_name_gen = am.create_action("random_name_generator")
        if action_random_name_gen is None:
            print("Failed to create node: random_name_generator")
            return False
        action_save_file = am.create_action("save_file")
        if action_save_file is None:
            print("Failed to create node: save_file")
            return False
        action_export_abc = am.create_action("export_alembic")
        if action_export_abc is None:
            print("Failed to create node: export_alembic")
            return False

        # Change inputs
        # Change open file input
        is_input_set = am.set_input(action_open_file.id, 0, core.ActionDataValueVariable.ENTITY_PATH)
        if not is_input_set:
            print("Open file input not set")
            return False

        # Set random name generation length
        is_input_set = am.set_input(action_random_name_gen.id, 0, 12)
        if not is_input_set:
            print("Random name input not set")
            return False

        # Set sphere inputs
        is_input_set = am.link_input(action_create_sphere.id, 0, action_random_name_gen.id, 0)
        if not is_input_set:
            print("Sphere name input not set")
            return False
        is_input_set = am.set_input(action_create_sphere.id, 1, random.uniform(0.5, 2.0))
        if not is_input_set:
            print("Sphere radius not set")
            return False

        # Set alembic export inputs
        is_input_set = am.set_input(action_export_abc.id, 0, "1 1")
        if not is_input_set:
            print("Alembic frame-range input not set")
            return False
        is_input_set = am.link_input(action_export_abc.id, 1, action_create_sphere.id, 0)
        if not is_input_set:
            print("Alembic root name input not set")
            return False
        is_input_set = am.set_input(action_export_abc.id, 2, 'C:/Users/suraj/Desktop/export/$ENTITY_NAME.abc')
        if not is_input_set:
            print("Alembic file name input not set")
            return False


    def create_python_example_actions(self, am):
        # Create three action runtimes (Similar to adding three nodes in the UI)
        action_random_name_gen = am.create_action("random_name_generator")
        if action_random_name_gen is None:
            print("Failed to create node: random_name_generator")
            return False
        action_create_file = am.create_action("create_file")
        if action_create_file is None:
            print("Failed to create node: create_file")
            return False
        action_write_file = am.create_action("write_file")
        if action_write_file is None:
            print("Failed to create node: write_file")
            return False

        # Change inputs
        # Set random name generation length
        is_input_set = am.set_input(action_random_name_gen.id, 0, 12)
        if not is_input_set:
            print("Random name input not set")
            return False

        # Set filepath
        is_input_set = am.set_input(action_create_file.id,
                                    0,
                                    '"D:/Personal_Work/Pipeline/TaskProcessor/TaskProcessor/build/gen_file.txt"')
        if not is_input_set:
            print("Create file input not set")
            return False

        # Link filepath input of this node with output of create file node
        is_input_set = am.link_input(action_write_file.id, 0, action_create_file.id, 0)
        if not is_input_set:
            print("Failed to link create file output to write file input")
            return False
        # Link filepath input of this node with output of create file node
        is_input_set = am.link_input(action_write_file.id, 1, action_random_name_gen.id, 0)
        if not is_input_set:
            print("Failed to link random name output to write file input")
            return False

    def test_task_execution(self):
        print("<----RUNNING TASK EXECUTION TEST---->")

        # Initialize Engine
        engine_config_path = "../resources/configs/config_engine.json"
        eg = engine.Engine(engine_config_path)

        # Set current engine
        is_engine_set = eg.set_current_engine("maya")
        if is_engine_set:
            print("Engine set to: {}".format(eg.current_engine.name))
        else:
            print("Engine not found")
            return False
        print("\n")

        # Initialize Entities
        em = core.EntityManager()
        em.extensions = eg.current_engine.extensions
        # em.add_entity('../resources/example_maya_entities/maya_entity_01.ma')
        em.add_entity('../resources/example_maya_entities')

        if len(em.entities) == 0:
            print("No entities found")
            return False

        print("Listing entities:")
        for e in em.entities:
            print(e.path)
        print("\n")

        # Initialize Action definition provider
        action_paths = ["../actions"]
        adp = core.ActionDefinitionProvider(action_paths)
        if len(adp.get_all()) == 0:
            print("No action definitions found")
            return False

        # Initialize Action Manager
        am = core.ActionManager(adp)

        # Create actions
        # self.create_python_example_actions(am)
        self.create_maya_example_actions(am)

        # Create node graph for the actions
        node_graph = core.NodeGraph(am.actions)

        # Create a processor, job and start execution
        print('\n')
        proc = core.Processor(eg)
        proc.create_job(em.entities, node_graph.get_actions())
        proc.start()
        print('\n')

        print("<----COMPLETED TASK EXECUTION TEST---->")

    def test_task_serialization(self):
        # Initialize Action definition provider
        action_paths = ["../actions"]
        adp = core.ActionDefinitionProvider(action_paths)
        if len(adp.get_all()) == 0:
            print("No action definitions found")
            return False

        # Initialize Action Manager
        am = core.ActionManager(adp)

        # Create actions
        # self.create_python_example_actions(am)
        self.create_maya_example_actions(am)

        # Create node graph for the actions
        node_graph = core.NodeGraph(am.actions)

        task = core.Task(None, node_graph.get_actions(), "Maya Alembic Export Task")
        print("Complete JSON:")
        print(task.to_json(include_action_def=True, include_action_init_code=True))
        # print("Min JSON:")
        # print(task.to_json(False, False))

    def test_engine(self):
        print("<----RUNNING ENGINE TEST---->")

        engine_config_path = "../resources/configs/config_engine.json"
        eg = engine.Engine(engine_config_path)
        for e in eg.engine_data:
            print(e)

        print("<----COMPLETED ENGINE TEST---->")


if __name__ == '__main__':
    unittest.main()
