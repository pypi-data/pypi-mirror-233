import sys
import os
import requests
import traceback

from pydantic import BaseModel, Extra

this = sys.modules[__name__]

# os.environ["SERVICE_DISCOVERY"] = "http://host.docker.internal:9000"
# os.environ["SERVICE_DISCOVERY"] = "https://localhost:9000"
# os.environ["PROJECT_ID"] = "test-project"
# os.environ["USER"] = "test-user"


class ClientInformation(BaseModel):
    xflow_server_url: str
    user: str
    project_id: str
    is_init: bool = False
    component_path: str = "/api/component"
    pipeline_path: str = "/api/pipeline"

    class Config:
        extra = Extra.forbid


def init():
    try:
        if this.client_info.is_init:
            print("xflow client is already inited")
            return
    except AttributeError:
        xflow_server_url = ''
        service_discovery_url = os.getenv("SERVICE_DISCOVERY") + "/api/service?name=xflow"
        print(service_discovery_url)
        res = requests.get(url=service_discovery_url, verify=False)
        print(res)
        if res.status_code == 200:
            code = res.json().get("CODE")
            if code == "00":
                xflow_server_url = res.json().get("URL")
        if xflow_server_url == '':
            raise InitError("can't find xflow server")
        this.client_info = ClientInformation(xflow_server_url=xflow_server_url,
                                             user=os.getenv("USER_ID"),
                                             project_id=os.getenv("PROJECT_ID"),
                                             is_init=True)
    except Exception as exc:
        print(exc.__str__())


class InitError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.traceback = traceback.format_exc()


def init_check() -> None:
    if hasattr(this, "client_info"):
        if not this.client_info.is_init:
            raise RuntimeError("xflow didn't initiated. call xflow.init() before using xflow")
    else:
        raise RuntimeError("xflow didn't initiated. call xflow.init() before using xflow")
