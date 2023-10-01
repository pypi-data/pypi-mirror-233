from __future__ import annotations

import pydantic as pydantic_v2
import pydantic.v1 as pydantic_v1
from pydantic_core import PydanticUndefined


def v2_field_to_v1(field: pydantic_v2.fields.FieldInfo) -> pydantic_v1.fields.FieldInfo:
    kwargs = {"alias": field.alias}
    if field.default is not PydanticUndefined:
        kwargs["default"] = field.default
    return pydantic_v1.Field(**kwargs)


def v2_model_to_v1(model: type[pydantic_v2.BaseModel]) -> type[pydantic_v1.BaseModel]:
    return pydantic_v1.create_model(
        model.__name__,
        **{
            f_name: (field.annotation, v2_field_to_v1(field))
            for f_name, field in model.model_fields.items()
        }
    )


def render_model(model: type[pydantic_v1.BaseModel], data, **kwargs) -> dict:
    if not isinstance(data, model):
        data = model.parse_obj(data)
    return data.dict(**kwargs)


def kebabify_model(model: type[pydantic_v1.BaseModel]):
    for f_name, field in model.__fields__.items():
        if field.alias == f_name:
            field.alias = field.name.replace("_", "-")
