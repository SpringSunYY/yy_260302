# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: like_info_mapper.py
# @Time    : 2026-03-02 16:56:43

from typing import List, Optional
from datetime import datetime

from flask import g
from sqlalchemy import select, update, delete

from ruoyi_admin.ext import db
from ruoyi_recruit.domain.entity import LikeInfo
from ruoyi_recruit.domain.entity import RecommendInfo
from ruoyi_recruit.domain.po import LikeInfoPo
from ruoyi_recruit.domain.po import RecommendInfoPo


class LikeInfoMapper:
    """用户点赞Mapper"""

    @classmethod
    def select_like_info_list(cls, like_info: LikeInfo) -> List[LikeInfo]:
        """
        查询用户点赞列表

        Args:
            like_info (like_info): 用户点赞对象

        Returns:
            List[like_info]: 用户点赞列表
        """
        try:
            # 构建查询条件
            stmt = select(LikeInfoPo)

            if like_info.id is not None:
                stmt = stmt.where(LikeInfoPo.id == like_info.id)

            if like_info.user_name:
                stmt = stmt.where(LikeInfoPo.user_name.like("%" + str(like_info.user_name) + "%"))

            if like_info.post_type is not None:
                stmt = stmt.where(LikeInfoPo.post_type == like_info.post_type)

            if like_info.city_level is not None:
                stmt = stmt.where(LikeInfoPo.city_level == like_info.city_level)

            if like_info.province:
                stmt = stmt.where(LikeInfoPo.province.like("%" + str(like_info.province) + "%"))

            if like_info.city:
                stmt = stmt.where(LikeInfoPo.city.like("%" + str(like_info.city) + "%"))

            if like_info.experience_required is not None:
                stmt = stmt.where(LikeInfoPo.experience_required == like_info.experience_required)

            if like_info.education_required is not None:
                stmt = stmt.where(LikeInfoPo.education_required == like_info.education_required)

            if like_info.main_business:
                stmt = stmt.where(LikeInfoPo.main_business.like("%" + str(like_info.main_business) + "%"))

            if like_info.enterprise_size is not None:
                stmt = stmt.where(LikeInfoPo.enterprise_size == like_info.enterprise_size)

            if like_info.financing_situation is not None:
                stmt = stmt.where(LikeInfoPo.financing_situation == like_info.financing_situation)

            _params = getattr(like_info, "params", {}) or {}
            begin_val = _params.get("beginCreateTime")
            end_val = _params.get("endCreateTime")
            if begin_val is not None:
                stmt = stmt.where(LikeInfoPo.create_time >= begin_val)
            if end_val is not None:
                stmt = stmt.where(LikeInfoPo.create_time <= end_val)
            if "criterian_meta" in g and g.criterian_meta.page:
                g.criterian_meta.page.stmt = stmt
            result = db.session.execute(stmt).scalars().all()
            return [LikeInfo.model_validate(item) for item in result] if result else []
        except Exception as e:
            print(f"查询用户点赞列表出错: {e}")
            return []

    @classmethod
    def select_like_info_by_id(cls, id: int) -> Optional[LikeInfo]:
        """
        根据ID查询用户点赞

        Args:
            id (int): 编号

        Returns:
            like_info: 用户点赞对象
        """
        try:
            result = db.session.get(LikeInfoPo, id)
            return LikeInfo.model_validate(result) if result else None
        except Exception as e:
            print(f"根据ID查询用户点赞出错: {e}")
            return None

    @classmethod
    def insert_like_info(cls, like_info: LikeInfo) -> int:
        """
        新增用户点赞

        Args:
            like_info (like_info): 用户点赞对象

        Returns:
            int: 插入的记录数
        """
        try:
            now = datetime.now()
            new_po = LikeInfoPo()
            new_po.recruit_id = like_info.recruit_id
            new_po.user_id = like_info.user_id
            new_po.user_name = like_info.user_name
            new_po.post_type = like_info.post_type
            new_po.city_level = like_info.city_level
            new_po.province = like_info.province
            new_po.city = like_info.city
            new_po.salary_month_avg = like_info.salary_month_avg
            new_po.experience_required = like_info.experience_required
            new_po.education_required = like_info.education_required
            new_po.main_business = like_info.main_business
            new_po.enterprise_size = like_info.enterprise_size
            new_po.financing_situation = like_info.financing_situation
            new_po.score = like_info.score
            new_po.create_time = like_info.create_time or now
            db.session.add(new_po)
            db.session.commit()
            like_info.id = new_po.id
            return 1
        except Exception as e:
            db.session.rollback()
            print(f"新增用户点赞出错: {e}")
            return 0

    @classmethod
    def update_like_info(cls, like_info: LikeInfo) -> int:
        """
        修改用户点赞

        Args:
            like_info (like_info): 用户点赞对象

        Returns:
            int: 更新的记录数
        """
        try:

            existing = db.session.get(LikeInfoPo, like_info.id)
            if not existing:
                return 0
            now = datetime.now()
            # 主键不参与更新
            existing.user_id = like_info.user_id
            existing.user_name = like_info.user_name
            existing.post_type = like_info.post_type
            existing.city_level = like_info.city_level
            existing.province = like_info.province
            existing.city = like_info.city
            existing.salary_month_avg = like_info.salary_month_avg
            existing.experience_required = like_info.experience_required
            existing.education_required = like_info.education_required
            existing.main_business = like_info.main_business
            existing.enterprise_size = like_info.enterprise_size
            existing.financing_situation = like_info.financing_situation
            existing.score = like_info.score
            existing.create_time = like_info.create_time
            db.session.commit()
            return 1

        except Exception as e:
            db.session.rollback()
            print(f"修改用户点赞出错: {e}")
            return 0

    @classmethod
    def delete_like_info_by_ids(cls, ids: List[int]) -> int:
        """
        批量删除用户点赞

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        try:
            stmt = delete(LikeInfoPo).where(LikeInfoPo.id.in_(ids))
            result = db.session.execute(stmt)
            db.session.commit()
            return result.rowcount
        except Exception as e:
            db.session.rollback()
            print(f"批量删除用户点赞出错: {e}")
            return 0

    @classmethod
    def select_is_like(cls, recruit_id: int, user_id: int) -> Optional[LikeInfo]:
        """
        查询用户是否点赞

        Args:
            recruit_id (int): 招聘信息ID
            user_id (int): 用户ID

        Returns:
            like_info: 用户点赞对象
        """
        try:
            stmt = select(LikeInfoPo).where(LikeInfoPo.recruit_id == recruit_id, LikeInfoPo.user_id == user_id)
            result = db.session.execute(stmt).scalars().first()
            return LikeInfo.model_validate(result) if result else None
        except Exception as e:
            print(f"查询用户是否点赞出错: {e}")

    @classmethod
    def delete_like_by_recruit_and_user(cls, recruit_id: int, user_id: int) -> int:
        """
        根据招聘信息ID和用户ID删除点赞记录

        Args:
            recruit_id (int): 招聘信息ID
            user_id (int): 用户ID

        Returns:
            int: 删除的记录数
        """
        try:
            stmt = delete(LikeInfoPo).where(
                LikeInfoPo.recruit_id == recruit_id,
                LikeInfoPo.user_id == user_id
            )
            result = db.session.execute(stmt)
            db.session.commit()
            return result.rowcount
        except Exception as e:
            db.session.rollback()
            print(f"删除用户点赞出错: {e}")
            return 0

    @classmethod
    def select_user_latest_likes(cls, user_id: int, limit: int = 30) -> List[LikeInfo]:
        """
        获取用户最新的N条点赞记录

        Args:
            user_id (int): 用户ID
            limit (int): 返回记录数，默认30

        Returns:
            List[LikeInfo]: 用户点赞记录列表
        """
        try:
            stmt = select(LikeInfoPo).where(
                LikeInfoPo.user_id == user_id
            ).order_by(LikeInfoPo.create_time.desc()).limit(limit)
            result = db.session.execute(stmt).scalars().all()
            return [LikeInfo.model_validate(item) for item in result] if result else []
        except Exception as e:
            print(f"获取用户最新点赞记录出错: {e}")
            return []

    @classmethod
    def select_user_latest_likes_after_time(cls, user_id: int, after_time: datetime, limit: int = 30) -> List[LikeInfo]:
        """
        获取用户在指定时间之后的N条点赞记录

        Args:
            user_id (int): 用户ID
            after_time (datetime): 时间点
            limit (int): 返回记录数，默认30

        Returns:
            List[LikeInfo]: 用户点赞记录列表
        """
        try:
            stmt = select(LikeInfoPo).where(
                LikeInfoPo.user_id == user_id,
                LikeInfoPo.create_time > after_time
            ).order_by(LikeInfoPo.create_time.desc()).limit(limit)
            result = db.session.execute(stmt).scalars().all()
            return [LikeInfo.model_validate(item) for item in result] if result else []
        except Exception as e:
            print(f"获取用户时间点之后点赞记录出错: {e}")
            return []

