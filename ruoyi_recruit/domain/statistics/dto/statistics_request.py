from typing import Optional, Annotated, List

from pydantic import Field

from ruoyi_common.base.model import BaseEntity
from ruoyi_common.base.schema_excel import ExcelField
from ruoyi_common.base.schema_vo import VoField


class StatisticsRequest(BaseEntity):
    #地区
    address: Annotated[
        Optional[str],
        Field(default=None, description="地区"),
        VoField(query=True),
        ExcelField(name="地区")
    ]
    #岗位
    postType: Annotated[
        Optional[str],
        Field(default=None, description="岗位"),
        VoField(query=True),
        ExcelField(name="岗位")
    ]
