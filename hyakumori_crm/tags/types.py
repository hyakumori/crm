from typing import List
from uuid import UUID

from pydantic import BaseModel
from pydantic.color import Color


class ColorMapInput(BaseModel):
    value: str
    color: Color


class TagSettingInput(BaseModel):
    id: str = None
    name: str
    code: str
    color_maps: List[ColorMapInput]


class AssignTagItem(BaseModel):
    tag_name: str
    value: str


class TagDeleteInput(BaseModel):
    id: str


class AssignTagInput(BaseModel):
    object_id: str
    tags: List[AssignTagItem] = []


class TagKeyMigrateInput(BaseModel):
    object_ids: List[str]
    from_key: str
    to_key: str
    do_update: bool = False


class TagKeyMigrateAllInput(BaseModel):
    from_key: str
    to_key: str
    do_update: bool = False
