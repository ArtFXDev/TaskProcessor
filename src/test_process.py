import unittest
import taskprocessor.core as core


class MyTestCase(unittest.TestCase):
    def test_processor(self):
        print("<----RUNNING TASK PROCESSOR TEST---->")

        # Create an entity with hard coded path.
        entity1 = core.Entity(
            "C:/Users/User/Desktop/SchoolFiles/Pipeline/MOVIE/ASSETS/CAR/MODELING/PUBLISHED/CAR_MODELING_V001.mb")
        entity2 = core.Entity(
            "C:/Users/User/Desktop/SchoolFiles/Pipeline/MOVIE/ASSETS/CAR/SURFACING/WIP/CAR_SURFACING_V002.ma")

        task1 = core.Task(entity1)
        task2 = core.Task(entity2)

        action_definition1 = core.ActionDefinition()
        action_definition1.label = "Test1Label"
        action_definition1.name = "Test1Name"
        action_definition1.exe_code = "Test1Exe"

        action_runtime1 = core.ActionRuntime(action_definition1)
        action_runtime2 = core.ActionRuntime(action_definition1)

        task1.add_actions([action_runtime1, action_runtime2])
        task2.add_actions([action_runtime1, action_runtime2])

        job = core.Job([task1, task2])

        processor = core.Processor(job)

        processor()

        print("<----COMPLETED TASK PROCESSOR TEST---->")

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

        # Initialize Action manager
        action_paths = ["../taskprocessor/resources"]
        am = core.ActionManager(action_paths)

        # Create three action runtimes (Similar to adding three nodes in the UI)
        action_random_name_gen = am.create_action("random_name_generator")
        action_create_file = am.create_action("create_file")
        action_write_file = am.create_action("write_file")


        # Change inputs
        # Set random name generation length
        am.set_input(action_random_name_gen.id, 0, 12)
        # Set filepath
        am.set_input(action_create_file.id,
                     0,
                     '"D:/Personal_Work/Pipeline/TaskProcessor/TaskProcessor/taskprocessor/resources/gen_file.txt"')

        # Link filepath input of this node with output of create file node
        am.link_input(action_write_file.id, 0, action_create_file.id, 0)
        # Link filepath input of this node with output of create file node
        am.link_input(action_write_file.id, 1, action_random_name_gen.id, 0)

        # Add actions to task
        task = core.Task(None)
        task.add_actions(am.actions)
        task.start()

        print("<----COMPLETED TASK EXECUTION TEST---->")


if __name__ == '__main__':
    unittest.main()
