# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: like_info.py
# @Time    : 2026-03-02 16:56:43

from typing import Optional, Annotated
from datetime import datetime
from pydantic import Field, BeforeValidator
from ruoyi_common.base.model import BaseEntity
from ruoyi_common.base.transformer import to_datetime, str_to_int
from ruoyi_common.base.schema_excel import ExcelField
from ruoyi_common.base.schema_vo import VoField


class LikeInfo(BaseEntity):
    """
    用户点赞对象
    """
    # 编号
    id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="编号"),
        VoField(query=True),
        ExcelField(name="编号")
    ]
    # 用户
    user_id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="用户"),
        ExcelField(name="用户")
    ]
    # 用户名
    user_name: Annotated[
        Optional[str],
        Field(default=None, description="用户名"),
        VoField(query=True),
        ExcelField(name="用户名")
    ]
    # 岗位大类
    post_type: Annotated[
        Optional[str],
        Field(default=None, description="岗位大类"),
        VoField(query=True),
        ExcelField(name="岗位大类", dict_type="recruit_post_type")
    ]
    # 城市等级
    city_level: Annotated[
        Optional[str],
        Field(default=None, description="城市等级"),
        VoField(query=True),
        ExcelField(name="城市等级", dict_type="recruit_city_level")
    ]
    # 省份
    province: Annotated[
        Optional[str],
        Field(default=None, description="省份"),
        VoField(query=True),
        ExcelField(name="省份")
    ]
    # 城市
    city: Annotated[
        Optional[str],
        Field(default=None, description="城市"),
        VoField(query=True),
        ExcelField(name="城市")
    ]
    # 薪资平均值
    salary_month_avg: Annotated[
        Optional[float],
        Field(default=None, description="薪资平均值"),
        ExcelField(name="薪资平均值")
    ]
    # 经验要求
    experience_required: Annotated[
        Optional[str],
        Field(default=None, description="经验要求"),
        VoField(query=True),
        ExcelField(name="经验要求", dict_type="recruit_experience_required")
    ]
    # 学历要求
    education_required: Annotated[
        Optional[str],
        Field(default=None, description="学历要求"),
        VoField(query=True),
        ExcelField(name="学历要求", dict_type="recruit_education_required")
    ]
    # 主营业务
    main_business: Annotated[
        Optional[str],
        Field(default=None, description="主营业务"),
        VoField(query=True),
        ExcelField(name="主营业务")
    ]
    # 企业规模
    enterprise_size: Annotated[
        Optional[str],
        Field(default=None, description="企业规模"),
        VoField(query=True),
        ExcelField(name="企业规模", dict_type="recruit_enterprise_size")
    ]
    # 融资情况
    financing_situation: Annotated[
        Optional[str],
        Field(default=None, description="融资情况"),
        VoField(query=True),
        ExcelField(name="融资情况", dict_type="recruit_financing_situation")
    ]
    # 分数
    score: Annotated[
        Optional[float],
        Field(default=None, description="分数"),
        ExcelField(name="分数")
    ]
    # 创建时间
    create_time: Annotated[
        Optional[datetime],
        BeforeValidator(to_datetime()),
        Field(default=None, description="创建时间"),
        VoField(query=True),
        ExcelField(name="创建时间")
    ]
    params: Optional[dict] = Field(default=None, description="参数")
    # 页码
    page_num: Optional[int] = Field(default=1, description="页码")
    # 每页数量
    page_size: Optional[int] = Field(default=10, description="每页数量")