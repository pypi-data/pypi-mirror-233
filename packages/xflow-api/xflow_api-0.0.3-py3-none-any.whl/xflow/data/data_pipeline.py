from xflow._flow.component import Component, ComponentTypeCode
from xflow._flow.pipeline import Pipeline


def create_component(name: str, func: callable, description: str = '') -> Component:
    return Component(name=name,
                     func=func,
                     desc=description,
                     component_type=ComponentTypeCode.DATA)


def create_pipeline() -> Pipeline:
    pass
