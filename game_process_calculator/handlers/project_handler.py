from ast import Index
import json
import re
import os
import requests

from copy import deepcopy
from typing import List, Optional, Dict, Union

# from handlers import BaseDatabaseInteractor
from handlers import BaseHandler
from models import Project, ProjectFilter


class ProjectHandler(BaseHandler):
    save_filename: Optional[str] = None
    _projects: Optional[List[Project]] = None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.save_filename = 'projects.json'
        self._projects = None

    @property
    def projects(self) -> List[Project]:
        if self._projects is None:
            self.load()
        return self._projects

    @property
    def save_file_path(self) -> str:
        return os.path.join(self.save_dir, self.save_filename)

    def load(self) -> None:
        if os.path.exists(self.save_file_path):
            data = [Project.build(p) for p in self.load_file(self.save_file_path)]
        else:
            data = []
        self._projects = data

    def save(self) -> None:
        os.makedirs(self.save_dir, exist_ok=True)
        content = [p.put() for p in self.projects]
        self.save_file(self.save_file_path, content)

    def create(self, project: Project) -> Project:
        projects = self.projects
        new_project = Project.build(project.put())
        new_project.id = len(projects)
        projects.append(new_project)
        self.save()
        return new_project

    def filter(self, project_filter: ProjectFilter) -> List[Project]:
        projects = self.projects
        projects = project_filter.filter_results(projects)
        return projects

    def update(self, saved_project: Project, project: Project) -> Project:
        saved_project.update(project)
        self.projects[saved_project.id] = saved_project
        self.save()
        return deepcopy(project)

    def delete(self, project: Project) -> Project:
        project.delete()
        self.projects[project.id] = project
        self.save()
        return deepcopy(project)

    def export_projects(self) -> Dict:
        projects = self.filter(ProjectFilter())
        return {'projects': [p.put() for p in projects]}

    def import_projects(self, dct) -> List[Project]:
        self._projects = []
        projects = self.projects
        output = []
        for project_dct in dct['projects']:
            project = Project.build(project_dct)
            output.append(project)
            projects.append(project)
        self.save()
        return output
