from __future__ import annotations

import random
import unittest
from taskprocessor import config_manager
import taskprocessor.core as core
import taskprocessor.core.engine as engine


class MyTestCase(unittest.TestCase):
    def create_maya_example_actions(self, core_manager: core.CoreManager):
        action_open_file = core_manager.create_action("open_file")
        if action_open_file is None:
            print("Failed to create node: open_file")
            return False
        action_create_sphere = core_manager.create_action("create_sphere")
        if action_create_sphere is None:
            print("Failed to create node: create_sphere")
            return False
        action_random_name_gen = core_manager.create_action("random_name_generator")
        if action_random_name_gen is None:
            print("Failed to create node: random_name_generator")
            return False
        action_save_file = core_manager.create_action("save_file")
        if action_save_file is None:
            print("Failed to create node: save_file")
            return False
        action_export_abc = core_manager.create_action("export_alembic")
        if action_export_abc is None:
            print("Failed to create node: export_alembic")
            return False

        # Change inputs
        # Change open file input
        is_input_set = core_manager.set_input(action_open_file.id, 1, core.ActionDataValueVariable.ENTITY_PATH)
        if not is_input_set:
            print("Open file input not set")
            return False

        # Set random name generation length
        is_input_set = core_manager.set_input(action_random_name_gen.id, 1, 12)
        if not is_input_set:
            print("Random name input not set")
            return False

        # Set sphere inputs
        is_input_set = core_manager.link_input(action_create_sphere.id, 1, action_random_name_gen.id, 1)
        if not is_input_set:
            print("Sphere name input not set")
            return False
        is_input_set = core_manager.set_input(action_create_sphere.id, 2, random.uniform(0.5, 2.0))
        if not is_input_set:
            print("Sphere radius not set")
            return False

        # Set alembic export inputs
        is_input_set = core_manager.set_input(action_export_abc.id, 1, "1 1")
        if not is_input_set:
            print("Alembic frame-range input not set")
            return False
        is_input_set = core_manager.link_input(action_export_abc.id, 2, action_create_sphere.id, 1)
        if not is_input_set:
            print("Alembic root name input not set")
            return False
        is_input_set = core_manager.set_input(action_export_abc.id, 3,
                                              f'{config_manager.get_build_dir()}/$ENTITY_NAME.abc')
        if not is_input_set:
            print("Alembic file name input not set")
            return False

    def create_python_example_actions(self, core_manager: core.CoreManager):
        # Create three action runtimes (Similar to adding three nodes in the UI)
        action_random_name_gen = core_manager.create_action("random_name_generator")
        if action_random_name_gen is None:
            print("Failed to create node: random_name_generator")
            return False
        action_create_file = core_manager.create_action("create_file")
        if action_create_file is None:
            print("Failed to create node: create_file")
            return False
        action_write_file = core_manager.create_action("write_file")
        if action_write_file is None:
            print("Failed to create node: write_file")
            return False

        # Change inputs
        # Set random name generation length
        is_input_set = core_manager.set_input(action_random_name_gen.id, 0, 12)
        if not is_input_set:
            print("Random name input not set")
            return False

        # Set filepath
        is_input_set = core_manager.set_input(action_create_file.id,
                                              0,
                                              f'"{config_manager.get_build_dir()}/gen_file.txt"')
        if not is_input_set:
            print("Create file input not set")
            return False

        # Link filepath input of this node with output of create file node
        is_input_set = core_manager.link_input(action_write_file.id, 0, action_create_file.id, 0)
        if not is_input_set:
            print("Failed to link create file output to write file input")
            return False
        # Link filepath input of this node with output of create file node
        is_input_set = core_manager.link_input(action_write_file.id, 1, action_random_name_gen.id, 0)
        if not is_input_set:
            print("Failed to link random name output to write file input")
            return False

    def on_exec_started(self, data: str):
        print(f"Execution Started: {data}")

    def on_exec_progress(self, task: str, action: str, total_progress: float, task_progress: float, data: str):
        print(f"Execution Progress: {task} | {action} | {total_progress} | {task_progress}")
        if len(data) > 0:
            print(f"Execution Progress Data: {data}")

    def on_exec_error(self, data: str):
        # print(f"Execution Error: {data}")
        pass

    def on_exec_completed(self, status: bool, data: str):
        print(f"Execution Completed: {status} | {data}")
        print("<----COMPLETED TASK EXECUTION TEST---->")

    def test_task_execution(self):
        print("<----RUNNING TASK EXECUTION TEST---->")

        core_manager = core.CoreManager()
        core_manager.set_engine("maya")
        core_manager.add_entity(config_manager.get_example_maya_entities_dir())
        self.create_maya_example_actions(core_manager)
        core_manager.set_on_process_listeners(self.on_exec_started,
                                              self.on_exec_progress,
                                              self.on_exec_error,
                                              self.on_exec_completed)
        core_manager.run()

    def test_task_serialization(self):
        # Initialize Action definition provider
        core_manager = core.CoreManager()
        self.create_maya_example_actions(core_manager)

        task = core.Task(None, core_manager.get_all_actions(), "Maya Alembic Export Task")
        print("Complete JSON:")
        print(task.to_json(include_action_def=True, include_action_init_code=True))
        # print("Min JSON:")
        # print(task.to_json(False, False))

    def test_engine(self):
        print("<----RUNNING ENGINE TEST---->")

        eg = engine.Engine(config_manager.get_engine_config_path())
        for e in eg.engine_data:
            print(e)

        print("<----COMPLETED ENGINE TEST---->")


if __name__ == '__main__':
    unittest.main()
