# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: recruit_info_service.py
# @Time    : 2026-03-02 16:56:43

import re
from datetime import datetime
from typing import List, Optional

from ruoyi_common.exception import ServiceException
from ruoyi_common.utils import DateUtil
from ruoyi_common.utils.base import LogUtil
from ruoyi_common.utils.city_map_util import CityMapUtil
from ruoyi_common.utils.security_util import get_username, get_user_id
from ruoyi_recruit.domain.entity import RecruitInfo, ViewInfo
from ruoyi_recruit.mapper import LikeInfoMapper, ViewInfoMapper
from ruoyi_recruit.mapper.recruit_info_mapper import RecruitInfoMapper


class RecruitInfoService:
    """招聘信息服务类"""

    @classmethod
    def select_recruit_info_list(cls, recruit_info: RecruitInfo) -> List[RecruitInfo]:
        """
        查询招聘信息列表

        Args:
            recruit_info (recruit_info): 招聘信息对象

        Returns:
            List[recruit_info]: 招聘信息列表
        """
        return RecruitInfoMapper.select_recruit_info_list(recruit_info)

    @classmethod
    def select_recruit_info_by_id(cls, recruit_id: int) -> Optional[RecruitInfo]:
        """
        根据ID查询招聘信息

        Args:
            recruit_id (int): 编号

        Returns:
            recruit_info: 招聘信息对象
        """
        return RecruitInfoMapper.select_recruit_info_by_id(recruit_id)

    def select_recruit_info_detail_by_id(self, recruit_id) -> Optional[RecruitInfo]:
        recruit_info = RecruitInfoMapper.select_recruit_info_by_id(recruit_id)
        user_id = get_user_id()
        user_name = get_username()
        # 查询是否点赞
        like_info_db = LikeInfoMapper.select_is_like(recruit_id, user_id)
        if like_info_db:
            recruit_info.is_liked = True
        else:
            recruit_info.is_liked = False
        now = DateUtil.get_date_now()
        # 查询用户今日是否浏览过
        view_info_db = ViewInfoMapper.select_is_view_by_date(recruit_id, user_id, now)
        if view_info_db is None:
            # 新增浏览信息
            view_info = ViewInfo()
            view_info.recruit_id = recruit_id
            view_info.user_id = user_id
            view_info.user_name = user_name
            view_info.post_type = recruit_info.post_type
            view_info.city_level = recruit_info.city_level
            view_info.province = recruit_info.province
            view_info.city = recruit_info.city
            view_info.salary_month_avg = recruit_info.salary_month_avg
            view_info.experience_required = recruit_info.experience_required
            view_info.education_required = recruit_info.education_required
            view_info.main_business = recruit_info.main_business
            view_info.financing_situation = recruit_info.financing_situation
            view_info.enterprise_size = recruit_info.enterprise_size
            view_info.score = 3
            ViewInfoMapper.insert_view_info(view_info)
        return recruit_info

    @classmethod
    def insert_recruit_info(cls, recruit_info: RecruitInfo) -> int:
        """
        新增招聘信息

        Args:
            recruit_info (recruit_info): 招聘信息对象

        Returns:
            int: 插入的记录数
        """
        recruit_info.user_id = get_user_id()
        # 查询改为是否已存在
        recruit_info_db = RecruitInfoMapper.select_recruit_info_by_unique(recruit_info.post,
                                                                          recruit_info.enterprise_name,
                                                                          recruit_info.city)
        if recruit_info_db:
            raise ServiceException(
                f"已存在岗位：{recruit_info.post}，企业：{recruit_info.enterprise_name}，城市：{recruit_info.city}")
        return RecruitInfoMapper.insert_recruit_info(recruit_info)

    @classmethod
    def update_recruit_info(cls, recruit_info: RecruitInfo) -> int:
        """
        修改招聘信息

        Args:
            recruit_info (recruit_info): 招聘信息对象

        Returns:
            int: 更新的记录数
        """
        # 查询改为是否已存在
        recruit_info_db = RecruitInfoMapper.select_recruit_info_by_unique(recruit_info.post,
                                                                          recruit_info.enterprise_name,
                                                                          recruit_info.city)
        if recruit_info_db and recruit_info_db.recruit_id != recruit_info.recruit_id:
            raise ServiceException(
                f"已存在岗位：{recruit_info.post}，企业：{recruit_info.enterprise_name}，城市：{recruit_info.city}")
        return RecruitInfoMapper.update_recruit_info(recruit_info)

    @classmethod
    def delete_recruit_info_by_ids(cls, ids: List[int]) -> int:
        """
        批量删除招聘信息

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        return RecruitInfoMapper.delete_recruit_info_by_ids(ids)

    @classmethod
    def import_recruit_info(cls, recruit_info_list: List[RecruitInfo]) -> str:
        """
        导入招聘信息数据

        Args:
            recruit_info_list (List[recruit_info]): 招聘信息列表

        Returns:
            str: 导入结果消息
        """
        if not recruit_info_list:
            raise ServiceException("导入招聘信息数据不能为空")

        # 初始化城市映射工具
        CityMapUtil.initialize()
        user_name = get_username()
        user_id = get_user_id()
        success_count = 0
        fail_count = 0
        success_msg = ""
        fail_msg = ""
        skip_count = 0  # 过滤掉的数据数量
        total_count = len(recruit_info_list)
        processed_count = 0

        LogUtil.logger.info(f"[导入招聘信息] 开始导入，共 {total_count} 条数据")

        for recruit_info in recruit_info_list:
            processed_count += 1
            # 每10条打印一次进度
            if processed_count % 10 == 0:
                LogUtil.logger.info(f"[导入招聘信息] 进度：{processed_count}/{total_count}")

            try:
                # 3、如果岗位、城市、省份为空则过滤此数据
                if not recruit_info.post or not recruit_info.city or not recruit_info.province:
                    skip_count += 1
                    LogUtil.logger.warn(
                        f"[导入招聘信息] 过滤数据：岗位={recruit_info.post}, 城市={recruit_info.city}, 省份={recruit_info.province}")
                    continue

                # 1、优化省份城市：转换为完整地址
                normalized_province, normalized_city, full_address = CityMapUtil.normalize_province_city(
                    recruit_info.province, recruit_info.city
                )
                recruit_info.province = normalized_province
                recruit_info.city = normalized_city
                recruit_info.full_address = full_address

                # 2、薪资处理：如果薪资备注为空默认为12薪，计算平均薪资
                salary_avg, salary_remark = cls._process_salary(
                    recruit_info.salary_min,
                    recruit_info.salary_max,
                    recruit_info.salary_remark
                )
                recruit_info.salary_month_avg = salary_avg
                recruit_info.salary_remark = salary_remark

                # 5、技能要求拼接：skill_required1-4 用 / 分割
                recruit_info.skill_required = cls._process_skill_required(
                    recruit_info.skill_required1,
                    recruit_info.skill_required2,
                    recruit_info.skill_required3,
                    recruit_info.skill_required4
                )

                # 6、根据 post + enterprise_name + city 唯一标识判断新增或更新
                existing = None
                if recruit_info.post and recruit_info.enterprise_name and recruit_info.city:
                    existing = RecruitInfoMapper.select_recruit_info_by_unique(
                        recruit_info.post,
                        recruit_info.enterprise_name,
                        recruit_info.city
                    )

                now = datetime.now()
                display_value = f"{recruit_info.post}-{recruit_info.enterprise_name}-{recruit_info.city}"

                if existing:
                    # 存在则更新：更新更新人和更新时间，保留创建人和创建时间
                    recruit_info.recruit_id = existing.recruit_id
                    recruit_info.user_id = existing.user_id
                    recruit_info.create_time = existing.create_time
                    recruit_info.update_by = user_name
                    recruit_info.update_time = now
                    result = RecruitInfoMapper.update_recruit_info(recruit_info)
                    LogUtil.logger.info(f"[导入招聘信息] 更新成功：{display_value}")
                else:
                    # 不存在则新增
                    recruit_info.user_id = user_id
                    recruit_info.create_time = now
                    recruit_info.update_by = None
                    recruit_info.update_time = now
                    result = RecruitInfoMapper.insert_recruit_info(recruit_info)
                    LogUtil.logger.info(f"[导入招聘信息] 新增成功：{display_value}")

                if result > 0:
                    success_count += 1
                    success_msg += f"<br/> 第{success_count}条数据，操作成功：{display_value}"
                else:
                    fail_count += 1
                    fail_msg += f"<br/> 第{fail_count}条数据，操作失败：{display_value}"
            except Exception as e:
                fail_count += 1
                fail_msg += f"<br/> 第{fail_count}条数据，导入失败，原因：{e.__class__.__name__}"
                LogUtil.logger.error(f"导入招聘信息失败，原因：{e}")

        # 构建结果消息
        result_parts = []
        if success_count > 0:
            result_parts.append(f"导入成功{success_count}条")
        if fail_count > 0:
            result_parts.append(f"失败{fail_count}条")
        if skip_count > 0:
            result_parts.append(f"过滤{skip_count}条(岗位/城市/省份为空)")

        if fail_count > 0:
            if success_msg:
                fail_msg = "，".join(result_parts) + f"。{success_msg}<br/>" + fail_msg
            else:
                fail_msg = "，".join(result_parts) + f"。{fail_msg}"
            raise ServiceException(fail_msg)

        success_msg = f"恭喜您，数据已全部导入成功！共 {success_count} 条，数据如下：" + success_msg
        LogUtil.logger.info(
            f"[导入招聘信息] 导入完成，共 {total_count} 条，成功 {success_count} 条，失败 {fail_count} 条，过滤 {skip_count} 条")
        return success_msg

    @staticmethod
    def _process_salary(salary_min: Optional[float], salary_max: Optional[float],
                        salary_remark: Optional[str]) -> tuple:
        """
        处理薪资信息：
        1. 如果薪资备注为空，默认为12薪
        2. 根据下限、上限和n薪计算平均月薪

        Args:
            salary_min (Optional[float]): 薪资下限
            salary_max (Optional[float]): 薪资上限
            salary_remark (Optional[str]): 薪资备注（如"13薪"）

        Returns:
            tuple: (平均月薪, 薪资备注)
        """
        # 处理薪资备注，空值默认为12薪
        months = 12  # 默认12薪
        if salary_remark:
            # 匹配 n薪 格式
            match = re.search(r'(\d+)\s*薪', salary_remark)
            if match:
                months = int(match.group(1))
        else:
            salary_remark = "12薪"  # 默认值

        # 计算平均月薪
        salary_avg = None
        if salary_min is not None and salary_max is not None:
            # (下限 + 上限) / 2 * 月份数 / 12
            salary_avg = (salary_min + salary_max) / 2 * months / 12

        return salary_avg, salary_remark

    @staticmethod
    def _process_skill_required(skill1: Optional[str], skill2: Optional[str],
                                skill3: Optional[str], skill4: Optional[str]) -> str:
        """
        拼接技能要求，将4个技能要求字段用 / 分割

        Args:
            skill1 (Optional[str]): 技能要求1
            skill2 (Optional[str]): 技能要求2
            skill3 (Optional[str]): 技能要求3
            skill4 (Optional[str]): 技能要求4

        Returns:
            str: 拼接后的技能要求
        """
        skills = []
        for skill in [skill1, skill2, skill3, skill4]:
            if skill and str(skill).strip():
                skills.append(str(skill).strip())

        return " / ".join(skills)
