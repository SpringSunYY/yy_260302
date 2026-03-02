# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: like_info_service.py
# @Time    : 2026-03-02 16:56:43

from typing import List, Optional

from ruoyi_common.exception import ServiceException
from ruoyi_common.utils.base import LogUtil
from ruoyi_common.utils.security_util import get_username, get_user_id
from ruoyi_recruit.domain.entity import LikeInfo, RecruitInfo
from ruoyi_recruit.mapper.like_info_mapper import LikeInfoMapper

class LikeInfoService:
    """用户点赞服务类"""
    @classmethod
    def select_like_info_list(cls, like_info: LikeInfo) -> List[LikeInfo]:
        """
        查询用户点赞列表

        Args:
            like_info (like_info): 用户点赞对象

        Returns:
            List[like_info]: 用户点赞列表
        """
        return LikeInfoMapper.select_like_info_list(like_info)

    
    @classmethod
    def select_like_info_by_id(cls, id: int) -> Optional[LikeInfo]:
        """
        根据ID查询用户点赞

        Args:
            id (int): 编号

        Returns:
            like_info: 用户点赞对象
        """
        return LikeInfoMapper.select_like_info_by_id(id)
    
    @classmethod
    def insert_like_info(cls, like_info: LikeInfo) -> int:
        """
        新增用户点赞

        Args:
            like_info (like_info): 用户点赞对象

        Returns:
            int: 插入的记录数
        """
        return LikeInfoMapper.insert_like_info(like_info)

    
    @classmethod
    def update_like_info(cls, like_info: LikeInfo) -> int:
        """
        修改用户点赞

        Args:
            like_info (like_info): 用户点赞对象

        Returns:
            int: 更新的记录数
        """
        return LikeInfoMapper.update_like_info(like_info)
    

    
    @classmethod
    def delete_like_info_by_ids(cls, ids: List[int]) -> int:
        """
        批量删除用户点赞

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        return LikeInfoMapper.delete_like_info_by_ids(ids)

    @classmethod
    def toggle_like(cls, recruit_info: RecruitInfo) -> dict:
        """
        点赞或取消点赞

        Args:
            recruit_info (RecruitInfo): 招聘信息对象

        Returns:
            dict: 操作结果，包含 is_liked (bool) 表示操作后是否已点赞
        """
        user_id = get_user_id()
        user_name = get_username()

        # 查询是否已点赞
        existing_like = LikeInfoMapper.select_is_like(recruit_info.recruit_id, user_id)

        if existing_like:
            # 已点赞，取消点赞
            result = LikeInfoMapper.delete_like_by_recruit_and_user(recruit_info.recruit_id, user_id)
            if result > 0:
                return {"is_liked": False, "msg": "取消点赞成功"}
            return {"is_liked": True, "msg": "取消点赞失败"}
        else:
            # 未点赞，添加点赞
            like_info = LikeInfo()
            like_info.recruit_id = recruit_info.recruit_id
            like_info.user_id = user_id
            like_info.user_name = user_name
            like_info.post_type = recruit_info.post_type
            like_info.city_level = recruit_info.city_level
            like_info.province = recruit_info.province
            like_info.city = recruit_info.city
            like_info.salary_month_avg = recruit_info.salary_month_avg
            like_info.experience_required = recruit_info.experience_required
            like_info.education_required = recruit_info.education_required
            like_info.main_business = recruit_info.main_business
            like_info.enterprise_size = recruit_info.enterprise_size
            like_info.financing_situation = recruit_info.financing_situation
            like_info.score = 5

            result = LikeInfoMapper.insert_like_info(like_info)
            if result > 0:
                return {"is_liked": True, "msg": "点赞成功"}
            return {"is_liked": False, "msg": "点赞失败"}
    
    @classmethod
    def import_like_info(cls, like_info_list: List[LikeInfo], is_update: bool = False) -> str:
        """
        导入用户点赞数据

        Args:
            like_info_list (List[like_info]): 用户点赞列表
            is_update (bool): 是否更新已存在的数据

        Returns:
            str: 导入结果消息
        """
        if not like_info_list:
            raise ServiceException("导入用户点赞数据不能为空")

        success_count = 0
        fail_count = 0
        success_msg = ""
        fail_msg = ""

        for like_info in like_info_list:
            try:
                display_value = like_info
                
                display_value = getattr(like_info, "id", display_value)
                existing = None
                if like_info.id is not None:
                    existing = LikeInfoMapper.select_like_info_by_id(like_info.id)
                if existing:
                    if is_update:
                        result = LikeInfoMapper.update_like_info(like_info)
                    else:
                        fail_count += 1
                        fail_msg += f"<br/> 第{fail_count}条数据，已存在：{display_value}"
                        continue
                else:
                    result = LikeInfoMapper.insert_like_info(like_info)
                
                if result > 0:
                    success_count += 1
                    success_msg += f"<br/> 第{success_count}条数据，操作成功：{display_value}"
                else:
                    fail_count += 1
                    fail_msg += f"<br/> 第{fail_count}条数据，操作失败：{display_value}"
            except Exception as e:
                fail_count += 1
                fail_msg += f"<br/> 第{fail_count}条数据，导入失败，原因：{e.__class__.__name__}"
                LogUtil.logger.error(f"导入用户点赞失败，原因：{e}")

        if fail_count > 0:
            if success_msg:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{success_msg}<br/>" + fail_msg
            else:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{fail_msg}"
            raise ServiceException(fail_msg)
        success_msg = f"恭喜您，数据已全部导入成功！共 {success_count} 条，数据如下：" + success_msg
        return success_msg