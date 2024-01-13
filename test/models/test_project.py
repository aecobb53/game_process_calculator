import json
import re
import os

from unittest import TestCase
from unittest.mock import MagicMock, call
from .. import MyTestCase

import sys
sys.path.append('/home/acobb/git/game_process_calculator/game_process_calculator')
from game_process_calculator import Project


class ProjectTest(MyTestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_create_obj(self):
        project = Project(
            name='test',
        )
        validation = {
            "id": None,
            "description": None,
            "notes": None,
            "name": "test",
            "active": True,
            "deleted": False,
        }
        actual = project.put()
        validation['uid'] = actual['uid']
        validation['creation_datetime'] = actual['creation_datetime']
        validation['update_datetime'] = actual['update_datetime']
        self.assertEqual(actual, validation)
        project2 = Project.build(actual)
        self.assertEqual(project2.put(), validation)
