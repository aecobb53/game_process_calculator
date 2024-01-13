import json
import re
import os
import requests

from copy import deepcopy
from typing import List, Optional, Dict, Union

from handlers import BaseDatabaseInteractor
from models import Project, ProjectFilter


class ProjectHandler(BaseDatabaseInteractor):
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

    def update(self, project: Project) -> None:
        updated_project = self.filter(project_filter=ProjectFilter(uid=[project.uid]))[0]
        updated_project.update(project)
        self.projects[updated_project.id] = updated_project
        self.save()
        return deepcopy(project)

    def delete(self, project: Project) -> None:
        project.deleted = True
        self.update(project=project)
