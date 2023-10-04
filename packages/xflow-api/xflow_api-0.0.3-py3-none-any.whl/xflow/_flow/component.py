import inspect
import io
from types import GenericAlias
import sys
from io import StringIO, BytesIO
from dataclasses import dataclass
import requests
import json

import dill
from IPython import get_ipython

from xflow._private.request_vo import ExportComponent
import xflow._private.client as xflow_client


@dataclass
class ComponentTypeCode:
    DATA: str = '1'
    EXPERIMENT: str = '2'
COMPONENT_TYPE_CODE = ComponentTypeCode()

class Component:
    def __init__(self, name: str, func: callable, component_type: str,
                 script: str | None = None, desc: str = ''):
        self.__name: str = name
        self.__func: callable = func
        self.__description: str = desc
        if component_type not in COMPONENT_TYPE_CODE.__dict__.values():
            raise AttributeError("undefined component type")
        self.__component_type: str = component_type
        self.__args: dict = get_io_info(func)
        if script is None:
            self.__script: str = get_script(func)
        else:
            self.__script: str = script
        self.__func_obj: bytes = pickled_func(func)

    def __call__(self, *args, **kwargs):
        return self.__func(*args, **kwargs)

    def execute(self, *args, **kwargs):
        return self.__func(*args, **kwargs)

    def export(self):
        xflow_client.init_check()
        client_info: xflow_client.ClientInformation = xflow_client.client_info
        url = client_info.xflow_server_url + client_info.component_path + "/export"
        body = ExportComponent(PRJ_ID=client_info.project_id,
                               REG_ID=client_info.user,
                               CMPNT_NM=self.__name,
                               CMPNT_TYPE_CD=self.__component_type,
                               CMPNT_IN=self.__args["inputs"],
                               CMPNT_OUT=self.__args["outputs"],
                               CMPNT_SCRIPT=self.__script,
                               CMPNT_DESC=self.__description)
        func_obj = {"file": io.BytesIO(self.__func_obj)}
        try:
            response = requests.post(url=url, data={"data": str(json.dumps(body.dict()))}, files=func_obj)
        except requests.exceptions.ConnectionError:
            raise RuntimeError("can't connect to xflow server")
        else:
            if response.status_code == 200:
                print(response.json())
            else:
                raise RuntimeError(f"failed to get data from xflow server: {response.status_code}")


    def update(self):
        pass

    def delete(self):
        pass

    @property
    def args(self):
        return self.__args

    @property
    def name(self):
        return self.__name

    @property
    def script(self):
        return self.__script

    @property
    def description(self):
        return self.__description

    @property
    def func_obj(self):
        return self.__func_obj

    @property
    def component_type(self):
        return self.__component_type


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout


def get_io_info(func: callable) -> dict[str, dict | list]:
    inputs = {}
    outputs = []
    args_info = inspect.get_annotations(func)
    if "return" in args_info:
        output_info = args_info["return"]
        del args_info["return"]
        if output_info.__name__ == tuple.__name__:
            if isinstance(output_info, GenericAlias):
                for arg in output_info.__args__:
                    outputs.append(arg.__name__)
        else:
            outputs.append(output_info.__name__)
    for arg, type_ in args_info.items():
        inputs[arg] = type_.__name__
    io_info = {"inputs": inputs, "outputs": outputs}
    return io_info


def get_script(func: callable) -> str:
    func_string = inspect.getsource(func)
    return func_string
    # ipython = get_ipython()
    # if ipython:
    #     with Capturing() as output:
    #         ipython.run_line_magic("pinfo2", func.__name__)
    #     s_idx = -1
    #     e_idx = -1
    #     for idx, line in enumerate(output):
    #         if "Source" in line:
    #             s_idx = idx + 1
    #         elif "File" in line or "Type" in line:
    #             e_idx = idx - 1
    #     if s_idx != -1 and e_idx != -1:
    #         func_string = '\n'.join(output[s_idx:e_idx])
    #         return func_string
    #     else:
    #         raise SyntaxError("\n".join(output))
    # else:
    #     func_string = inspect.getsource(func)
    #     return func_string


def pickled_func(func: callable) -> bytes:
    return dill.dumps(func)


def restore_func(func_obj: bytes) -> callable:
    return dill.loads(func_obj)
