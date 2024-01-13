import json
import re
import os

from unittest import TestCase
from unittest.mock import MagicMock, call

from .. import MyTestCase

import sys
sys.path.append('/home/acobb/git/game_process_calculator/game_process_calculator')
from game_process_calculator import Project, ProjectFilter
from game_process_calculator import ProjectHandler


class ProjectTest(MyTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.test_dir = os.path.join(os.getcwd(), 'test', 'test_data')
        self.ph = ProjectHandler()
        self.ph.save_dir = self.test_dir

        self.clear_test_data()

    def clear_test_data(self):
        for fl in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, fl))

    def test_create_a_project(self):
        project = Project(name='Testing')
        self.ph.create(project=project)
        self.ph.load()
        self.assertEqual(len(self.ph.projects), 1)

    def test_filter_projects(self):
        project1 = Project(name='Testing')
        project2 = Project(name='Testing2')
        project3 = Project(name='Testing3', active=False)
        self.ph.create(project=project1)
        self.ph.create(project=project2)
        self.ph.create(project=project3)

        filter1 = ProjectFilter(name=['Testing'])
        filtered_results1 = self.ph.filter(project_filter=filter1)
        self.assertEqual(len(filtered_results1), 1)

        filter2 = ProjectFilter(name=['Testing', 'Testing2'])
        filtered_results2 = self.ph.filter(project_filter=filter2)
        self.assertEqual(len(filtered_results2), 2)

        filter3 = ProjectFilter(active=True)
        filtered_results3 = self.ph.filter(project_filter=filter3)
        self.assertEqual(len(filtered_results3), 2)

    def test_modify_a_project(self):
        project1 = Project(name='Testing')
        project2 = Project(name='Testing2')
        project3 = Project(name='Testing3', active=False)
        self.ph.create(project=project1)
        self.ph.create(project=project2)
        self.ph.create(project=project3)
        filter1 = ProjectFilter(name=['Testing2'])
        updated_project = self.ph.filter(project_filter=filter1)[0]
        updated_project.name = 'Renamed'
        self.ph.update(project=updated_project)

        filter2 = ProjectFilter()
        updated_projects = self.ph.filter(project_filter=filter2)
        self.assertEqual(len(updated_projects), 3)
        self.assertEqual(updated_projects[1].name, 'Renamed')

    def test_delete_a_project(self):
        project1 = Project(name='Testing')
        project2 = Project(name='Testing2')
        project3 = Project(name='Testing3', active=False)
        self.ph.create(project=project1)
        self.ph.create(project=project2)
        self.ph.create(project=project3)
        self.ph.delete(project=project2)

        filter2 = ProjectFilter()
        updated_projects = self.ph.filter(project_filter=filter2)
        self.assertEqual(len(updated_projects), 2)
