# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: recruit_info.py
# @Time    : 2026-03-02 16:56:43

from typing import Optional, Annotated
from datetime import datetime
from pydantic import Field, BeforeValidator
from ruoyi_common.base.model import BaseEntity
from ruoyi_common.base.transformer import to_datetime, str_to_int
from ruoyi_common.base.schema_excel import ExcelField
from ruoyi_common.base.schema_vo import VoField


class RecruitInfo(BaseEntity):
    """
    招聘信息对象
    """
    # 编号
    recruit_id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="编号"),
        VoField(query=True),
        ExcelField(name="编号")
    ]
    # 岗位大类
    post_type: Annotated[
        Optional[str],
        Field(default=None, description="岗位大类"),
        VoField(query=True),
        ExcelField(name="岗位大类", dict_type="recruit_post_type")
    ]
    # 岗位
    post: Annotated[
        Optional[str],
        Field(default=None, description="岗位"),
        VoField(query=True),
        ExcelField(name="岗位")
    ]
    # 岗位更新时间
    post_update_time: Annotated[
        Optional[datetime],
        BeforeValidator(to_datetime()),
        Field(default=None, description="岗位更新时间"),
        VoField(query=True),
        ExcelField(name="岗位更新时间")
    ]
    # 标题链接
    title_url: Annotated[
        Optional[str],
        Field(default=None, description="标题链接"),
        ExcelField(name="标题链接")
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
    # 工作地点
    location: Annotated[
        Optional[str],
        Field(default=None, description="工作地点"),
        ExcelField(name="工作地点")
    ]
    # 薪资范围
    salary_range: Annotated[
        Optional[str],
        Field(default=None, description="薪资范围"),
        ExcelField(name="薪资范围")
    ]
    # 薪资下限
    salary_min: Annotated[
        Optional[float],
        Field(default=None, description="薪资下限"),
        ExcelField(name="薪资下限")
    ]
    # 薪资上限
    salary_max: Annotated[
        Optional[float],
        Field(default=None, description="薪资上限"),
        ExcelField(name="薪资上限")
    ]
    # 薪资平均值
    salary_month_avg: Annotated[
        Optional[float],
        Field(default=None, description="薪资平均值"),
        ExcelField(name="薪资平均值")
    ]
    # 薪资备注
    salary_remark: Annotated[
        Optional[str],
        Field(default=None, description="薪资备注"),
        ExcelField(name="薪资备注")
    ]
    # 奖金绩效
    bonus_performance: Annotated[
        Optional[str],
        Field(default=None, description="奖金绩效"),
        ExcelField(name="奖金绩效")
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
    # 技能要求
    skill_required: Annotated[
        Optional[str],
        Field(default=None, description="技能要求"),
        VoField(query=True),
        ExcelField(name="技能要求")
    ]
    # 技能要求1
    skill_required1: Annotated[
        Optional[str],
        Field(default=None, description="技能要求1"),
        ExcelField(name="技能要求1")
    ]
    # 技能要求2
    skill_required2: Annotated[
        Optional[str],
        Field(default=None, description="技能要求2"),
        ExcelField(name="技能要求2")
    ]
    # 技能要求3
    skill_required3: Annotated[
        Optional[str],
        Field(default=None, description="技能要求3"),
        ExcelField(name="技能要求3")
    ]
    # 技能要求4
    skill_required4: Annotated[
        Optional[str],
        Field(default=None, description="技能要求4"),
        ExcelField(name="技能要求4")
    ]
    # 岗位描述
    post_desc: Annotated[
        Optional[str],
        Field(default=None, description="岗位描述"),
        ExcelField(name="岗位描述")
    ]
    # 企业名称
    enterprise_name: Annotated[
        Optional[str],
        Field(default=None, description="企业名称"),
        VoField(query=True),
        ExcelField(name="企业名称")
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
    # 企业介绍
    enterprise_desc: Annotated[
        Optional[str],
        Field(default=None, description="企业介绍"),
        ExcelField(name="企业介绍")
    ]
    # 备注
    remark: Annotated[
        Optional[str],
        Field(default=None, description="备注"),
        ExcelField(name="备注")
    ]
    # 创建人
    user_id: Annotated[
        Optional[int],
        BeforeValidator(str_to_int),
        Field(default=None, description="创建人"),
        ExcelField(name="创建人")
    ]
    # 创建时间
    create_time: Annotated[
        Optional[datetime],
        BeforeValidator(to_datetime()),
        Field(default=None, description="创建时间"),
        VoField(query=True),
        ExcelField(name="创建时间")
    ]
    # 更新人
    update_by: Annotated[
        Optional[str],
        Field(default=None, description="更新人"),
        ExcelField(name="更新人")
    ]
    # 更新时间
    update_time: Annotated[
        Optional[datetime],
        BeforeValidator(to_datetime()),
        Field(default=None, description="更新时间"),
        ExcelField(name="更新时间")
    ]
    params: Optional[dict] = Field(default=None, description="参数")
    # 页码
    page_num: Optional[int] = Field(default=1, description="页码")
    # 每页数量
    page_size: Optional[int] = Field(default=10, description="每页数量")