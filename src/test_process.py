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

    def test_task_execution(self):
        print("<----RUNNING TASK EXECUTION TEST---->")

        # Initialize Engine
        engine_config_path = "../resources/configs/config_engine.json"
        eg = engine.Engine(engine_config_path)

        # Set current engine
        is_engine_set = eg.set_current_engine("python")
        if is_engine_set:
            print("Engine set to: {}".format(eg.current_engine.name))
        else:
            print("Engine not found")
            return False
        print("\n")

        # Initialize Entities
        em = core.EntityManager()
        em.extensions = eg.current_engine.extensions
        em.add_entity('../resources/example_entities')

        if len(em.entities) == 0:
            print("No entities found")
            return False

        print("Listing entities:")
        for e in em.entities:
            print(e.path)
        print("\n")

        # Initialize Action manager
        action_paths = ["../actions"]
        am = core.ActionManager(action_paths)
        am.set_current_engine(eg.current_engine.name)

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
        am.set_input(action_random_name_gen.id, 0, 12)
        # Set filepath
        am.set_input(action_create_file.id,
                     0,
                     '"D:/Personal_Work/Pipeline/TaskProcessor/TaskProcessor/build/gen_file.txt"')

        # Link filepath input of this node with output of create file node
        am.link_input(action_write_file.id, 0, action_create_file.id, 0)
        # Link filepath input of this node with output of create file node
        am.link_input(action_write_file.id, 1, action_random_name_gen.id, 0)

        print('\n')
        proc = core.Processor(eg)
        proc.create_job(em.entities, am.actions)
        proc.start()
        print('\n')

        print("<----COMPLETED TASK EXECUTION TEST---->")

    def test_engine(self):
        print("<----RUNNING ENGINE TEST---->")

        engine_config_path = "../resources/configs/config_engine.json"
        eg = engine.Engine(engine_config_path)
        for e in eg.engine_data:
            print(e)

        print("<----COMPLETED ENGINE TEST---->")


if __name__ == '__main__':
    unittest.main()
