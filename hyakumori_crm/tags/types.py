from typing import List

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


class AssignTagInput(BaseModel):
    object_id: str
    delete: List[AssignTagItem] = []
    add: List[AssignTagItem] = []
