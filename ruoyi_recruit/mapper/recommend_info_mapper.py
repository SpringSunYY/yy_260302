# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: recommend_info_mapper.py
# @Time    : 2026-03-02 16:56:43

from typing import List, Optional
from datetime import datetime

from flask import g
from sqlalchemy import select, update, delete

from ruoyi_admin.ext import db
from ruoyi_recruit.domain.entity import RecommendInfo
from ruoyi_recruit.domain.po import RecommendInfoPo


class RecommendInfoMapper:
    """用户推荐Mapper"""

    @classmethod
    def select_recommend_info_list(cls, recommend_info: RecommendInfo) -> List[RecommendInfo]:
        """
        查询用户推荐列表

        Args:
            recommend_info (recommend_info): 用户推荐对象

        Returns:
            List[recommend_info]: 用户推荐列表
        """
        try:
            # 构建查询条件
            stmt = select(RecommendInfoPo)

            if recommend_info.id is not None:
                stmt = stmt.where(RecommendInfoPo.id == recommend_info.id)

            if recommend_info.user_name:
                stmt = stmt.where(RecommendInfoPo.user_name.like("%" + str(recommend_info.user_name) + "%"))

            _params = getattr(recommend_info, "params", {}) or {}
            begin_val = _params.get("beginCreateTime")
            end_val = _params.get("endCreateTime")
            if begin_val is not None:
                stmt = stmt.where(RecommendInfoPo.create_time >= begin_val)
            if end_val is not None:
                stmt = stmt.where(RecommendInfoPo.create_time <= end_val)

            if ("criterian_meta" in g and
                    g.criterian_meta.scope is not None and
                    g.criterian_meta.scope != [] and
                    g.criterian_meta.scope != ()):
                stmt = stmt.where(g.criterian_meta.scope)
            stmt = stmt.order_by(RecommendInfoPo.create_time.desc())
            if "criterian_meta" in g and g.criterian_meta.page:
                g.criterian_meta.page.stmt = stmt
            result = db.session.execute(stmt).scalars().all()
            return [RecommendInfo.model_validate(item) for item in result] if result else []
        except Exception as e:
            print(f"查询用户推荐列表出错: {e}")
            return []

    @classmethod
    def select_recommend_info_by_id(cls, id: int) -> Optional[RecommendInfo]:
        """
        根据ID查询用户推荐

        Args:
            id (int): 推荐编号

        Returns:
            recommend_info: 用户推荐对象
        """
        try:
            result = db.session.get(RecommendInfoPo, id)
            return RecommendInfo.model_validate(result) if result else None
        except Exception as e:
            print(f"根据ID查询用户推荐出错: {e}")
            return None

    @classmethod
    def insert_recommend_info(cls, recommend_info: RecommendInfo) -> int:
        """
        新增用户推荐

        Args:
            recommend_info (recommend_info): 用户推荐对象

        Returns:
            int: 插入的记录数
        """
        try:
            now = datetime.now()
            new_po = RecommendInfoPo()
            new_po.id = recommend_info.id
            new_po.user_id = recommend_info.user_id
            new_po.user_name = recommend_info.user_name
            new_po.model_info = recommend_info.model_info
            new_po.content = recommend_info.content
            new_po.create_time = recommend_info.create_time or now
            db.session.add(new_po)
            db.session.commit()
            recommend_info.id = new_po.id
            return 1
        except Exception as e:
            db.session.rollback()
            print(f"新增用户推荐出错: {e}")
            return 0

    @classmethod
    def update_recommend_info(cls, recommend_info: RecommendInfo) -> int:
        """
        修改用户推荐

        Args:
            recommend_info (recommend_info): 用户推荐对象

        Returns:
            int: 更新的记录数
        """
        try:

            existing = db.session.get(RecommendInfoPo, recommend_info.id)
            if not existing:
                return 0
            now = datetime.now()
            # 主键不参与更新
            existing.user_id = recommend_info.user_id
            existing.user_name = recommend_info.user_name
            existing.model_info = recommend_info.model_info
            existing.content = recommend_info.content
            existing.create_time = recommend_info.create_time
            db.session.commit()
            return 1

        except Exception as e:
            db.session.rollback()
            print(f"修改用户推荐出错: {e}")
            return 0

    @classmethod
    def delete_recommend_info_by_ids(cls, ids: List[int]) -> int:
        """
        批量删除用户推荐

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        try:
            stmt = delete(RecommendInfoPo).where(RecommendInfoPo.id.in_(ids))
            result = db.session.execute(stmt)
            db.session.commit()
            return result.rowcount
        except Exception as e:
            db.session.rollback()
            print(f"批量删除用户推荐出错: {e}")
            return 0

    @classmethod
    def select_user_recommend_history(cls, user_id: int) -> Optional[RecommendInfo]:
        """
        获取用户最新的推荐记录

        Args:
            user_id (int): 用户ID

        Returns:
            Optional[RecommendInfo]: 推荐记录
        """
        try:
            stmt = select(RecommendInfoPo).where(
                RecommendInfoPo.user_id == user_id
            ).order_by(RecommendInfoPo.create_time.desc()).limit(1)
            result = db.session.execute(stmt).scalars().first()
            return RecommendInfo.model_validate(result) if result else None
        except Exception as e:
            print(f"获取用户推荐历史出错: {e}")
            return None
