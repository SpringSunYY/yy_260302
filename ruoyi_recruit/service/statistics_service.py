from typing import List

from ruoyi_recruit.domain.statistics.vo import StatisticsVo
from ruoyi_recruit.mapper import StatisticsMapper


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
                if cur_min is not None and (province_map[province]["min"] is None or cur_min < province_map[province]["min"]):
                    province_map[province]["min"] = cur_min
                if cur_max is not None and (province_map[province]["max"] is None or cur_max > province_map[province]["max"]):
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
