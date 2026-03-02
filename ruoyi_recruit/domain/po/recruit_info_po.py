# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: recruit_info_po.py
# @Time    : 2026-03-02 16:56:43

from typing import Optional
from datetime import datetime

from sqlalchemy import BigInteger, Boolean, Date, DateTime, Float, Integer, JSON, LargeBinary, Numeric, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column

from ruoyi_admin.ext import db

class RecruitInfoPo(db.Model):
    """
    招聘信息PO对象
    """
    __tablename__ = 'tb_recruit_info'
    __table_args__ = {'comment': '招聘信息'}
    recruit_id: Mapped[int] = mapped_column(
        'recruit_id',
        BigInteger,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment='编号'
    )
    post_type: Mapped[Optional[str]] = mapped_column(
        'post_type',
        String(255),
        nullable=True,
        comment='岗位大类'
    )
    post: Mapped[Optional[str]] = mapped_column(
        'post',
        String(255),
        nullable=True,
        comment='岗位'
    )
    post_update_time: Mapped[Optional[datetime]] = mapped_column(
        'post_update_time',
        DateTime,
        nullable=True,
        comment='岗位更新时间'
    )
    title_url: Mapped[Optional[str]] = mapped_column(
        'title_url',
        Text,
        nullable=True,
        comment='标题链接'
    )
    city_level: Mapped[Optional[str]] = mapped_column(
        'city_level',
        String(255),
        nullable=True,
        comment='城市等级'
    )
    province: Mapped[Optional[str]] = mapped_column(
        'province',
        String(255),
        nullable=True,
        comment='省份'
    )
    city: Mapped[Optional[str]] = mapped_column(
        'city',
        String(255),
        nullable=True,
        comment='城市'
    )
    location: Mapped[Optional[str]] = mapped_column(
        'location',
        String(255),
        nullable=True,
        comment='工作地点'
    )
    salary_range: Mapped[Optional[str]] = mapped_column(
        'salary_range',
        String(255),
        nullable=True,
        comment='薪资范围'
    )
    salary_min: Mapped[Optional[str]] = mapped_column(
        'salary_min',
        Numeric(10, 0),
        nullable=True,
        comment='薪资下限'
    )
    salary_max: Mapped[Optional[str]] = mapped_column(
        'salary_max',
        Numeric(10, 0),
        nullable=True,
        comment='薪资上限'
    )
    salary_month_avg: Mapped[Optional[str]] = mapped_column(
        'salary_month_avg',
        Numeric(10, 0),
        nullable=True,
        comment='薪资平均值'
    )
    salary_remark: Mapped[Optional[str]] = mapped_column(
        'salary_remark',
        String(255),
        nullable=True,
        comment='薪资备注'
    )
    bonus_performance: Mapped[Optional[str]] = mapped_column(
        'bonus_performance',
        String(255),
        nullable=True,
        comment='奖金绩效'
    )
    experience_required: Mapped[Optional[str]] = mapped_column(
        'experience_required',
        String(255),
        nullable=True,
        comment='经验要求'
    )
    education_required: Mapped[Optional[str]] = mapped_column(
        'education_required',
        String(255),
        nullable=True,
        comment='学历要求'
    )
    skill_required: Mapped[Optional[str]] = mapped_column(
        'skill_required',
        String(255),
        nullable=True,
        comment='技能要求'
    )
    skill_required1: Mapped[Optional[str]] = mapped_column(
        'skill_required_1',
        String(255),
        nullable=True,
        comment='技能要求1'
    )
    skill_required2: Mapped[Optional[str]] = mapped_column(
        'skill_required_2',
        String(255),
        nullable=True,
        comment='技能要求2'
    )
    skill_required3: Mapped[Optional[str]] = mapped_column(
        'skill_required_3',
        String(255),
        nullable=True,
        comment='技能要求3'
    )
    skill_required4: Mapped[Optional[str]] = mapped_column(
        'skill_required_4',
        String(255),
        nullable=True,
        comment='技能要求4'
    )
    post_desc: Mapped[Optional[str]] = mapped_column(
        'post_desc',
        Text,
        nullable=True,
        comment='岗位描述'
    )
    enterprise_name: Mapped[Optional[str]] = mapped_column(
        'enterprise_name',
        String(255),
        nullable=True,
        comment='企业名称'
    )
    main_business: Mapped[Optional[str]] = mapped_column(
        'main_business',
        String(255),
        nullable=True,
        comment='主营业务'
    )
    enterprise_size: Mapped[Optional[str]] = mapped_column(
        'enterprise_size',
        String(255),
        nullable=True,
        comment='企业规模'
    )
    financing_situation: Mapped[Optional[str]] = mapped_column(
        'financing_situation',
        String(255),
        nullable=True,
        comment='融资情况'
    )
    enterprise_desc: Mapped[Optional[str]] = mapped_column(
        'enterprise_desc',
        Text,
        nullable=True,
        comment='企业介绍'
    )
    remark: Mapped[Optional[str]] = mapped_column(
        'remark',
        Text,
        nullable=True,
        comment='备注'
    )
    user_id: Mapped[Optional[int]] = mapped_column(
        'user_id',
        BigInteger,
        nullable=False,
        comment='创建人'
    )
    create_time: Mapped[Optional[datetime]] = mapped_column(
        'create_time',
        DateTime,
        nullable=False,
        comment='创建时间'
    )
    update_by: Mapped[Optional[str]] = mapped_column(
        'update_by',
        String(255),
        nullable=True,
        comment='更新人'
    )
    update_time: Mapped[Optional[datetime]] = mapped_column(
        'update_time',
        DateTime,
        nullable=True,
        comment='更新时间'
    )