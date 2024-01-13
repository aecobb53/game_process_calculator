import json
import re
import os

from unittest import TestCase
from unittest.mock import MagicMock, call
from .. import MyTestCase

import sys
sys.path.append('/home/acobb/git/game_process_calculator/game_process_calculator')
from game_process_calculator import Project, Resource


class ResourceTest(MyTestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_create_obj(self):
        project = Project(
            name='test',
        )
        resource = Resource(
            name='test',
            project_uid=project.uid,
        )
        validation = {
            "id": None,
            "description": None,
            "notes": None,
            "name": "test",
            "project_uid": project.uid,
            "active": True,
            "deleted": False,
            "acquisition_uids": None,
            "desposal_uids": None,
            "value_obj_uid": None,
            "value_amount": None
        }
        actual = resource.put()
        validation['uid'] = actual['uid']
        validation['creation_datetime'] = actual['creation_datetime']
        validation['update_datetime'] = actual['update_datetime']
        self.assertEqual(actual, validation)
        resource2 = Resource.build(actual)
        print(json.dumps(resource2.put(), indent=4))
        self.assertEqual(resource2.put(), validation)

    def test_simple_properties(self):
        project = Project(
            name='test',
        )
        resource_acquisition = Resource(
            name='Acquisition Material',
            project_uid=project.uid,
        )
        resource_desposal = Resource(
            name='Desposal Material',
            project_uid=project.uid,
        )
        resource_value = Resource(
            name='Value Material',
            project_uid=project.uid,
        )
        resource = Resource(
            name='test',
            project_uid=project.uid,
            acquisition_uids=[resource_acquisition.uid],
            desposal_uids=[resource_desposal.uid],
            value_obj_uid=resource_value.uid,
            value_amount=1.5
        )
        validation = {
            "id": None,
            "description": None,
            "notes": None,
            "name": "test",
            "deleted": False,
            "project_uid": project.uid,
            "active": True,
            "acquisition_uids": [resource_acquisition.uid],
            "desposal_uids": [resource_desposal.uid],
            "value_obj_uid": resource_value.uid,
            "value_amount": 1.5
        }
        actual = resource.put()
        validation['uid'] = actual['uid']
        validation['creation_datetime'] = actual['creation_datetime']
        validation['update_datetime'] = actual['update_datetime']
        self.assertEqual(actual, validation)
        resource2 = Resource.build(actual)
        self.assertEqual(resource2.put(), validation)
