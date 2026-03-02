# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: recruit_info_service.py
# @Time    : 2026-03-02 16:56:43

from typing import List, Optional

from ruoyi_common.exception import ServiceException
from ruoyi_common.utils.base import LogUtil
from ruoyi_recruit.domain.entity import RecruitInfo
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
    
    @classmethod
    def insert_recruit_info(cls, recruit_info: RecruitInfo) -> int:
        """
        新增招聘信息

        Args:
            recruit_info (recruit_info): 招聘信息对象

        Returns:
            int: 插入的记录数
        """
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
    def import_recruit_info(cls, recruit_info_list: List[RecruitInfo], is_update: bool = False) -> str:
        """
        导入招聘信息数据

        Args:
            recruit_info_list (List[recruit_info]): 招聘信息列表
            is_update (bool): 是否更新已存在的数据

        Returns:
            str: 导入结果消息
        """
        if not recruit_info_list:
            raise ServiceException("导入招聘信息数据不能为空")

        success_count = 0
        fail_count = 0
        success_msg = ""
        fail_msg = ""

        for recruit_info in recruit_info_list:
            try:
                display_value = recruit_info
                
                display_value = getattr(recruit_info, "recruit_id", display_value)
                existing = None
                if recruit_info.recruit_id is not None:
                    existing = RecruitInfoMapper.select_recruit_info_by_id(recruit_info.recruit_id)
                if existing:
                    if is_update:
                        result = RecruitInfoMapper.update_recruit_info(recruit_info)
                    else:
                        fail_count += 1
                        fail_msg += f"<br/> 第{fail_count}条数据，已存在：{display_value}"
                        continue
                else:
                    result = RecruitInfoMapper.insert_recruit_info(recruit_info)
                
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

        if fail_count > 0:
            if success_msg:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{success_msg}<br/>" + fail_msg
            else:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{fail_msg}"
            raise ServiceException(fail_msg)
        success_msg = f"恭喜您，数据已全部导入成功！共 {success_count} 条，数据如下：" + success_msg
        return success_msg