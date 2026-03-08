# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: view_info_mapper.py
# @Time    : 2026-03-02 16:56:42
from typing import List, Optional
from datetime import datetime

from flask import g
from sqlalchemy import select, update, delete, and_

from ruoyi_admin.ext import db
from ruoyi_recruit.domain.entity import ViewInfo
from ruoyi_recruit.domain.po import ViewInfoPo


class ViewInfoMapper:
    """用户浏览Mapper"""

    @classmethod
    def select_view_info_list(cls, view_info: ViewInfo) -> List[ViewInfo]:
        """
        查询用户浏览列表

        Args:
            view_info (view_info): 用户浏览对象

        Returns:
            List[view_info]: 用户浏览列表
        """
        try:
            # 构建查询条件
            stmt = select(ViewInfoPo)

            if view_info.id is not None:
                stmt = stmt.where(ViewInfoPo.id == view_info.id)

            if view_info.user_name:
                stmt = stmt.where(ViewInfoPo.user_name.like("%" + str(view_info.user_name) + "%"))

            if view_info.post_type is not None:
                stmt = stmt.where(ViewInfoPo.post_type == view_info.post_type)

            if view_info.city_level is not None:
                stmt = stmt.where(ViewInfoPo.city_level == view_info.city_level)

            if view_info.province:
                stmt = stmt.where(ViewInfoPo.province.like("%" + str(view_info.province) + "%"))

            if view_info.city:
                stmt = stmt.where(ViewInfoPo.city.like("%" + str(view_info.city) + "%"))

            if view_info.experience_required is not None:
                stmt = stmt.where(ViewInfoPo.experience_required == view_info.experience_required)

            if view_info.education_required is not None:
                stmt = stmt.where(ViewInfoPo.education_required == view_info.education_required)

            if view_info.main_business:
                stmt = stmt.where(ViewInfoPo.main_business.like("%" + str(view_info.main_business) + "%"))

            if view_info.enterprise_size is not None:
                stmt = stmt.where(ViewInfoPo.enterprise_size == view_info.enterprise_size)

            if view_info.financing_situation is not None:
                stmt = stmt.where(ViewInfoPo.financing_situation == view_info.financing_situation)

            if view_info.score is not None:
                stmt = stmt.where(ViewInfoPo.score == view_info.score)

            _params = getattr(view_info, "params", {}) or {}
            begin_val = _params.get("beginCreateTime")
            end_val = _params.get("endCreateTime")
            if begin_val is not None:
                stmt = stmt.where(ViewInfoPo.create_time >= begin_val)
            if end_val is not None:
                stmt = stmt.where(ViewInfoPo.create_time <= end_val)

            if ("criterian_meta" in g and
                        g.criterian_meta.scope is not None and
                        g.criterian_meta.scope != [] and
                        g.criterian_meta.scope != ()):
                stmt = stmt.where(g.criterian_meta.scope)
            stmt = stmt.order_by(ViewInfoPo.create_time.desc())
            if "criterian_meta" in g and g.criterian_meta.page:
                g.criterian_meta.page.stmt = stmt
            result = db.session.execute(stmt).scalars().all()
            return [ViewInfo.model_validate(item) for item in result] if result else []
        except Exception as e:
            print(f"查询用户浏览列表出错: {e}")
            return []

    @classmethod
    def select_view_info_by_id(cls, id: int) -> Optional[ViewInfo]:
        """
        根据ID查询用户浏览

        Args:
            id (int): 编号

        Returns:
            view_info: 用户浏览对象
        """
        try:
            result = db.session.get(ViewInfoPo, id)
            return ViewInfo.model_validate(result) if result else None
        except Exception as e:
            print(f"根据ID查询用户浏览出错: {e}")
            return None

    @classmethod
    def insert_view_info(cls, view_info: ViewInfo) -> int:
        """
        新增用户浏览

        Args:
            view_info (view_info): 用户浏览对象

        Returns:
            int: 插入的记录数
        """
        try:
            now = datetime.now()
            new_po = ViewInfoPo()
            new_po.id = view_info.id
            new_po.recruit_id = view_info.recruit_id
            new_po.user_id = view_info.user_id
            new_po.user_name = view_info.user_name
            new_po.post_type = view_info.post_type
            new_po.city_level = view_info.city_level
            new_po.province = view_info.province
            new_po.city = view_info.city
            new_po.salary_month_avg = view_info.salary_month_avg
            new_po.experience_required = view_info.experience_required
            new_po.education_required = view_info.education_required
            new_po.main_business = view_info.main_business
            new_po.enterprise_size = view_info.enterprise_size
            new_po.financing_situation = view_info.financing_situation
            new_po.score = view_info.score
            new_po.create_time = view_info.create_time or now
            db.session.add(new_po)
            db.session.commit()
            view_info.id = new_po.id
            return 1
        except Exception as e:
            db.session.rollback()
            print(f"新增用户浏览出错: {e}")
            return 0

    @classmethod
    def update_view_info(cls, view_info: ViewInfo) -> int:
        """
        修改用户浏览

        Args:
            view_info (view_info): 用户浏览对象

        Returns:
            int: 更新的记录数
        """
        try:

            existing = db.session.get(ViewInfoPo, view_info.id)
            if not existing:
                return 0
            now = datetime.now()
            # 主键不参与更新
            existing.user_id = view_info.user_id
            existing.user_name = view_info.user_name
            existing.post_type = view_info.post_type
            existing.city_level = view_info.city_level
            existing.province = view_info.province
            existing.city = view_info.city
            existing.salary_month_avg = view_info.salary_month_avg
            existing.experience_required = view_info.experience_required
            existing.education_required = view_info.education_required
            existing.main_business = view_info.main_business
            existing.enterprise_size = view_info.enterprise_size
            existing.financing_situation = view_info.financing_situation
            existing.score = view_info.score
            existing.create_time = view_info.create_time
            db.session.commit()
            return 1

        except Exception as e:
            db.session.rollback()
            print(f"修改用户浏览出错: {e}")
            return 0

    @classmethod
    def delete_view_info_by_ids(cls, ids: List[int]) -> int:
        """
        批量删除用户浏览

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        try:
            stmt = delete(ViewInfoPo).where(ViewInfoPo.id.in_(ids))
            result = db.session.execute(stmt)
            db.session.commit()
            return result.rowcount
        except Exception as e:
            db.session.rollback()
            print(f"批量删除用户浏览出错: {e}")
            return 0

    @classmethod
    def select_is_view_by_date(cls, recruit_id: int, user_id: int, now: str) \
            -> Optional[ViewInfo]:
        """
        查询用户是否浏览过该职位，时间为0:00:00,23:59:59范围

        Args:
            recruit_id (int): 职位ID
            user_id (int): 用户ID
            now (str): 当前时间

        Returns:
            view_info: 用户浏览对象
        """
        try:
            date_obj = datetime.strptime(now, '%Y-%m-%d')
            start_time = date_obj.replace(hour=0, minute=0, second=0, microsecond=0)
            end_time = date_obj.replace(hour=23, minute=59, second=59, microsecond=999999)
            stmt = select(ViewInfoPo).where(
                and_(ViewInfoPo.recruit_id == recruit_id,
                     ViewInfoPo.user_id == user_id,
                     ViewInfoPo.create_time >= start_time,
                     ViewInfoPo.create_time <= end_time))
            result = db.session.execute(stmt).scalars().first()
            return ViewInfo.model_validate(result) if result else None
        except Exception as e:
            print(f"查询用户是否浏览过该职位出错: {e}")

    @classmethod
    def select_user_latest_views(cls, user_id: int, limit: int = 30) -> List[ViewInfo]:
        """
        获取用户最新的N条浏览记录

        Args:
            user_id (int): 用户ID
            limit (int): 返回记录数，默认30

        Returns:
            List[ViewInfo]: 用户浏览记录列表
        """
        try:
            stmt = select(ViewInfoPo).where(
                ViewInfoPo.user_id == user_id
            ).order_by(ViewInfoPo.create_time.desc()).limit(limit)
            result = db.session.execute(stmt).scalars().all()
            return [ViewInfo.model_validate(item) for item in result] if result else []
        except Exception as e:
            print(f"获取用户最新浏览记录出错: {e}")
            return []

    @classmethod
    def select_user_latest_views_after_time(cls, user_id: int, after_time: datetime, limit: int = 30) -> List[ViewInfo]:
        """
        获取用户在指定时间之后的N条浏览记录

        Args:
            user_id (int): 用户ID
            after_time (datetime): 时间点
            limit (int): 返回记录数，默认30

        Returns:
            List[ViewInfo]: 用户浏览记录列表
        """
        try:
            stmt = select(ViewInfoPo).where(
                ViewInfoPo.user_id == user_id,
                ViewInfoPo.create_time > after_time
            ).order_by(ViewInfoPo.create_time.desc()).limit(limit)
            result = db.session.execute(stmt).scalars().all()
            return [ViewInfo.model_validate(item) for item in result] if result else []
        except Exception as e:
            print(f"获取用户时间点之后浏览记录出错: {e}")
            return []
