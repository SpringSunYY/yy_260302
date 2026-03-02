# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: city_map_util.py
# @Time    : 2026-03-02

import json
import os
from typing import Dict, Optional


class CityMapUtil:
    """城市名称映射工具类"""

    _instance = None
    _city_name_map: Dict[str, str] = {}
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def initialize(cls, json_path: Optional[str] = None):
        """
        初始化城市名称映射

        Args:
            json_path: JSON文件路径，如果为None则使用默认路径
        """
        if cls._initialized:
            return

        # 默认路径：ruoyi_common/config/area_data.json
        if json_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # ruoyi_common/utils -> ruoyi_common/config
            json_path = os.path.join(current_dir, '..', 'config', 'area_data.json')
            json_path = os.path.normpath(json_path)

        cls._city_name_map = cls._load_city_name_map(json_path)
        cls._initialized = True

    @classmethod
    def _load_city_name_map(cls, json_path: str) -> Dict[str, str]:
        """
        加载城市名称映射，将简单城市名映射到完整地名

        Args:
            json_path: JSON文件路径

        Returns:
            Dict[str, str]: 城市名称映射字典
        """
        city_map = {}

        if not os.path.exists(json_path):
            print(f"[城市映射加载] 文件不存在: {json_path}")
            return city_map

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                area_data = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"[城市映射加载] 从JSON文件加载失败: {e}")
            return city_map

        # 处理每个区域数据项
        for item in area_data:
            if 'name' in item and 'fullName' in item:
                name = item['name']
                full_name = item['fullName']

                # 检查是否已在映射中
                if name in city_map or full_name in city_map.values():
                    continue

                city_map[name] = full_name
                cls._add_city_name_variations(city_map, name, full_name)

        print(f"[城市映射加载] 加载完成，共 {len(city_map)} 个映射")
        return city_map

    @classmethod
    def _add_city_name_variations(cls, city_map: Dict[str, str], name: str, full_name: str):
        """为城市名称添加简化变体"""
        # 创建简化名称映射
        if name.endswith('市'):
            simple_name = name[:-1]  # 移除"市"
            if simple_name not in city_map:
                city_map[simple_name] = full_name
        elif name.endswith('自治区'):
            simple_name = name[:-3]  # 移除"自治区"
            if simple_name not in city_map:
                city_map[simple_name] = full_name

    @classmethod
    def get_full_name(cls, city_name: str) -> str:
        """
        获取城市的完整名称

        Args:
            city_name: 城市名称

        Returns:
            str: 完整地名，如果找不到则返回原名称
        """
        if not cls._initialized:
            cls.initialize()

        return cls._city_name_map.get(city_name, city_name)

    @classmethod
    def normalize_province_city(cls, province: str, city: str) -> tuple:
        """
        规范化省份和城市信息，直接使用JSON映射

        Args:
            province (str): 省份
            city (str): 城市

        Returns:
            tuple: (规范化后的省份, 规范化后的城市, 完整地址)
        """
        if not cls._initialized:
            cls.initialize()

        # 直接用城市名查找映射
        if city:
            full_name = cls.get_full_name(city)
            if full_name and full_name != city:
                # 分割完整地址得到省份和城市
                parts = full_name.split(" ")
                if len(parts) >= 2:
                    return parts[0], parts[1], full_name

        # 如果找不到映射，返回原值
        if province and city:
            full_address = f"{province} {city}"
            return province, city, full_address

        return province, city, ""

