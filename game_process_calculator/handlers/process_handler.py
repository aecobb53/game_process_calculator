import json
import re
import os
import requests

from copy import deepcopy
from typing import List, Optional, Dict, Union

# from handlers import BaseDatabaseInteractor
from handlers import BaseHandler
from models import Process, ProcessFilter


class ProcessHandler(BaseHandler):
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
        new_process = Process.build(process.put())
        new_process.id = len(processes)
        processes.append(new_process)
        self.save()
        return new_process

    def filter(self, process_filter: ProcessFilter) -> List[Process]:
        processes = self.processes
        processes = process_filter.filter_results(processes)
        return processes

    def update(self, process: Process) -> Process:
        processes = self.filter(ProcessFilter(uid=[process.uid]))

        if len(processes) == 0:
            raise IndexError(f"Process with uid {process.uid} not found")
        elif len(processes) > 1:
            raise IndexError(f"Process with uid {process.uid} returns multiple results")

        updated_process = self.filter(process_filter=ProcessFilter(uid=[process.uid]))[0]
        updated_process.update(process)
        self.processes[updated_process.id] = updated_process
        self.save()
        return deepcopy(process)

    def delete(self, process_uid: int) -> Process:
        processes = self.filter(ProcessFilter(uid=[process_uid]))

        if len(processes) == 0:
            raise IndexError(f"Process with uid {process_uid} not found")
        elif len(processes) > 1:
            raise IndexError(f"Process with uid {process_uid} returns multiple results")

        delete_process = self.filter(process_filter=ProcessFilter(uid=[process_uid]))[0]
        delete_process.delete()
        self.processes[delete_process.id] = delete_process
        self.save()
        return deepcopy(delete_process)

    def export_processes(self) -> Dict:
        processes = self.filter(ProcessFilter())
        return {'processes': [p.put() for p in processes]}

    def import_processes(self, dct) -> List[Process]:
        self._processes = []
        processes = self.processes
        output = []
        print(json.dumps(dct, indent=4))
        for process_dct in dct['processes']:
            process = Process.build(process_dct)
            output.append(process)
            processes.append(process)

        self.save()
        return output
