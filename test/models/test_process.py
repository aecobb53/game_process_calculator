import json
import re
import os

from unittest import TestCase
from unittest.mock import MagicMock, call
from .. import MyTestCase

import sys
sys.path.append('/home/acobb/git/game_process_calculator/game_process_calculator')
from game_process_calculator import Project, Resource, Process


class ProcessTest(MyTestCase):
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
            consume_uids={resource.uid: 1},
            produce_uids={resource.uid: 1},
        )
        validation = {
            "id": None,
            "description": None,
            "notes": None,
            "name": "test",
            "project_uid": project.uid,
            "active": True,
            "deleted": False,
            "consume_uids": {
                resource.uid: 1.0
            },
            "produce_uids": {
                resource.uid: 1.0
            },
            "process_time_seconds": None,
            "rest_time_seconds": None
        }
        actual = process.put()
        validation['uid'] = actual['uid']
        validation['creation_datetime'] = actual['creation_datetime']
        validation['update_datetime'] = actual['update_datetime']
        # print(json.dumps(validation, indent=4))
        self.assertEqual(actual, validation)
        resource2 = Process.build(actual)
        self.assertEqual(resource2.put(), validation)

    # def test_properties(self):
    #     project = Project(
    #         name='test',
    #     )
    #     resource_value = Resource(
    #         name='Value Material',
    #         project_uid=project.uid,
    #     )
    #     consumes_resource_1 = Resource(
    #         name='Consumed Resource',
    #         project_uid=project.uid,
    #         value_obj_uid=resource_value.uid,
    #         value_amount=5,
    #     )
    #     consumes_resource_2 = Resource(
    #         name='Consumed Resource',
    #         project_uid=project.uid,
    #         value_obj_uid=resource_value.uid,
    #         value_amount=1,
    #     )
    #     produces_resource_1 = Resource(
    #         name='Produces Resource',
    #         project_uid=project.uid,
    #         value_obj_uid=resource_value.uid,
    #         value_amount=100,
    #     )
    #     produces_resource_2 = Resource(
    #         name='Produces Resource',
    #         project_uid=project.uid,
    #         value_obj_uid=resource_value.uid,
    #         value_amount=0.5,
    #     )
    #     process = Process(
    #         name='test',
    #         consume_uids={
    #             consumes_resource_1.uid: 5,
    #             consumes_resource_2.uid: 10,
    #         },
    #         produce_uids={
    #             produces_resource_1.uid: 1,
    #             produces_resource_2.uid: 1.5,
    #         },
    #     )
    #     validation = {
    #         "id": None,
    #         "description": None,
    #         "notes": None,
    #         "name": "test",
    #         "active": True,
    #         "consume_uids": {
    #             consumes_resource_1.uid: 5,
    #             consumes_resource_2.uid: 10,
    #         },
    #         "produce_uids": {
    #             produces_resource_1.uid: 1,
    #             produces_resource_2.uid: 1.5,
    #         },
    #         "process_time_seconds": None,
    #         "rest_time_seconds": None
    #     }
    #     print(json.dumps(process.put(), indent=4))
    #     actual = process.put()
    #     validation['uid'] = actual['uid']
    #     validation['creation_datetime'] = actual['creation_datetime']
    #     validation['update_datetime'] = actual['update_datetime']
    #     # print(json.dumps(validation, indent=4))
    #     self.assertEqual(actual, validation)
    #     resource2 = Process.build(actual)
    #     self.assertEqual(resource2.put(), validation)
    #     print('copnsumes')
    #     print(process.consumes)
    #     self.assertEqual(process.consumes, [
    #         consumes_resource_1,
    #         consumes_resource_2,
    #     ])
    #     print('produces')
    #     print(process.produces)
    #     self.assertEqual(process.produces, [
    #         produces_resource_1,
    #         produces_resource_2,
    #     ])
    #     print('process_cost')
    #     print(process.process_cost)
    #     self.assertEqual(process.process_cost, 1)
