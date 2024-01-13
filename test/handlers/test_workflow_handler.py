import json
import re
import os

from unittest import TestCase
from unittest.mock import MagicMock, call

from game_process_calculator.models import workflow

from .. import MyTestCase

import sys
sys.path.append('/home/acobb/git/game_process_calculator/game_process_calculator')
from game_process_calculator import Project, Resource, ProcessFilter, Process, ProcessFilter, Workflow, ProcessType, WorkflowFilter
from game_process_calculator import ProjectHandler, ResourceHandler, ProcessHandler, WorkflowHandler


class ProcessTest(MyTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.test_dir = os.path.join(os.getcwd(), 'test', 'test_data')
        self.proj_h = ProjectHandler()
        self.proj_h.save_dir = self.test_dir
        self.rh = ResourceHandler()
        self.rh.save_dir = self.test_dir
        self.proc_h = ProcessHandler()
        self.proc_h.save_dir = self.test_dir
        self.wh = WorkflowHandler()
        self.wh.save_dir = self.test_dir

        self.clear_test_data()

    def clear_test_data(self):
        for fl in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, fl))

    def test_create_a_workflow(self):
        project = Project(name='Testing Project')
        process = Process(name='Testing Process', project_uid=project.uid)

        workflow = Workflow(name='Testing Workflow', project_uid=project.uid,
            process_uids=[process.uid], process_type=ProcessType.LINEAR)

        self.wh.create(workflow=workflow)

        self.wh.load()
        self.assertEqual(len(self.wh.workflows), 1)

    def test_filter_workflows(self):
        project = Project(name='Testing Project')
        process = Process(name='Testing', project_uid=project.uid)

        workflow1 = Workflow(name='Testing', project_uid=project.uid,
            process_uids=[process.uid], process_type=ProcessType.LINEAR)
        workflow2 = Workflow(name='Testing2', project_uid=project.uid,
            process_uids=[process.uid], process_type=ProcessType.PARALLEL)
        workflow3 = Workflow(name='Testing3', project_uid=project.uid,
            process_uids=[process.uid], process_type=ProcessType.WEB,  active=False)
        self.wh.create(workflow=workflow1)
        self.wh.create(workflow=workflow2)
        self.wh.create(workflow=workflow3)

        filter1 = WorkflowFilter(name=['Testing'])
        filtered_results1 = self.wh.filter(workflow_filter=filter1)
        self.assertEqual(len(filtered_results1), 1)

        filter2 = WorkflowFilter(name=['Testing', 'Testing2'])
        filtered_results2 = self.wh.filter(workflow_filter=filter2)
        self.assertEqual(len(filtered_results2), 2)

        filter3 = WorkflowFilter(active=True)
        filtered_results3 = self.wh.filter(workflow_filter=filter3)
        self.assertEqual(len(filtered_results3), 2)

    def test_modify_a_workflow(self):
        project = Project(name='Testing Project')
        process = Process(name='Testing', project_uid=project.uid)

        workflow1 = Workflow(name='Testing', project_uid=project.uid,
            process_uids=[process.uid], process_type=ProcessType.LINEAR)
        workflow2 = Workflow(name='Testing2', project_uid=project.uid,
            process_uids=[process.uid], process_type=ProcessType.PARALLEL)
        workflow3 = Workflow(name='Testing3', project_uid=project.uid,
            process_uids=[process.uid], process_type=ProcessType.WEB,  active=False)
        self.wh.create(workflow=workflow1)
        self.wh.create(workflow=workflow2)
        self.wh.create(workflow=workflow3)

        filter1 = WorkflowFilter(name=['Testing2'])
        updated_process = self.wh.filter(workflow_filter=filter1)[0]
        updated_process.name = 'Renamed'
        self.wh.update(workflow=updated_process)

        filter2 = WorkflowFilter()
        updated_process = self.wh.filter(workflow_filter=filter2)
        self.assertEqual(len(updated_process), 3)
        self.assertEqual(updated_process[1].name, 'Renamed')

    def test_delete_a_workflow(self):
        project = Project(name='Testing Project')
        process = Process(name='Testing', project_uid=project.uid)

        workflow1 = Workflow(name='Testing', project_uid=project.uid,
            process_uids=[process.uid], process_type=ProcessType.LINEAR)
        workflow2 = Workflow(name='Testing2', project_uid=project.uid,
            process_uids=[process.uid], process_type=ProcessType.PARALLEL)
        workflow3 = Workflow(name='Testing3', project_uid=project.uid,
            process_uids=[process.uid], process_type=ProcessType.WEB,  active=False)
        self.wh.create(workflow=workflow1)
        self.wh.create(workflow=workflow2)
        self.wh.create(workflow=workflow3)

        filter1 = WorkflowFilter(name=['Testing2'])
        updated_process = self.wh.filter(workflow_filter=filter1)[0]
        self.wh.delete(workflow=updated_process)

        filter2 = WorkflowFilter()
        updated_process = self.wh.filter(workflow_filter=filter2)
        self.assertEqual(len(updated_process), 2)
