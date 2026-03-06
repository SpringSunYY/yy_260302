from typing import List

from ruoyi_recruit.domain.statistics.po import StatisticsPo
from ruoyi_recruit.domain.statistics.vo import StatisticsVo
from ruoyi_recruit.mapper import StatisticsMapper
from ruoyi_system.service.sys_config import SysConfigService
from ruoyi_common.constant import ConfigConstants

class StatisticsService:
    """
    招聘信息数据分析统计
    """

    @classmethod
    def map_statistics(cls, statistics_entity) -> List[StatisticsVo]:
        """
        地图统计信息
        """
        pos = StatisticsMapper.map_statistics(statistics_entity)
        if not pos:
            return []
        # 以空格分割，例如广东省 广州市
        # 如果传过来的地区等级为空，则返回每个省份数据，需要构建到每个省份
        # 如果传过来的地区等级不为空，则返回每个城市数据，需要构建到每个城市
        if statistics_entity.address is None:
            province_map = {}
            for po in pos:
                if not po.name:
                    continue
                province = str(po.name).split(" ")[0]
                if province not in province_map:
                    province_map[province] = {"value": 0, "weighted_avg_sum": 0.0, "min": None, "max": None}
                val = int(po.value) if po.value else 0
                province_map[province]["value"] += val
                province_map[province]["weighted_avg_sum"] += float(po.avg or 0) * val
                cur_min = float(po.min) if po.min is not None else None
                cur_max = float(po.max) if po.max is not None else None
                if cur_min is not None and (
                        province_map[province]["min"] is None or cur_min < province_map[province]["min"]):
                    province_map[province]["min"] = cur_min
                if cur_max is not None and (
                        province_map[province]["max"] is None or cur_max > province_map[province]["max"]):
                    province_map[province]["max"] = cur_max
            result = []
            for province, data in province_map.items():
                avg = data["weighted_avg_sum"] / data["value"] if data["value"] > 0 else 0.0
                result.append(StatisticsVo(
                    name=province,
                    value=data["value"],
                    avg=round(avg, 2),
                    min=round(data["min"], 2) if data["min"] is not None else None,
                    max=round(data["max"], 2) if data["max"] is not None else None
                ))
            return result
        else:
            result = []
            for po in pos:
                if not po.name:
                    continue
                parts = str(po.name).split(" ")
                city = parts[1] if len(parts) > 1 else parts[0]
                result.append(StatisticsVo(
                    name=city,
                    value=int(po.value) if po.value is not None else None,
                    avg=round(float(po.avg), 2) if po.avg is not None else None,
                    min=round(float(po.min), 2) if po.min is not None else None,
                    max=round(float(po.max), 2) if po.max is not None else None
                ))
            return result

    @classmethod
    def city_level_statistics(cls, statistics_entity) -> List[StatisticsVo]:
        """
        城市等级统计
        """
        pos = StatisticsMapper.city_level_statistics(statistics_entity)
        return cls.build_result(pos)

    @classmethod
    def post_type_statistics(cls, statistics_entity) -> List[StatisticsVo]:
        """
        岗位统计
        """
        pos = StatisticsMapper.post_type_statistics(statistics_entity)
        return cls.build_result(pos)

    @classmethod
    def education_statistics(cls, statistics_entity) -> List[StatisticsVo]:
        """
        学历统计
        """
        pos = StatisticsMapper.education_statistics(statistics_entity)
        return cls.build_result(pos)

    @classmethod
    def build_result(cls, pos: List[StatisticsPo]) -> List[StatisticsVo]:
        """
        构建结果
        """
        if not pos:
            return []
        result = []
        for po in pos:
            result.append(StatisticsVo(
                name=po.name,
                value=int(po.value) if po.value is not None else None,
                avg=round(float(po.avg), 2) if po.avg is not None else None,
                min=round(float(po.min), 2) if po.min is not None else None,
                max=round(float(po.max), 2) if po.max is not None else None
            ))
        return result

    @classmethod
    def enterprise_size_statistics(cls, statistics_entity) -> List[StatisticsVo]:
        """
        企业规模统计
        """
        pos = StatisticsMapper.enterprise_size_statistics(statistics_entity)
        return cls.build_result(pos)

    @classmethod
    def experience_statistics(cls, statistics_entity) -> List[StatisticsVo]:
        """
        经验统计
        """
        pos = StatisticsMapper.experience_statistics(statistics_entity)
        return cls.build_result(pos)

    @classmethod
    def build_strip_result(cls, pos: List[StatisticsPo], size: 50) -> List[StatisticsVo]:
        """
        构建特殊结果
        """
        if not pos:
            return []

        result_map = {}
        for po in pos:
            if not po.name:
                continue
            # 如果有空格去掉空格
            name = str(po.name).replace(" ", "")
            names = str(name).replace("/", ",").split(",")
            value = int(po.value) if po.value else 0
            avg = float(po.avg) if po.avg is not None else 0.0
            cur_min = float(po.min) if po.min is not None else None
            cur_max = float(po.max) if po.max is not None else None

            for name_str in names:
                name_str = name_str.strip()
                if not name_str:
                    continue
                if name_str not in result_map:
                    result_map[name_str] = {
                        "value": 0,
                        "weighted_avg_sum": 0.0,
                        "min": None,
                        "max": None
                    }

                result_map[name_str]["value"] += value
                result_map[name_str]["weighted_avg_sum"] += avg * value

                if cur_min is not None:
                    if result_map[name_str]["min"] is None or cur_min < result_map[name_str]["min"]:
                        result_map[name_str]["min"] = cur_min
                if cur_max is not None:
                    if result_map[name_str]["max"] is None or cur_max > result_map[name_str]["max"]:
                        result_map[name_str]["max"] = cur_max

        result = []
        for name_str, data in result_map.items():
            avg = data["weighted_avg_sum"] / data["value"] if data["value"] > 0 else 0.0
            result.append(StatisticsVo(
                name=name_str,
                value=data["value"],
                avg=round(avg, 2),
                min=round(data["min"], 2) if data["min"] is not None else None,
                max=round(data["max"], 2) if data["max"] is not None else None
            ))

        result.sort(key=lambda x: x.value if x.value else 0, reverse=True)
        # 返回前100
        result = result[:size]
        return result

    @classmethod
    def main_business_statistics(cls, statistics_entity) -> List[StatisticsVo]:
        """
        主营业务统计
        """
        pos = StatisticsMapper.main_business_statistics(statistics_entity)
        return cls.build_strip_result(pos, 50)

    @classmethod
    def skill_statistics(cls, statistics_entity) -> List[StatisticsVo]:
        """
        技能统计
        """
        pos = StatisticsMapper.skill_statistics(statistics_entity)
        return cls.build_strip_result(pos, 200)

    @classmethod
    def _get_salary_range(cls) -> List[int]:
        """获取薪资区间配置"""
        salary_range_str = SysConfigService.select_config_by_key(ConfigConstants.CONFIG_KEY_SALARY_RANGE)
        try:
            return [int(x.strip()) for x in salary_range_str.split(',')]
        except Exception:
            return [6000, 8000, 10000, 15000, 20000]

    @classmethod
    def _format_salary(cls, salary: int) -> str:
        """格式化薪资显示，小于10000显示为K，大于等于10000显示为W"""
        if salary < 10000:
            return f"{salary // 1000}K"
        else:
            w_value = salary / 10000
            if w_value == int(w_value):
                return f"{int(w_value)}W"
            else:
                return f"{w_value:.1f}W"

    @classmethod
    def _get_salary_range_label(cls, salary: float, salary_range: List[int]) -> str:
        """根据薪资获取范围标签（格式化显示）"""
        if not salary:
            return "未知"
        formatted_range = [cls._format_salary(s) for s in salary_range]
        if salary < salary_range[0]:
            return f"{formatted_range[0]}以下"
        elif salary >= salary_range[-1]:
            return f"{formatted_range[-1]}以上"
        else:
            for i in range(len(salary_range) - 1):
                if salary_range[i] <= salary < salary_range[i + 1]:
                    return f"{formatted_range[i]}-{formatted_range[i + 1]}"
            return f"{formatted_range[-1]}以上"

    @classmethod
    def salary_statistics(cls, statistics_entity) -> List[StatisticsVo]:
        """
        薪资统计
        """
        pos = StatisticsMapper.salary_statistics(statistics_entity)
        if not pos:
            return []
        # 获取薪资区间配置并格式化name字段
        salary_range = cls._get_salary_range()

        # 先将数据按name分组聚合
        result_map = {}
        for po in pos:
            name = po.name
            if name is not None:
                name = cls._get_salary_range_label(float(name), salary_range)

            value = int(po.value) if po.value is not None else 0
            avg = float(po.avg) if po.avg is not None else 0.0

            if name not in result_map:
                result_map[name] = {
                    "value": 0,
                    "weighted_avg_sum": 0.0,
                    "min": None,
                    "max": None
                }

            result_map[name]["value"] += value
            result_map[name]["weighted_avg_sum"] += avg * value

            cur_min = float(po.min) if po.min is not None else None
            cur_max = float(po.max) if po.max is not None else None

            if cur_min is not None:
                if result_map[name]["min"] is None or cur_min < result_map[name]["min"]:
                    result_map[name]["min"] = cur_min
            if cur_max is not None:
                if result_map[name]["max"] is None or cur_max > result_map[name]["max"]:
                    result_map[name]["max"] = cur_max

        # 构建结果列表
        result = []
        for name, data in result_map.items():
            avg = data["weighted_avg_sum"] / data["value"] if data["value"] > 0 else 0.0
            result.append(StatisticsVo(
                name=name,
                value=data["value"],
                avg=round(avg, 2),
                min=round(data["min"], 2) if data["min"] is not None else None,
                max=round(data["max"], 2) if data["max"] is not None else None
            ))
        return result
