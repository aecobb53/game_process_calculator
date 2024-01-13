import json
import re
import os
import requests

from typing import List, Optional, Dict, Union

from handlers import BaseDatabaseInteractor
from models import Process, ProcessFilter


class ProcessHandler(BaseDatabaseInteractor):
    save_filename: Optional[str] = None
    _processes: Optional[List[Process]] = None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.save_filename = 'processes.json'
        self._processes = None

    @property
    def processes(self) -> List[Process]:
        if self._processes is None:
            self.load()
        return self._processes

    @property
    def save_file_path(self) -> str:
        return os.path.join(self.save_dir, self.save_filename)

    def load(self) -> None:
        if os.path.exists(self.save_file_path):
            data = [Process.build(p) for p in self.load_file(self.save_file_path)]
        else:
            data = []
        self._processes = data

    def save(self) -> None:
        os.makedirs(self.save_dir, exist_ok=True)
        content = [p.put() for p in self.processes]
        self.save_file(self.save_file_path, content)

    def create(self, process: Process) -> Process:
        processes = self.processes
        process.id = len(processes)
        processes.append(process)
        self.save()
        return process

    def filter(self, process_filter: ProcessFilter) -> List[Process]:
        processes = self.processes
        processes = process_filter.filter_results(processes)
        return processes

    def update(self, process: Process) -> None:
        old_process = self.filter(process_filter=ProcessFilter(uid=[process.uid]))[0]
        self.processes[old_process.id] = process
        self.save()

    def delete(self, process: Process) -> None:
        process.deleted = True
        self.update(process=process)
