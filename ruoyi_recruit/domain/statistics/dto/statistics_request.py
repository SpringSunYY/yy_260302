from typing import Optional, Annotated, List

from pydantic import Field

from ruoyi_common.base.model import BaseEntity
from ruoyi_common.base.schema_excel import ExcelField
from ruoyi_common.base.schema_vo import VoField


class StatisticsRequest(BaseEntity):
    # 地区
    address: Annotated[
        Optional[str],
        Field(default=None, description="地区"),
        VoField(query=True),
        ExcelField(name="地区")
    ]
    # 城市等级
    city_level: Annotated[
        Optional[str],
        Field(default=None, description="城市等级"),
        VoField(query=True),
        ExcelField(name="城市等级")
    ]
    # 岗位
    postType: Annotated[
        Optional[str],
        Field(default=None, description="岗位"),
        VoField(query=True),
        ExcelField(name="岗位")
    ]
    # 学历
    education: Annotated[
        Optional[str],
        Field(default=None, description="学历"),
        VoField(query=True),
        ExcelField(name="学历")
    ]
    # 企业规模
    enterprise_size: Annotated[
        Optional[str],
        Field(default=None, description="企业规模"),
        VoField(query=True),
        ExcelField(name="企业规模")
    ]
    # 经验
    experience: Annotated[
        Optional[str],
        Field(default=None, description="经验"),
        VoField(query=True),
        ExcelField(name="经验")
    ]
    # 主营业务
    main_business: Annotated[
        Optional[str],
        Field(default=None, description="主营业务"),
        VoField(query=True),
        ExcelField(name="主营业务")
    ]
    # 技能
    skill: Annotated[
        Optional[str],
        Field(default=None, description="技能"),
        VoField(query=True),
        ExcelField(name="技能")
    ]
    # 最大工资
    max_salary: Annotated[
        Optional[str],
        Field(default=None, description="最大工资"),
        VoField(query=True),
        ExcelField(name="最大工资")
    ]
    # 最小工资
    min_salary: Annotated[
        Optional[str],
        Field(default=None, description="最小工资"),
        VoField(query=True),
        ExcelField(name="最小工资")
    ]
    # 融资
    financingSituation: Annotated[
        Optional[str],
        Field(default=None, description="融资"),
        VoField(query=True),
        ExcelField(name="融资")
    ]
    # limit
    limit: Annotated[
        Optional[int],
        Field(default=None, description="limit"),
        VoField(query=True),
        ExcelField(name="limit")
    ]
