import json
import re
import os

from unittest import TestCase
from unittest.mock import MagicMock, call

from .. import MyTestCase

import sys
sys.path.append('/home/acobb/git/game_process_calculator/game_process_calculator')
from game_process_calculator import Project, Resource, ProcessFilter, Process, ProcessFilter
from game_process_calculator import ProjectHandler, ResourceHandler, ProcessHandler


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

        self.clear_test_data()

    def clear_test_data(self):
        for fl in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, fl))

    def test_create_a_process(self):
        project = Project(name='Testing Project')
        consume_resource = Resource(name='Consume Testing', project_uid=project.uid)
        produce_resource = Resource(name='Consume Testing', project_uid=project.uid)

        process = Process(name='Testing', project_uid=project.uid,
            consume_uids={consume_resource.uid: 1.5}, produce_uids={produce_resource.uid: 1})
        self.proc_h.create(process=process)

        self.proc_h.load()
        self.assertEqual(len(self.proc_h.processes), 1)

    def test_filter_processes(self):
        project = Project(name='Testing Project')

        acquisition_resource = Resource(name='Acquisition Resource', project_uid=project.uid)
        desposal_resource = Resource(name='Desposal Resource', project_uid=project.uid)
        value_resource = Resource(name='Value Resource', project_uid=project.uid)

        consume_resource = Resource(name='Consume Testing', project_uid=project.uid)
        produce_resource = Resource(name='Produce Testing', project_uid=project.uid,
            acquisition_uids=[acquisition_resource.uid], desposal_uids=[desposal_resource.uid],
            value_obj_uid=value_resource.uid, value_amount=5)
        self.rh.create(resource=consume_resource)
        self.rh.create(resource=produce_resource)

        process1 = Process(name='Testing', project_uid=project.uid,
            consume_uids={consume_resource.uid: 1.5}, produce_uids={produce_resource.uid: 1})
        process2 = Process(name='Testing2', project_uid=project.uid)
        process3 = Process(name='Testing3', project_uid=project.uid, active=False)
        self.proc_h.create(process=process1)
        self.proc_h.create(process=process2)
        self.proc_h.create(process=process3)

        filter1 = ProcessFilter(name=['Testing'])
        filtered_results1 = self.proc_h.filter(process_filter=filter1)
        self.assertEqual(len(filtered_results1), 1)

        filter2 = ProcessFilter(name=['Testing', 'Testing2'])
        filtered_results2 = self.proc_h.filter(process_filter=filter2)
        self.assertEqual(len(filtered_results2), 2)

        filter3 = ProcessFilter(active=True)
        filtered_results3 = self.proc_h.filter(process_filter=filter3)
        self.assertEqual(len(filtered_results3), 2)

    def test_modify_a_process(self):
        project = Project(name='Testing Project')
        self.proj_h.create(project=project)

        acquisition_resource = Resource(name='Acquisition Resource', project_uid=project.uid)
        desposal_resource = Resource(name='Desposal Resource', project_uid=project.uid)
        value_resource = Resource(name='Value Resource', project_uid=project.uid)

        consume_resource = Resource(name='Consume Testing', project_uid=project.uid)
        produce_resource = Resource(name='Produce Testing', project_uid=project.uid,
            acquisition_uids=[acquisition_resource.uid], desposal_uids=[desposal_resource.uid],
            value_obj_uid=value_resource.uid, value_amount=5)
        self.rh.create(resource=consume_resource)
        self.rh.create(resource=produce_resource)

        process1 = Process(name='Testing', project_uid=project.uid,
            consume_uids={consume_resource.uid: 1.5}, produce_uids={produce_resource.uid: 1})
        process2 = Process(name='Testing2', project_uid=project.uid)
        process3 = Process(name='Testing3', project_uid=project.uid)
        self.proc_h.create(process=process1)
        self.proc_h.create(process=process2)
        self.proc_h.create(process=process3)

        filter1 = ProcessFilter(name=['Testing2'])
        updated_process = self.proc_h.filter(process_filter=filter1)[0]
        updated_process.name = 'Renamed'
        self.proc_h.update(process=updated_process)

        filter2 = ProcessFilter()
        updated_process = self.proc_h.filter(process_filter=filter2)
        self.assertEqual(len(updated_process), 3)
        self.assertEqual(updated_process[1].name, 'Renamed')

    def test_delete_a_process(self):
        project = Project(name='Testing Project')
        self.proj_h.create(project=project)

        acquisition_resource = Resource(name='Acquisition Resource', project_uid=project.uid)
        desposal_resource = Resource(name='Desposal Resource', project_uid=project.uid)
        value_resource = Resource(name='Value Resource', project_uid=project.uid)

        consume_resource = Resource(name='Consume Testing', project_uid=project.uid)
        produce_resource = Resource(name='Produce Testing', project_uid=project.uid,
            acquisition_uids=[acquisition_resource.uid], desposal_uids=[desposal_resource.uid],
            value_obj_uid=value_resource.uid, value_amount=5)
        self.rh.create(resource=consume_resource)
        self.rh.create(resource=produce_resource)

        process1 = Process(name='Testing', project_uid=project.uid,
            consume_uids={consume_resource.uid: 1.5}, produce_uids={produce_resource.uid: 1})
        process2 = Process(name='Testing2', project_uid=project.uid)
        process3 = Process(name='Testing3', project_uid=project.uid)
        self.proc_h.create(process=process1)
        self.proc_h.create(process=process2)
        self.proc_h.create(process=process3)

        filter1 = ProcessFilter(name=['Testing2'])
        delete_process = self.proc_h.filter(process_filter=filter1)[0]
        self.proc_h.delete(process=delete_process)

        filter2 = ProcessFilter()
        updated_process = self.proc_h.filter(process_filter=filter2)
        self.assertEqual(len(updated_process), 2)
