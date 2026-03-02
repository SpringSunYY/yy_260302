# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: view_info_po.py
# @Time    : 2026-03-02 16:56:42

from typing import Optional
from datetime import datetime

from sqlalchemy import BigInteger, Boolean, Date, DateTime, Float, Integer, JSON, LargeBinary, Numeric, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column

from ruoyi_admin.ext import db

class ViewInfoPo(db.Model):
    """
    用户浏览PO对象
    """
    __tablename__ = 'tb_view_info'
    __table_args__ = {'comment': '用户浏览'}
    id: Mapped[int] = mapped_column(
        'id',
        BigInteger,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment='编号'
    )
    user_id: Mapped[Optional[int]] = mapped_column(
        'user_id',
        BigInteger,
        nullable=False,
        comment='用户'
    )
    user_name: Mapped[Optional[str]] = mapped_column(
        'user_name',
        String(255),
        nullable=False,
        comment='用户名'
    )
    post_type: Mapped[Optional[str]] = mapped_column(
        'post_type',
        String(255),
        nullable=True,
        comment='岗位大类'
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
    salary_month_avg: Mapped[Optional[str]] = mapped_column(
        'salary_month_avg',
        Numeric(10, 0),
        nullable=True,
        comment='薪资平均值'
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
    score: Mapped[Optional[str]] = mapped_column(
        'score',
        Numeric(10, 0),
        nullable=False,
        comment='分数'
    )
    create_time: Mapped[Optional[datetime]] = mapped_column(
        'create_time',
        DateTime,
        nullable=False,
        comment='创建时间'
    )