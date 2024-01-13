import json
import re
import os
from time import process_time
from turtle import update

from unittest import TestCase
from unittest.mock import MagicMock, call

from .. import MyTestCase

import sys
sys.path.append('/home/acobb/git/game_process_calculator/game_process_calculator')
from game_process_calculator import (Project,
    ProjectFilter,
    Resource,
    ResourceFilter,
    Process,
    ProcessFilter,
    Workflow,
    ProcessType,
    WorkflowFilter)
from game_process_calculator import (ProjectHandler,
    ResourceHandler,
    ProcessHandler,
    WorkflowHandler,
    DataHandler)


class DataTest(MyTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.test_dir = os.path.join(os.getcwd(), 'test', 'test_data')
        self.dh = DataHandler()
        self.dh.project_handler.save_dir = self.test_dir
        self.dh.resource_handler.save_dir = self.test_dir
        self.dh.process_handler.save_dir = self.test_dir
        self.dh.workflow_handler.save_dir = self.test_dir

        self.clear_test_data()

    def clear_test_data(self):
        for fl in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, fl))

    def test_simple_linear_scenario(self):
        """
        A simple scenario:
            - Project 1
                - Resources: 
                - Processes:
                - Workflows:
            - Project 2
                - Resources: 
                - Processes:
                - Workflows:
        """
        # Project 1
        project1 = Project(name='Testing Project 1')
        self.dh.create_project(project1)

        starting_resource = Resource(name='Starting Resource', project_uid=project1.uid)
        intermediate_resource = Resource(name='Intermediate Resource', project_uid=project1.uid,
            value_obj_uid=starting_resource.uid, value_amount=5)
        finished_resource = Resource(name='Finished Resource', project_uid=project1.uid,
            value_obj_uid=starting_resource.uid, value_amount=25)
        self.dh.create_resource(starting_resource)
        self.dh.create_resource(intermediate_resource)
        self.dh.create_resource(finished_resource)

        first_process = Process(name='First Process', project_uid=project1.uid,
            consume_uids={starting_resource.uid: 5}, produce_uids={intermediate_resource.uid: 1},
            process_time=15)
        second_process = Process(name='Second Process', project_uid=project1.uid,
            consume_uids={intermediate_resource.uid: 5}, produce_uids={finished_resource.uid: 1},
            process_time=30)
        self.dh.create_process(first_process)
        self.dh.create_process(second_process)

        workflow = Workflow(name='Simple Linear Workflow', project_uid=project1.uid,
            process_uids=[first_process.uid, second_process.uid], process_type=ProcessType.LINEAR)
        self.dh.create_workflow(workflow)

        # Project 2
        project2 = Project(name='Testing Project 2')
        self.dh.create_project(project2)

        starting_resource = Resource(name='Starting Resource', project_uid=project2.uid)
        intermediate_resource = Resource(name='Intermediate Resource', project_uid=project2.uid,
            value_obj_uid=starting_resource.uid, value_amount=5)
        finished_resource = Resource(name='Finished Resource', project_uid=project2.uid,
            value_obj_uid=starting_resource.uid, value_amount=25)
        self.dh.create_resource(starting_resource)
        self.dh.create_resource(intermediate_resource)
        self.dh.create_resource(finished_resource)

        first_process = Process(name='First Process', project_uid=project2.uid,
            consume_uids={starting_resource.uid: 5}, produce_uids={intermediate_resource.uid: 1},
            process_time=15)
        second_process = Process(name='Second Process', project_uid=project2.uid,
            consume_uids={intermediate_resource.uid: 5}, produce_uids={finished_resource.uid: 1},
            process_time=30)
        self.dh.create_process(first_process)
        self.dh.create_process(second_process)

        workflow = Workflow(name='Simple Linear Workflow', project_uid=project2.uid,
            process_uids=[first_process.uid, second_process.uid], process_type=ProcessType.LINEAR)
        self.dh.create_workflow(workflow)

        # Project 3
        project3 = Project(name='Testing Project 3')
        self.dh.create_project(project3)

        starting_resource = Resource(name='Starting Resource', project_uid=project3.uid)
        intermediate_resource = Resource(name='Intermediate Resource', project_uid=project3.uid,
            value_obj_uid=starting_resource.uid, value_amount=5)
        finished_resource = Resource(name='Finished Resource', project_uid=project3.uid,
            value_obj_uid=starting_resource.uid, value_amount=25)
        self.dh.create_resource(starting_resource)
        self.dh.create_resource(intermediate_resource)
        self.dh.create_resource(finished_resource)

        first_process = Process(name='First Process', project_uid=project3.uid,
            consume_uids={starting_resource.uid: 5}, produce_uids={intermediate_resource.uid: 1},
            process_time=15)
        second_process = Process(name='Second Process', project_uid=project3.uid,
            consume_uids={intermediate_resource.uid: 5}, produce_uids={finished_resource.uid: 1},
            process_time=30)
        self.dh.create_process(first_process)
        self.dh.create_process(second_process)

        workflow = Workflow(name='Simple Linear Workflow', project_uid=project3.uid,
            process_uids=[first_process.uid, second_process.uid], process_type=ProcessType.LINEAR)
        self.dh.create_workflow(workflow)

        # Filter results
        # Project
        project_1_filter = ProjectFilter()
        filter_project_1 = self.dh.filter_projects(project_1_filter)
        self.assertEqual(len(filter_project_1), 3)

        project_2_filter = ProjectFilter(name=[project2.name])
        filter_project_2 = self.dh.filter_projects(project_2_filter)
        self.assertEqual(len(filter_project_2), 1)

        # Resource
        resource_1_filter = ResourceFilter(name=[starting_resource.name])
        filter_resource_1 = self.dh.filter_resources(resource_1_filter)
        self.assertEqual(len(filter_resource_1), 3)

        resource_2_filter = ResourceFilter(project_uid=[project1.uid], name=[starting_resource.name])
        filter_resource_2 = self.dh.filter_resources(resource_2_filter)
        self.assertEqual(len(filter_resource_2), 1)

        # Process
        process_1_filter = ProcessFilter(name=[first_process.name])
        filter_process_1 = self.dh.filter_processes(process_1_filter)
        self.assertEqual(len(filter_process_1), 3)

        process_2_filter = ProcessFilter(project_uid=[project1.uid], name=[first_process.name])
        filter_process_2 = self.dh.filter_processes(process_2_filter)
        self.assertEqual(len(filter_process_2), 1)

        # Workflow
        workflow_1_filter = WorkflowFilter(name=[workflow.name])
        filter_workflow_1 = self.dh.filter_workflows(workflow_1_filter)
        self.assertEqual(len(filter_workflow_1), 3)

        workflow_2_filter = WorkflowFilter(project_uid=[project1.uid], name=[workflow.name])
        filter_workflow_2 = self.dh.filter_workflows(workflow_2_filter)
        self.assertEqual(len(filter_workflow_2), 1)

        # UID lists
        project_uids = self.dh.filter_projects(ProjectFilter())
        resource_uids = self.dh.filter_resources(ResourceFilter())
        process_uids = self.dh.filter_processes(ProcessFilter())
        workflow_uids = self.dh.filter_workflows(WorkflowFilter())

        print(f"project_uids: {len(project_uids)}")
        print(f"resource_uids: {len(resource_uids)}")
        print(f"process_uids: {len(process_uids)}")
        print(f"workflow_uids: {len(workflow_uids)}")

        # Update Records
        update_project = self.dh.filter_projects(ProjectFilter(name=[project2.name]))[0]
        update_project.name = 'Updated Project'
        self.dh.update_project(update_project)

        update_resource = self.dh.filter_resources(
            ResourceFilter(project_uid=[project1.uid], name=[intermediate_resource.name]))[0]
        update_resource.name = 'Updated Resource'
        self.dh.update_resource(update_resource)

        update_process = self.dh.filter_processes(
            ProcessFilter(project_uids=[project1.uid], name=[second_process.name]))[0]
        update_process.name = 'Updated Process'
        self.dh.update_process(update_process)

        update_workflow = self.dh.filter_workflows(
            WorkflowFilter(project_uids=[project1.uid], name=[workflow.name]))[0]
        update_workflow.name = 'Updated Workflow'
        self.dh.update_workflow(update_workflow)

        # Delete Records
        self.dh.delete_project(update_project)

        self.dh.delete_resource(update_resource)

        self.dh.delete_process(update_process)

        self.dh.delete_workflow(update_workflow)

        # UID lists
        final_project_uids = self.dh.filter_projects(ProjectFilter())
        final_resource_uids = self.dh.filter_resources(ResourceFilter())
        final_process_uids = self.dh.filter_processes(ProcessFilter())
        final_workflow_uids = self.dh.filter_workflows(WorkflowFilter())

        print(f"project_uids: {len(project_uids), len(final_project_uids)}")
        print(f"resource_uids: {len(resource_uids), len(final_resource_uids)}")
        print(f"process_uids: {len(process_uids), len(final_process_uids)}")
        print(f"workflow_uids: {len(workflow_uids), len(final_workflow_uids)}")

        self.assertEqual(len(project_uids), len(final_project_uids) + 1)
        self.assertEqual(len(resource_uids), len(final_resource_uids) + 1)
        self.assertEqual(len(process_uids), len(final_process_uids) + 1)
        self.assertEqual(len(workflow_uids), len(final_workflow_uids) + 1)

    # def test_fail_to_update_locked_parameters(self):
    #     pass

    # def test_duplicate_project(self):
    #     pass

    # def test_duplicate_resource(self):
    #     pass

    # def test_duplicate_process(self):
    #     pass

    # def test_fail_to_create_resource_due_to_missing_records(self):
    #     pass

    # def test_fail_to_create_process_due_to_missing_records(self):
    #     pass

