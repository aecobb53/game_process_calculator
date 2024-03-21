import json
import re
import os

from copy import deepcopy
from enum import Enum
from typing import List, Optional, Dict, Union
from datetime import date, datetime, timedelta
from uuid import uuid4

from utils import Utils
from pydantic import field_validator, FieldValidationInfo, BaseModel


class BalanceWorkflowArgs(BaseModel):
    units_per_second: Optional[List[float]] = None

    @property
    def extract_units_per_second(self):
        if self.units_per_second is not None:
            return max(self.units_per_second)
#     name: Optional[List[str]] = None
#     project_uid: Optional[List[str]] = None
#     process_uids: Optional[List[str]] = None
#     focus_resource_uids: Optional[List[str]] = None

# #     def filter_results(self, results: List[Workflow]):
# #         results = super().filter_results(results)
# #         filtered = []
# #         for result in results:
# #             if self.name is not None:
# #                 if result.name not in self.name:
# #                     continue
# #             if self.project_uid is not None:
# #                 if result.project_uid not in self.project_uid:
# #                     continue
# #             if self.process_uids is not None:
# #                 if result.process_uids is None:
# #                     continue
# #                 if not any([uid in self.process_uids for uid in result.process_uids]):
# #                     continue
# #             if self.focus_resource_uids is not None:
# #                 if result.focus_resource_uids is None:
# #                     continue
# #                 if not any([uid in self.focus_resource_uids for uid in result.focus_resource_uids]):
# #                     continue
# #             filtered.append(deepcopy(result))
# #         return filtered
