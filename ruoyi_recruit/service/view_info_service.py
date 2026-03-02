# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: view_info_service.py
# @Time    : 2026-03-02 16:56:42

from typing import List, Optional

from ruoyi_common.exception import ServiceException
from ruoyi_common.utils.base import LogUtil
from ruoyi_recruit.domain.entity import ViewInfo
from ruoyi_recruit.mapper.view_info_mapper import ViewInfoMapper

class ViewInfoService:
    """用户浏览服务类"""
    @classmethod
    def select_view_info_list(cls, view_info: ViewInfo) -> List[ViewInfo]:
        """
        查询用户浏览列表

        Args:
            view_info (view_info): 用户浏览对象

        Returns:
            List[view_info]: 用户浏览列表
        """
        return ViewInfoMapper.select_view_info_list(view_info)

    
    @classmethod
    def select_view_info_by_id(cls, id: int) -> Optional[ViewInfo]:
        """
        根据ID查询用户浏览

        Args:
            id (int): 编号

        Returns:
            view_info: 用户浏览对象
        """
        return ViewInfoMapper.select_view_info_by_id(id)
    
    @classmethod
    def insert_view_info(cls, view_info: ViewInfo) -> int:
        """
        新增用户浏览

        Args:
            view_info (view_info): 用户浏览对象

        Returns:
            int: 插入的记录数
        """
        return ViewInfoMapper.insert_view_info(view_info)

    
    @classmethod
    def update_view_info(cls, view_info: ViewInfo) -> int:
        """
        修改用户浏览

        Args:
            view_info (view_info): 用户浏览对象

        Returns:
            int: 更新的记录数
        """
        return ViewInfoMapper.update_view_info(view_info)
    

    
    @classmethod
    def delete_view_info_by_ids(cls, ids: List[int]) -> int:
        """
        批量删除用户浏览

        Args:
            ids (List[int]): ID列表

        Returns:
            int: 删除的记录数
        """
        return ViewInfoMapper.delete_view_info_by_ids(ids)
    
    @classmethod
    def import_view_info(cls, view_info_list: List[ViewInfo], is_update: bool = False) -> str:
        """
        导入用户浏览数据

        Args:
            view_info_list (List[view_info]): 用户浏览列表
            is_update (bool): 是否更新已存在的数据

        Returns:
            str: 导入结果消息
        """
        if not view_info_list:
            raise ServiceException("导入用户浏览数据不能为空")

        success_count = 0
        fail_count = 0
        success_msg = ""
        fail_msg = ""

        for view_info in view_info_list:
            try:
                display_value = view_info
                
                display_value = getattr(view_info, "id", display_value)
                existing = None
                if view_info.id is not None:
                    existing = ViewInfoMapper.select_view_info_by_id(view_info.id)
                if existing:
                    if is_update:
                        result = ViewInfoMapper.update_view_info(view_info)
                    else:
                        fail_count += 1
                        fail_msg += f"<br/> 第{fail_count}条数据，已存在：{display_value}"
                        continue
                else:
                    result = ViewInfoMapper.insert_view_info(view_info)
                
                if result > 0:
                    success_count += 1
                    success_msg += f"<br/> 第{success_count}条数据，操作成功：{display_value}"
                else:
                    fail_count += 1
                    fail_msg += f"<br/> 第{fail_count}条数据，操作失败：{display_value}"
            except Exception as e:
                fail_count += 1
                fail_msg += f"<br/> 第{fail_count}条数据，导入失败，原因：{e.__class__.__name__}"
                LogUtil.logger.error(f"导入用户浏览失败，原因：{e}")

        if fail_count > 0:
            if success_msg:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{success_msg}<br/>" + fail_msg
            else:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{fail_msg}"
            raise ServiceException(fail_msg)
        success_msg = f"恭喜您，数据已全部导入成功！共 {success_count} 条，数据如下：" + success_msg
        return success_msg