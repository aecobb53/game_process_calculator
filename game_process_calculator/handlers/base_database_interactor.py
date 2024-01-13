import json
import re
import os
import uuid
import requests

from pydantic import BaseModel
from enum import Enum
from typing import List, Optional, Dict, Union
from datetime import date, datetime, timedelta
from uuid import uuid4


class BaseDatabaseInteractor(BaseModel):
    id: Optional[int] = None
    uid: Optional[str] = None
    creation_datetime: Optional[datetime] = None
    update_datetime: Optional[datetime] = None
    description: Optional[str] = None
    notes: Optional[List[str]] = None
    name: Optional[str] = None

    save_dir: Optional[str] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.uid is None:
            self.uid = str(uuid4())
        if self.creation_datetime is None:
            self.creation_datetime = datetime.utcnow()
        if self.update_datetime is None:
            self.update_datetime = datetime.utcnow()
        self.save_dir = os.path.join(os.path.dirname(os.getcwd()), 'data')


    def save_file(self, path: str, content: Dict):
        with open(path, 'w') as f:
            json.dump(content, f, indent=4)

    def load_file(cls, path):
        with open(path, 'r') as jf:
            content = json.load(jf)
        return content
