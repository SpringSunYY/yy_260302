from typing import List

from ruoyi_admin.ext import db
from ruoyi_recruit.domain.po import RecruitInfoPo
from ruoyi_recruit.domain.statistics.dto import StatisticsRequest
from ruoyi_recruit.domain.statistics.po import StatisticsPo
from sqlalchemy import select, func


class StatisticsMapper:
    """
    统计信息映射类
    """
    @classmethod
    def build_where(cls, stmt, statistics_entity):
        if statistics_entity.address is not None:
            stmt = stmt.where(RecruitInfoPo.full_address.like(f"%{statistics_entity.address}%"))
        if statistics_entity.cityLevel is not None:
            stmt = stmt.where(RecruitInfoPo.city_level == statistics_entity.cityLevel)
        if statistics_entity.postType is not None:
            stmt = stmt.where(RecruitInfoPo.post_type == statistics_entity.postType)
        return stmt

    @classmethod
    def map_statistics(cls, statistics_entity: StatisticsRequest) -> List[StatisticsPo]:
        """
        地图统计信息
        select count(*)     as value,
           avg(salary_month_avg) as avg,
           min(salary_month_avg) as min,
           max(salary_month_avg) as max,
           full_address as name
        from tb_recruit_info
        where full_address is not null
        group by full_address
        Args:
            statistics_entity: 统计信息实体

        Returns:
            统计信息PO列表
        """
        try:
            stmt = select(func.count("*").label("value"),
                          func.avg(RecruitInfoPo.salary_month_avg).label("avg"),
                          func.max(RecruitInfoPo.salary_month_avg).label("max"),
                          func.min(RecruitInfoPo.salary_month_avg).label("min"),
                          RecruitInfoPo.full_address.label("name")
                          ).select_from(RecruitInfoPo).group_by("name").order_by("value")
            stmt = cls.build_where(stmt, statistics_entity)
            result = db.session.execute(stmt).mappings().all()
            if not result:
                return []
            return [StatisticsPo(**item) for item in result]
        except Exception as e:
            print(f"获取地图统计信息失败: {e}")
            return []

    @classmethod
    def city_level_statistics(cls, statistics_entity) -> List[StatisticsPo]:
        """
        城市等级统计
        select count(*)     as value,
           avg(salary_month_avg) as avg,
           min(salary_month_avg) as min,
           max(salary_month_avg) as max,
           city_level as name
        from tb_recruit_info
        where full_address is not null
        group by name
        """
        try:
            stmt = select(func.count("*").label("value"),
                          func.avg(RecruitInfoPo.salary_month_avg).label("avg"),
                          func.max(RecruitInfoPo.salary_month_avg).label("max"),
                          func.min(RecruitInfoPo.salary_month_avg).label("min"),
                          RecruitInfoPo.city_level.label("name")
                          ).select_from(RecruitInfoPo).group_by("name").order_by("value")
            stmt = cls.build_where(stmt, statistics_entity)
            result = db.session.execute(stmt).mappings().all()
            if not result:
                return []
            return [StatisticsPo(**item) for item in result]
        except Exception as e:
            print(f"获取城市等级统计信息失败: {e}")
            return []


    @classmethod
    def post_type_statistics(cls, statistics_entity)->List[StatisticsPo]:
        """
        岗位统计
        select count(*)     as value,
           avg(salary_month_avg) as avg,
           min(salary_month_avg) as min,
           max(salary_month_avg) as max,
           post_type as name
        from tb_recruit_info
        where full_address is not null
        group by name
        """
        try:
            stmt = select(func.count("*").label("value"),
                          func.avg(RecruitInfoPo.salary_month_avg).label("avg"),
                          func.max(RecruitInfoPo.salary_month_avg).label("max"),
                          func.min(RecruitInfoPo.salary_month_avg).label("min"),
                          RecruitInfoPo.post_type.label("name")
                          ).select_from(RecruitInfoPo).group_by("name").order_by("value")
            stmt = cls.build_where(stmt, statistics_entity)
            result = db.session.execute(stmt).mappings().all()
            if not result:
                return []
            return [StatisticsPo(**item) for item in result]
        except Exception as e:
            print(f"获取岗位统计信息失败: {e}")
            return []
