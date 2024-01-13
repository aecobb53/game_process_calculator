import json
import os
import yaml
import re
from datetime import datetime, timedelta

from pydantic import BaseModel
from enum import Enum
from typing import List, Optional, Dict, Union


class Utils:
    def __init__(self):
        self._verbose = None
        self.time_str_format = '%Y-%m-%dT%H:%M:%S.%fZ'

    def verbose(self, current=None, obj_default=None):
        """
        Returns verbosity in this order:
        | obj_default is set | current set   | result used |
        | ---                | ---           | ---         |
        | False              | False         | current     |
        | False              | True          | current     |
        | True               | False         | obj_default |
        | True               | True          | current     |
        """
        if obj_default is not None:
            self._verbose = obj_default

        if current is None:
            if self._verbose is None:
                self._verbose = 0
            current = self._verbose
        return current

    def _parse_time_str(self, time_s):
        re_datetime = r'^(\d{4})-?(\d{2})?-?(\d{2})?T?(\d{2})?[:-]?(\d{2})?[:-]?(\d{2})?\.?(\d+)?'
        search = re.match(re_datetime, time_s)
        time = []
        for i in range(1,4):
            try:
                group = search.group(i)
                if group is None:
                    raise TypeError
                time.append(group)
            except TypeError:
                time.append('01')
            except IndexError:
                time.append('01')
        for i in range(4,7):
            try:
                group = search.group(i)
                if group is None:
                    raise TypeError
                time.append(group)
            except TypeError:
                time.append('00')
            except IndexError:
                time.append('00')
        try:
            group = search.group(7)[:6]
            time.append(group)
        except TypeError:
            time.append('0')
        except IndexError:
            time.append('0')

        time = '-'.join(time)
        obj = datetime.strptime(time, '%Y-%m-%d-%H-%M-%S-%f')
        return obj

    def time_str_to_obj(self, time_str, allow_none=False):
        if allow_none and time_str is None:
            return None
        if isinstance(time_str, str):
            time_obj = self._parse_time_str(time_str)
        return time_obj

    def time_obj_to_str(self, time_obj, time_format=None, allow_none=False):
        if allow_none and time_obj is None:
            return None
        if not time_format:
            time_format = self.time_str_format
        if isinstance(time_obj, datetime):
            time_str = datetime.strftime(time_obj, time_format)
        return time_str

    def time_parse(self, input_item, allow_none=True):
        if isinstance(input_item, datetime):
            return input_item
        elif isinstance(input_item, str):
            return self.time_str_to_obj(input_item, allow_none=allow_none)
            # try:
            #     return self.time_str_to_obj(input_item, allow_none=allow_none)
            # except:
            #     return TimePhraseInterpreter().parse(input_item)
        else:
            x=1
        x=1

    def time_compare(self, start, end):
        if not isinstance(start, datetime):
            start = self._parse_time_str(start)
        if not isinstance(end, datetime):
            end = self._parse_time_str(end)
        order = start <= end
        diff = end - start
        return order, diff

    def time_obj_to_day_obj(self, time_obj):
        day_obj = datetime(time_obj.year, time_obj.month, time_obj.day)
        return day_obj

    def tunnel_to_item(self, start, match):
        for root, dirs, files in os.walk(start):
            for directory in dirs:
                search = re.match(match, directory)
                if search:
                    return f"{root}/{directory}"
            for fl in files:
                search = re.match(match, fl)
                if search:
                    return f"{root}/{directory}/{fl}"
            return None

    def find_files(self, start, match):
        file_list = []
        for root, dirs, files in os.walk(start):
            for dir in dirs:
                file_list.extend(
                    self.find_files(
                        start=f"{root}/{dir}",
                        match=match
                    )
                )
            for fl in files:
                match_result = re.search(match, fl)
                if match_result:
                    file_list.append(f"{root}/{fl}")
            break
        return file_list

    def convert_headers_to_toc(
        self,
        list_of_headers: List[str],
        spaces=4,
    ):
        for header in list_of_headers:
            if header == '':
                continue
            indent = 0
            while header.startswith('#'):
                header.pop(0)
                indent += 1
            header.strip()

            toc_line = f"{indent * spaces * ' '}- [{header}](#{header.replace(' ', '-').lower()})"
            print(toc_line)

    def convert_to_camel(self, item):
        result = []
        start_of_word = False
        for c in item:
            if c == '_':
                start_of_word = True
                continue
            if start_of_word:
                c = c.upper()
                start_of_word = False
            else:
                c = c.lower()
            result.append(c)
        return ''.join(result)

    def convert_to_pascal(self, item):
        result = []
        start_of_word = True
        for c in item:
            if c == '_':
                start_of_word = True
                continue
            if start_of_word:
                c = c.upper()
                start_of_word = False
            else:
                c = c.lower()
            result.append(c)
        return ''.join(result)

    def convert_to_snake(self, item):
        result = []
        for index, c in enumerate(item):
            if c.isupper() and index != 0:
                c = f"_{c.lower()}"
            else:
                c = c.lower()
            result.append(c)
        return ''.join(result)

    def convert_to_screaming_snake(self, item):
        result = []
        for index, c in enumerate(item):
            if c.isupper() and index != 0:
                c = f"_{c.upper()}"
            else:
                c = c.upper()
            result.append(c)
        return ''.join(result)

    def _super_strip(self, string):
        """
        Strip extra whitespace and quotes if they exist to just return the string
        """
        string = string.strip()
        if string.startswith('"') and string.endswith('"'):
            string = string[1:-1]
        elif string.startswith("'") and string.endswith("'"):
            string = string[1:-1]
        return string

    def str_to_dict(self, dct_str):
        if dct_str.startswith('{') and dct_str.endswith('}'):
            output = {}
            dct_str = dct_str[1:-1]
            pairs = dct_str.split(f',')
            if pairs[-1] == '':
                pairs.pop(-1)
            for pair in pairs:
                item = pair.split(':')
                item = [self._super_strip(i) for i in item]
                if len(item) <= 1:
                    return None
                key = self.str_to_item(item[0])
                value = self.str_to_item(':'.join(item[1:]))
                output[key] = value
            return output
        else:
            return None

    def str_to_list(self, lst_str):
        if lst_str.startswith(('[', '(', '{')) and lst_str.endswith((']', ')', '}')):
            if lst_str.startswith('[') and lst_str.endswith(']'):
                lst_type = 'list'
            elif lst_str.startswith('(') and lst_str.endswith(')'):
                lst_type = 'tuple'
            elif lst_str.startswith('{') and lst_str.endswith('}'):
                lst_type = 'set'
            else:
                return None
            output = []
            lst_str = lst_str[1:-1]
            items = lst_str.split(f',')
            if items[-1] == '':
                items.pop(-1)
            for item in items:
                item = self.str_to_item(item)
                output.append(item)
            if lst_type == 'list':
                return list(output)
            elif lst_type == 'tuple':
                return frozenset(output)
            elif lst_type == 'set':
                return set(output)

    def str_to_item(self, item_str):
        # try:
        #     return complex(item_str)
        # except:
        #     pass
        try:
            return int(item_str)
        except:
            pass
        try:
            return float(item_str)
        except:
            pass

        if item_str in {'True', 'true', 'False', 'false'}:
            if item_str in {'True', 'true'}:
                return True
            elif item_str in {'False', 'false'}:
                return False

        try:
            if item_str.startswith(('b"', "b'")) and item_str.endswith(("'", '"')):
                return item_str[2:-1].encode()
        except:
            pass
        
        # item_str = bytearray(item_str)
        # item_str = memoryview(item_str)
        if item_str in ['None', 'null']:
            return None
        return self._super_strip(item_str)


# list_of_headers = [
#     '### tip-order',
#     '### maxar-tip-submission-gateway lambda',
#     '### seavision-interactor',
#     '### automated-tip-generator',
#     '### maritime-ui',
#     '### maritime-sar-invoke-lambda',
#     '### maritime-sar-handler',
#     '### maritime-tip-proxy',
# ]
# spaces=4
# for header in list_of_headers:
#     indent = 0
#     while header.startswith('#'):
#         header = header[1:]
#         indent += 1
#     header = header.strip()
#     toc_line = f"{indent * spaces * ' '}- [{header}](#{header.replace(' ', '-').lower()})"
#     print(toc_line)
