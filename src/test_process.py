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
        for a in am.action_runtimes:
            print(a.action_definition.name)

        search_criteria = "example"
        print("Actions containing name: {0}:".format(search_criteria))
        for a in am.get_actions_by_name(search_criteria):
            print(a.action_definition.name)

        print("<----COMPLETED ACTION MANAGER TEST---->")

    def test_task_execution(self):
        print("<----RUNNING TASK EXECUTION TEST---->")

        # Initialize Action manager
        action_paths = ["../taskprocessor/resources"]
        am = core.ActionManager(action_paths)

        # Get three actions (Similar to adding three nodes in the UI)
        action_random_name_gen = am.get_actions_by_name("random_name_gen")[0]
        action_create_file = am.get_actions_by_name("create_file")[0]
        action_write_file = am.get_actions_by_name("write_file")[0]

        # Change inputs
        # Set random name generation length
        action_random_name_gen.set_input(0, 12)
        action_create_file.set_input(0, '"D:/Personal_Work/Pipeline/TaskProcessor/TaskProcessor/taskprocessor/resources/gen_file.txt"')

        # Link filepath input of this node with output of create file node
        action_write_file.link_input(0, None, action_create_file.action_definition.outputs[0].id)
        # Link filepath input of this node with output of create file node
        action_write_file.link_input(1, None, action_random_name_gen.action_definition.outputs[0].id)

        # Add actions to task
        actions = [action_random_name_gen, action_create_file, action_write_file]
        task = core.Task(None)
        task.add_actions(actions)
        task.start()

        print("<----COMPLETED TASK EXECUTION TEST---->")



if __name__ == '__main__':
    unittest.main()
