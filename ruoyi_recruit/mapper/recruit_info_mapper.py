# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: recruit_info_mapper.py
# @Time    : 2026-03-02 16:56:43

from typing import List, Optional
from datetime import datetime

from flask import g
from sqlalchemy import select, update, delete

from ruoyi_admin.ext import db
from ruoyi_recruit.domain.entity import RecruitInfo
from ruoyi_recruit.domain.po import RecruitInfoPo

class RecruitInfoMapper:
    """招聘信息Mapper"""

    @classmethod
    def select_recruit_info_list(cls, recruit_info: RecruitInfo) -> List[RecruitInfo]:
        """
        查询招聘信息列表

        Args:
            recruit_info (recruit_info): 招聘信息对象

        Returns:
            List[recruit_info]: 招聘信息列表
        """
        try:
            # 构建查询条件
            stmt = select(RecruitInfoPo)


            if recruit_info.recruit_id is not None:
                stmt = stmt.where(RecruitInfoPo.recruit_id == recruit_info.recruit_id)

            if recruit_info.post_type is not None:
                stmt = stmt.where(RecruitInfoPo.post_type == recruit_info.post_type)

            if recruit_info.post:
                stmt = stmt.where(RecruitInfoPo.post.like("%" + str(recruit_info.post) + "%"))

            _params = getattr(recruit_info, "params", {}) or {}
            begin_val = _params.get("beginPostUpdateTime")
            end_val = _params.get("endPostUpdateTime")
            if begin_val is not None:
                stmt = stmt.where(RecruitInfoPo.post_update_time >= begin_val)
            if end_val is not None:
                stmt = stmt.where(RecruitInfoPo.post_update_time <= end_val)

            if recruit_info.city_level is not None:
                stmt = stmt.where(RecruitInfoPo.city_level == recruit_info.city_level)

            if recruit_info.province:
                stmt = stmt.where(RecruitInfoPo.province.like("%" + str(recruit_info.province) + "%"))

            if recruit_info.city:
                stmt = stmt.where(RecruitInfoPo.city.like("%" + str(recruit_info.city) + "%"))

            if recruit_info.experience_required is not None:
                stmt = stmt.where(RecruitInfoPo.experience_required == recruit_info.experience_required)

            if recruit_info.education_required is not None:
                stmt = stmt.where(RecruitInfoPo.education_required == recruit_info.education_required)

            if recruit_info.skill_required:
                stmt = stmt.where(RecruitInfoPo.skill_required.like("%" + str(recruit_info.skill_required) + "%"))

            if recruit_info.enterprise_name:
                stmt = stmt.where(RecruitInfoPo.enterprise_name.like("%" + str(recruit_info.enterprise_name) + "%"))

            if recruit_info.main_business:
                stmt = stmt.where(RecruitInfoPo.main_business.like("%" + str(recruit_info.main_business) + "%"))

            if recruit_info.enterprise_size is not None:
                stmt = stmt.where(RecruitInfoPo.enterprise_size == recruit_info.enterprise_size)

            if recruit_info.financing_situation is not None:
                stmt = stmt.where(RecruitInfoPo.financing_situation == recruit_info.financing_situation)

            _params = getattr(recruit_info, "params", {}) or {}
            begin_val = _params.get("beginCreateTime")
            end_val = _params.get("endCreateTime")
            if begin_val is not None:
                stmt = stmt.where(RecruitInfoPo.create_time >= begin_val)
            if end_val is not None:
                stmt = stmt.where(RecruitInfoPo.create_time <= end_val)
            stmt=stmt.order_by(RecruitInfoPo.update_time.desc())
            if "criterian_meta" in g and g.criterian_meta.page:
                g.criterian_meta.page.stmt = stmt
            result = db.session.execute(stmt).scalars().all()
            return [RecruitInfo.model_validate(item) for item in result] if result else []
        except Exception as e:
            print(f"查询招聘信息列表出错: {e}")
            return []


    @classmethod
    def select_recruit_info_by_id(cls, recruit_id: int) -> Optional[RecruitInfo]:
        """
        根据ID查询招聘信息

        Args:
            recruit_id (int): 编号

        Returns:
            recruit_info: 招聘信息对象
        """
        try:
            result = db.session.get(RecruitInfoPo, recruit_id)
            return RecruitInfo.model_validate(result) if result else None
        except Exception as e:
            print(f"根据ID查询招聘信息出错: {e}")
            return None


    @classmethod
    def insert_recruit_info(cls, recruit_info: RecruitInfo) -> int:
        """
        新增招聘信息

        Args:
            recruit_info (recruit_info): 招聘信息对象

        Returns:
            int: 插入的记录数
        """
        try:
            now = datetime.now()
            new_po = RecruitInfoPo()
            new_po.recruit_id = recruit_info.recruit_id
            new_po.post_type = recruit_info.post_type
            new_po.post = recruit_info.post
            new_po.post_update_time = recruit_info.post_update_time
            new_po.title_url = recruit_info.title_url
            new_po.city_level = recruit_info.city_level
            new_po.province = recruit_info.province
            new_po.city = recruit_info.city
            new_po.full_address = recruit_info.full_address
            new_po.location = recruit_info.location
            new_po.salary_range = recruit_info.salary_range
            new_po.salary_min = recruit_info.salary_min
            new_po.salary_max = recruit_info.salary_max
            new_po.salary_month_avg = recruit_info.salary_month_avg
            new_po.salary_remark = recruit_info.salary_remark
            new_po.bonus_performance = recruit_info.bonus_performance
            new_po.experience_required = recruit_info.experience_required
            new_po.education_required = recruit_info.education_required
            new_po.skill_required = recruit_info.skill_required
            new_po.skill_required1 = recruit_info.skill_required1
            new_po.skill_required2 = recruit_info.skill_required2
            new_po.skill_required3 = recruit_info.skill_required3
            new_po.skill_required4 = recruit_info.skill_required4
            new_po.post_desc = recruit_info.post_desc
            new_po.enterprise_name = recruit_info.enterprise_name
            new_po.main_business = recruit_info.main_business
            new_po.enterprise_size = recruit_info.enterprise_size
            new_po.financing_situation = recruit_info.financing_situation
            new_po.enterprise_desc = recruit_info.enterprise_desc
            new_po.remark = recruit_info.remark
            new_po.user_id = recruit_info.user_id
            new_po.create_time = recruit_info.create_time or now
            new_po.update_by = recruit_info.update_by
            new_po.update_time = recruit_info.update_time or now
            db.session.add(new_po)
            db.session.commit()
            recruit_info.recruit_id = new_po.recruit_id
            return 1
        except Exception as e:
            db.session.rollback()
            print(f"新增招聘信息出错: {e}")
            return 0


    @classmethod
    def update_recruit_info(cls, recruit_info: RecruitInfo) -> int:
        """
        修改招聘信息

        Args:
            recruit_info (recruit_info): 招聘信息对象

        Returns:
            int: 更新的记录数
        """
        try:

            existing = db.session.get(RecruitInfoPo, recruit_info.recruit_id)
            if not existing:
                return 0
            now = datetime.now()
            # 主键不参与更新
            existing.post_type = recruit_info.post_type
            existing.post = recruit_info.post
            existing.post_update_time = recruit_info.post_update_time
            existing.title_url = recruit_info.title_url
            existing.city_level = recruit_info.city_level
            existing.province = recruit_info.province
            existing.city = recruit_info.city
            existing.full_address=recruit_info.full_address
            existing.location = recruit_info.location
            existing.salary_range = recruit_info.salary_range
            existing.salary_min = recruit_info.salary_min
            existing.salary_max = recruit_info.salary_max
            existing.salary_month_avg = recruit_info.salary_month_avg
            existing.salary_remark = recruit_info.salary_remark
            existing.bonus_performance = recruit_info.bonus_performance
            existing.experience_required = recruit_info.experience_required
            existing.education_required = recruit_info.education_required
            existing.skill_required = recruit_info.skill_required
            existing.skill_required1 = recruit_info.skill_required1
            existing.skill_required2 = recruit_info.skill_required2
            existing.skill_required3 = recruit_info.skill_required3
            existing.skill_required4 = recruit_info.skill_required4
            existing.post_desc = recruit_info.post_desc
            existing.enterprise_name = recruit_info.enterprise_name
            existing.main_business = recruit_info.main_business
            existing.enterprise_size = recruit_info.enterprise_size
            existing.financing_situation = recruit_info.financing_situation
            existing.enterprise_desc = recruit_info.enterprise_desc
            existing.remark = recruit_info.remark
            existing.user_id = recruit_info.user_id
            existing.create_time = recruit_info.create_time
            existing.update_by = recruit_info.update_by
            existing.update_time = recruit_info.update_time or now
            db.session.commit()
            return 1

        except Exception as e:
            db.session.rollback()
            print(f"修改招聘信息出错: {e}")
            return 0

    @classmethod
    def delete_recruit_info_by_ids(cls, ids: List[int]) -> int:
        """
        批量删除招聘信息

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        try:
            stmt = delete(RecruitInfoPo).where(RecruitInfoPo.recruit_id.in_(ids))
            result = db.session.execute(stmt)
            db.session.commit()
            return result.rowcount
        except Exception as e:
            db.session.rollback()
            print(f"批量删除招聘信息出错: {e}")
            return 0

    @classmethod
    def select_recruit_info_by_unique(cls, post: str, enterprise_name: str, city: str) -> Optional[RecruitInfo]:
        """
        根据岗位+企业名称+城市查询唯一招聘信息

        Args:
            post (str): 岗位
            enterprise_name (str): 企业名称
            city (str): 城市

        Returns:
            Optional[RecruitInfo]: 招聘信息对象
        """
        try:
            stmt = select(RecruitInfoPo).where(
                RecruitInfoPo.post == post,
                RecruitInfoPo.enterprise_name == enterprise_name,
                RecruitInfoPo.city == city
            )
            result = db.session.execute(stmt).scalar_one_or_none()
            return RecruitInfo.model_validate(result) if result else None
        except Exception as e:
            print(f"根据唯一标识查询招聘信息出错: {e}")
            return None
