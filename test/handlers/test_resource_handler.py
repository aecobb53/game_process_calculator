import json
import re
import os

from unittest import TestCase
from unittest.mock import MagicMock, call

from .. import MyTestCase

import sys
sys.path.append('/home/acobb/git/game_process_calculator/game_process_calculator')
from game_process_calculator import Project, Resource, ResourceFilter
from game_process_calculator import ProjectHandler, ResourceHandler


class ResourceTest(MyTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.test_dir = os.path.join(os.getcwd(), 'test', 'test_data')
        self.ph = ProjectHandler()
        self.ph.save_dir = self.test_dir
        self.rh = ResourceHandler()
        self.rh.save_dir = self.test_dir

        self.clear_test_data()

    def clear_test_data(self):
        for fl in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, fl))

    def test_create_a_resource(self):
        project = Project(name='Testing Project')
        resource = Resource(name='Testing', project_uid=project.uid)

        self.rh.create(resource=resource)
        self.rh.load()
        self.assertEqual(len(self.rh.resources), 1)

    def test_filter_resources(self):
        project1 = Project(name='Testing Project')
        project2 = Project(name='Testing Project2')
        project3 = Project(name='Testing Project2', active=False)

        acquisition_resource = Resource(name='Acquisition Resource', project_uid=project1.uid)
        desposal_resource = Resource(name='Desposal Resource', project_uid=project1.uid)
        value_resource = Resource(name='Value Resource', project_uid=project1.uid)
        self.rh.create(resource=acquisition_resource)
        self.rh.create(resource=desposal_resource)
        self.rh.create(resource=value_resource)

        resource1 = Resource(name='Testing', project_uid=project1.uid, value_obj_uid=value_resource.uid, value_amount=10)
        resource2 = Resource(name='Testing2', project_uid=project1.uid,
            acquisition_uids=[acquisition_resource.uid], desposal_uids=[desposal_resource.uid],
            value_obj_uid=value_resource.uid, value_amount=5)
        resource3 = Resource(name='Testing3', project_uid=project2.uid, active=False)
        resource4 = Resource(name='Testing4', project_uid=project3.uid)
        self.rh.create(resource=resource1)
        self.rh.create(resource=resource2)
        self.rh.create(resource=resource3)
        self.rh.create(resource=resource4)

        filter1 = ResourceFilter(name=['Testing'])
        filtered_results1 = self.rh.filter(resource_filter=filter1)
        self.assertEqual(len(filtered_results1), 1)

        filter2 = ResourceFilter(name=['Testing', 'Testing2'])
        filtered_results2 = self.rh.filter(resource_filter=filter2)
        self.assertEqual(len(filtered_results2), 2)

        filter3 = ResourceFilter(project_uid=[project1.uid])
        filtered_results3 = self.rh.filter(resource_filter=filter3)
        self.assertEqual(len(filtered_results3), 5)

        filter4 = ResourceFilter(acquisition_uids=[acquisition_resource.uid])
        filtered_results4 = self.rh.filter(resource_filter=filter4)
        self.assertEqual(len(filtered_results4), 1)

        filter5 = ResourceFilter(value_obj_uid=value_resource.uid)
        filtered_results5 = self.rh.filter(resource_filter=filter5)
        self.assertEqual(len(filtered_results5), 2)

        filter6 = ResourceFilter(active=True)
        filtered_results6 = self.rh.filter(resource_filter=filter6)
        self.assertEqual(len(filtered_results6), 6)

    def test_modify_a_resource(self):
        project1 = Project(name='Testing Project')

        acquisition_resource = Resource(name='Acquisition Resource', project_uid=project1.uid)
        desposal_resource = Resource(name='Desposal Resource', project_uid=project1.uid)
        value_resource = Resource(name='Value Resource', project_uid=project1.uid)
        self.rh.create(resource=acquisition_resource)
        self.rh.create(resource=desposal_resource)
        self.rh.create(resource=value_resource)

        resource1 = Resource(name='Testing', project_uid=project1.uid, value_obj_uid=value_resource.uid, value_amount=10)
        resource2 = Resource(name='Testing2', project_uid=project1.uid,
            acquisition_uids=[acquisition_resource.uid], desposal_uids=[desposal_resource.uid],
            value_obj_uid=value_resource.uid, value_amount=5)
        self.rh.create(resource=resource1)
        self.rh.create(resource=resource2)

        filter1 = ResourceFilter(name=['Testing'])
        updated_resource = self.rh.filter(resource_filter=filter1)[0]
        updated_resource.name = 'Renamed'
        updated_resource.acquisition_uids = [acquisition_resource.uid]
        self.rh.update(resource=updated_resource)

        filter2 = ResourceFilter()
        updated_resource = self.rh.filter(resource_filter=filter2)
        self.assertEqual(len(updated_resource), 5)
        self.assertEqual(updated_resource[3].name, 'Renamed')
        self.assertEqual(updated_resource[3].acquisition_uids, [acquisition_resource.uid])

    def test_delete_a_resource(self):
        project1 = Project(name='Testing Project')

        acquisition_resource = Resource(name='Acquisition Resource', project_uid=project1.uid)
        desposal_resource = Resource(name='Desposal Resource', project_uid=project1.uid)
        value_resource = Resource(name='Value Resource', project_uid=project1.uid)
        self.rh.create(resource=acquisition_resource)
        self.rh.create(resource=desposal_resource)
        self.rh.create(resource=value_resource)

        resource1 = Resource(name='Testing', project_uid=project1.uid, value_obj_uid=value_resource.uid, value_amount=10)
        resource2 = Resource(name='Testing2', project_uid=project1.uid,
            acquisition_uids=[acquisition_resource.uid], desposal_uids=[desposal_resource.uid],
            value_obj_uid=value_resource.uid, value_amount=5)
        self.rh.create(resource=resource1)
        self.rh.create(resource=resource2)

        filter1 = ResourceFilter(name=['Testing2'])
        delete_resource = self.rh.filter(resource_filter=filter1)[0]
        self.rh.delete(resource=delete_resource)

        filter2 = ResourceFilter()
        updated_resources = self.rh.filter(resource_filter=filter2)
        self.assertEqual(len(updated_resources), 4)
