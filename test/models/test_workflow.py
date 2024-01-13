import json
import re
import os

from unittest import TestCase
from unittest.mock import MagicMock, call

from .. import MyTestCase

import sys
sys.path.append('/home/acobb/git/game_process_calculator/game_process_calculator')
from game_process_calculator import Project, Resource, Process, Workflow, ProcessType


class WorkflowTest(MyTestCase):
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
        process = Process(
            name='test',
            project_uid=project.uid,
            consume_ids={resource.uid: 1},
            produce_ids={resource.uid: 1},
        )
        workflow = Workflow(
            name='test',
            project_uid=project.uid,
            process_uids=[process.uid],
            process_type=ProcessType.LINEAR,
        )
        validation = {
            "id": None,
            "uid": "f1fb2f69-131a-477e-8b32-00738872b621",
            "creation_datetime": "2024-01-05T22:12:31.218130Z",
            "update_datetime": "2024-01-05T22:12:31.218134Z",
            "description": None,
            "notes": None,
            "name": "test",
            "project_uid": project.uid,
            "active": True,
            "deleted": False,
            "process_uids": [
                process.uid
            ],
            "process_type": "LINEAR"
        }
        print(json.dumps(workflow.put(), indent=4))
        actual = workflow.put()
        validation['uid'] = actual['uid']
        validation['creation_datetime'] = actual['creation_datetime']
        validation['update_datetime'] = actual['update_datetime']
        # print(json.dumps(validation, indent=4))
        self.assertEqual(actual, validation)
        resource2 = Workflow.build(actual)
        self.assertEqual(resource2.put(), validation)
