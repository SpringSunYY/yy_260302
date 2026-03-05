# -*- coding: utf-8 -*-
# @Author  : YY
# @FileName: recommend_info_service.py
# @Time    : 2026-03-02 16:56:43

import json
import math
from collections import defaultdict
from datetime import datetime
from typing import List, Optional, Dict, Tuple

from ruoyi_common.constant import HttpStatus, ConfigConstants
from ruoyi_common.exception import ServiceException
from ruoyi_common.utils.base import LogUtil
from ruoyi_recruit.domain.entity import RecommendInfo, LikeInfo, ViewInfo, RecruitInfo
from ruoyi_recruit.mapper.like_info_mapper import LikeInfoMapper
from ruoyi_recruit.mapper.recommend_info_mapper import RecommendInfoMapper
from ruoyi_recruit.mapper.recruit_info_mapper import RecruitInfoMapper
from ruoyi_recruit.mapper.view_info_mapper import ViewInfoMapper
from ruoyi_system.service.sys_config import SysConfigService


class RecommendInfoService:
    """招聘推荐服务类"""


    # ==================== 通用方法 ====================

    @classmethod
    def _get_config_value(cls, key: str, default_value: str = "0") -> str:
        """获取配置值"""
        value = SysConfigService.select_config_by_key(key)
        return value if value is not None else default_value

    @classmethod
    def _get_default_weights(cls) -> Dict[str, float]:
        """获取默认权重配置"""
        return {
            'postType': float(cls._get_config_value(ConfigConstants.CONFIG_KEY_POST_TYPE_WEIGHT, "20.0")),
            'cityLevel': float(cls._get_config_value(ConfigConstants.CONFIG_KEY_CITY_LEVEL_WEIGHT, "10.0")),
            'province': float(cls._get_config_value(ConfigConstants.CONFIG_KEY_PROVINCE_WEIGHT, "15.0")),
            'city': float(cls._get_config_value(ConfigConstants.CONFIG_KEY_CITY_WEIGHT, "20.0")),
            'experience': float(cls._get_config_value(ConfigConstants.CONFIG_KEY_EXPERIENCE_WEIGHT, "10.0")),
            'education': float(cls._get_config_value(ConfigConstants.CONFIG_KEY_EDUCATION_WEIGHT, "10.0")),
            'mainBusiness': float(cls._get_config_value(ConfigConstants.CONFIG_KEY_MAIN_BUSINESS_WEIGHT, "5.0")),
            'enterpriseSize': float(cls._get_config_value(ConfigConstants.CONFIG_KEY_ENTERPRISE_SIZE_WEIGHT, "5.0")),
            'financing': float(cls._get_config_value(ConfigConstants.CONFIG_KEY_FINANCING_WEIGHT, "3.0")),
            'salary': float(cls._get_config_value(ConfigConstants.CONFIG_KEY_SALARY_WEIGHT, "2.0"))
        }

    @classmethod
    def _get_salary_range(cls) -> List[int]:
        """获取薪资区间配置"""
        salary_range_str = cls._get_config_value(ConfigConstants.CONFIG_KEY_SALARY_RANGE, "6000,8000,10000,15000,20000")
        try:
            return [int(x.strip()) for x in salary_range_str.split(',')]
        except ValueError:
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
        # 格式化每个区间值
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
    def _calculate_time_weight(cls, create_time, now, time_decay_factor) -> float:
        """计算时间权重"""
        if not create_time:
            return 0.5
        days_diff = (now - create_time).days
        if days_diff <= 0:
            return 1.0
        return math.pow(time_decay_factor, days_diff)

    @classmethod
    def _merge_main_business(cls, prefs: Dict[str, float]) -> Dict[str, float]:
        """
        合并主营业务偏好，将分割后的值按原始组合聚合
        例如：{"计算机软件": 4.0, "互联网": 4.0} -> {"计算机软件/互联网": 8.0}
        """
        if not prefs:
            return {}

        # 按分割后的单项统计
        single_prefs = defaultdict(float)
        for key, value in prefs.items():
            parts = [p.strip() for p in key.split('/') if p.strip()]
            if len(parts) == 1:
                single_prefs[parts[0]] += value

        # 找出能组合的项
        merged = {}
        used = set()

        for key, value in prefs.items():
            parts = [p.strip() for p in key.split('/') if p.strip()]
            if len(parts) > 1:
                # 多项组合保留原样
                if key not in used:
                    merged[key] = value
                    used.add(key)
            else:
                # 单项检查是否能合并
                if parts[0] not in used:
                    # 尝试找其他可以组合的
                    other_parts = []
                    for other_key, other_value in prefs.items():
                        if other_key != key:
                            other_parts_key = [p.strip() for p in other_key.split('/') if p.strip()]
                            if len(other_parts_key) == 1 and parts[0] in other_parts_key:
                                if other_key not in used:
                                    combined = f"{parts[0]}/{other_parts_key[0]}"
                                    merged[combined] = value + other_value
                                    used.add(key)
                                    used.add(other_key)
                                    break
                    else:
                        # 无法合并，保留单项
                        if parts[0] not in used:
                            merged[parts[0]] = value
                            used.add(parts[0])

        return merged

    @classmethod
    def _calculate_dimension_similarity_fast(cls, dimension: str, user_preference: Dict[str, float],
                                             total_weight: float) -> float:
        """计算维度相似度分数（优化版）"""
        if not dimension or total_weight == 0:
            return 0.0

        items = set(item.strip() for item in dimension.split('/') if item.strip())
        if not items:
            return 0.0

        matched_score = 0.0
        match_count = 0

        for item in items:
            if item in user_preference:
                matched_score += user_preference[item]
                match_count += 1

        if match_count == 0:
            return 0.0

        similarity = matched_score / total_weight

        if match_count > 1:
            diversity_bonus = 0.1 * (match_count - 1)
            similarity = min(similarity * (1 + diversity_bonus), 1.0)

        if match_count == len(items) and len(items) > 1:
            similarity = min(similarity * 1.2, 1.0)

        return min(similarity, 1.0)

    # ==================== 对外接口 ====================

    @classmethod
    def select_recommend_info_list(cls, recommend_info: RecommendInfo) -> List[RecommendInfo]:
        """查询用户推荐列表"""
        return RecommendInfoMapper.select_recommend_info_list(recommend_info)

    @classmethod
    def select_recommend_info_by_id(cls, id: int) -> Optional[RecommendInfo]:
        """根据ID查询用户推荐"""
        return RecommendInfoMapper.select_recommend_info_by_id(id)

    @classmethod
    def insert_recommend_info(cls, recommend_info: RecommendInfo) -> int:
        """新增用户推荐"""
        return RecommendInfoMapper.insert_recommend_info(recommend_info)

    @classmethod
    def update_recommend_info(cls, recommend_info: RecommendInfo) -> int:
        """修改用户推荐"""
        return RecommendInfoMapper.update_recommend_info(recommend_info)

    @classmethod
    def delete_recommend_info_by_ids(cls, ids: List[int]) -> int:
        """批量删除用户推荐"""
        return RecommendInfoMapper.delete_recommend_info_by_ids(ids)

    @classmethod
    def import_recommend_info(cls, recommend_info_list: List[RecommendInfo], is_update: bool = False) -> str:
        """导入用户推荐数据"""
        if not recommend_info_list:
            raise ServiceException("导入用户推荐数据不能为空")

        success_count = 0
        fail_count = 0
        success_msg = ""
        fail_msg = ""

        for recommend_info in recommend_info_list:
            try:
                display_value = recommend_info
                display_value = getattr(recommend_info, "id", display_value)
                existing = None
                if recommend_info.id is not None:
                    existing = RecommendInfoMapper.select_recommend_info_by_id(recommend_info.id)
                if existing:
                    if is_update:
                        result = RecommendInfoMapper.update_recommend_info(recommend_info)
                    else:
                        fail_count += 1
                        fail_msg += f"<br/> 第{fail_count}条数据，已存在：{display_value}"
                        continue
                else:
                    result = RecommendInfoMapper.insert_recommend_info(recommend_info)

                if result > 0:
                    success_count += 1
                    success_msg += f"<br/> 第{success_count}条数据，操作成功：{display_value}"
                else:
                    fail_count += 1
                    success_msg += f"<br/> 第{success_count}条数据，操作失败：{display_value}"
            except Exception as e:
                fail_count += 1
                fail_msg += f"<br/> 第{fail_count}条数据，导入失败，原因：{e.__class__.__name__}"
                LogUtil.logger.error(f"导入用户推荐失败，原因：{e}")

        if fail_count > 0:
            if success_msg:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{success_msg}<br/>" + fail_msg
            else:
                fail_msg = f"导入成功{success_count}条，失败{fail_count}条。{fail_msg}"
            raise ServiceException(fail_msg)
        success_msg = f"恭喜您，数据已全部导入成功！共 {success_count} 条，数据如下：" + success_msg
        return success_msg

    # ==================== 核心推荐算法 ====================

    @classmethod
    def get_recommend_content(cls, user_id: int, user_name: str = None,
                             page_num: int = 1, page_size: int = 10) -> Dict:
        """
        为指定用户自动生成/更新推荐模型
        """
        try:
            recommend_obj = None
            LogUtil.logger.info(f"[推荐] 用户={user_id}, pageNum={page_num}, pageSize={page_size}")

            # 第一页时检查是否需要生成/更新推荐模型
            if page_num == 1:
                should_generate = cls._should_generate_new_recommendations(user_id)
                LogUtil.logger.info(f"[推荐] 用户={user_id}, 需要生成新推荐={should_generate}")
                if should_generate:
                    recommend_obj = cls._generate_new_recommendations(user_id, user_name)
                    LogUtil.logger.info(f"[推荐] 用户={user_id}, 新推荐生成完成")

            if recommend_obj is None or recommend_obj.id is None:
                recommend_obj = RecommendInfoMapper.select_user_recommend_history(user_id)
                LogUtil.logger.info(f"[推荐] 用户={user_id}, 从历史记录获取recommend_obj={recommend_obj}")

            if not recommend_obj or not recommend_obj.content:
                LogUtil.logger.info(f"用户 {user_id} 没有推荐记录")
                return {'rows': [], 'total': 0}

            content_data = json.loads(recommend_obj.content)
            LogUtil.logger.debug(f"[推荐] 用户={user_id}")

            recruit_scores = content_data.get('recruit_scores', [])
            total_count = content_data.get('total', len(recruit_scores))
            print(f"[推荐] 用户={user_id}, 总数={total_count}, 推荐数={len(recruit_scores)}")
            if not isinstance(recruit_scores, list):
                LogUtil.logger.error(f"用户 {user_id} 的推荐内容格式错误")
                return {'rows': [], 'total': 0}

            # 分页处理
            start_idx = (page_num - 1) * page_size
            end_idx = start_idx + page_size
            page_recruit_scores = recruit_scores[start_idx:end_idx]

            if not page_recruit_scores:
                LogUtil.logger.info(f"用户 {user_id} 没有推荐内容")
                return {'rows': [], 'total': 0}

            page_recruit_ids = [item[0] for item in page_recruit_scores]
            recruit_list = RecruitInfoMapper.select_recruit_info_by_ids(page_recruit_ids)

            recruit_dict = {recruit.recruit_id: recruit for recruit in recruit_list}

            result_list = []
            for recruit_id, score in page_recruit_scores:
                recruit = recruit_dict.get(recruit_id)
                if not recruit:
                    continue

                recruit_data = {
                    'recruitId': recruit.recruit_id or 0,
                    'post': recruit.post or '',
                    'postType': recruit.post_type or '',
                    'cityLevel': recruit.city_level or '',
                    'province': recruit.province or '',
                    'city': recruit.city or '',
                    'location': recruit.location or '',
                    'salaryRange': recruit.salary_range or '',
                    'salaryMin': recruit.salary_min or 0.0,
                    'salaryMax': recruit.salary_max or 0.0,
                    'salaryMonthAvg': recruit.salary_month_avg or 0.0,
                    'experienceRequired': recruit.experience_required or '',
                    'educationRequired': recruit.education_required or '',
                    'skillRequired': recruit.skill_required or '',
                    'enterpriseName': recruit.enterprise_name or '',
                    'mainBusiness': recruit.main_business or '',
                    'enterpriseSize': recruit.enterprise_size or '',
                    'financingSituation': recruit.financing_situation or ''
                }
                result_list.append(recruit_data)

            return {'rows': result_list, 'total': total_count}

        except Exception as e:
            LogUtil.logger.error(f"获取用户 {user_id} 推荐时出错: {e}")
            return {'rows': [], 'total': 0}

    @classmethod
    def _should_generate_new_recommendations(cls, user_id: int) -> bool:
        """判断是否应该生成新的推荐模型"""
        try:
            recommend = RecommendInfoMapper.select_user_recommend_history(user_id)
            if recommend is None:
                return True

            last_recommend_time = recommend.create_time

            view_new_record_num = int(cls._get_config_value(ConfigConstants.CONFIG_KEY_VIEW_NEW_RECORD_NUM, "5"))
            like_new_record_num = int(cls._get_config_value(ConfigConstants.CONFIG_KEY_LIKE_NEW_RECORD_NUM, "1"))

            new_views = ViewInfoMapper.select_user_latest_views_after_time(user_id, last_recommend_time, view_new_record_num)
            new_likes = LikeInfoMapper.select_user_latest_likes_after_time(user_id, last_recommend_time, like_new_record_num)

            if len(new_views) >= view_new_record_num or len(new_likes) >= like_new_record_num:
                return True
            else:
                return False

        except Exception as e:
            LogUtil.logger.error(f"检查用户 {user_id} 是否需要新推荐时出错: {e}")
            return False

    @classmethod
    def _generate_new_recommendations(cls, user_id: int, user_name: str = None) -> Optional[RecommendInfo]:
        """生成新的推荐模型"""
        now = datetime.now()

        # 获取配置
        weights = cls._get_default_weights()
        time_decay_factor = float(cls._get_config_value(ConfigConstants.CONFIG_KEY_TIME_DECAY_FACTOR, "0.95"))
        view_num = int(cls._get_config_value(ConfigConstants.CONFIG_KEY_VIEW_RECORD_NUM, "30"))
        like_num = int(cls._get_config_value(ConfigConstants.CONFIG_KEY_LIKE_RECORD_NUM, "5"))
        recommend_num = int(cls._get_config_value(ConfigConstants.CONFIG_KEY_RECOMMEND_NUM, "1000"))
        like_score = float(cls._get_config_value(ConfigConstants.CONFIG_KEY_LIKE_SCORE, "2.0"))
        view_score = float(cls._get_config_value(ConfigConstants.CONFIG_KEY_VIEW_SCORE, "1.0"))
        salary_range = cls._get_salary_range()

        # 获取浏览和点赞记录
        views = ViewInfoMapper.select_user_latest_views(user_id, view_num)
        likes = LikeInfoMapper.select_user_latest_likes(user_id, like_num)

        # 计算用户偏好
        user_preference = cls._calculate_user_preference(
            user_views=views,
            user_likes=likes,
            time_decay_factor=time_decay_factor,
            like_score=like_score,
            view_score=view_score,
            salary_range=salary_range,
            now=now
        )

        # 根据用户偏好获取候选岗位
        recruit_candidates = cls._get_candidate_recruits(user_preference, weights, recommend_num)

        # 计算岗位分数
        all_candidate_recruits = cls._calculate_recruit_score(
            recruit_list=recruit_candidates,
            user_preference=user_preference,
            weights=weights,
            salary_range=salary_range,
            recommend_num=recommend_num
        )

        # 构建结果集
        recruit_scores = []
        for recruit, score in all_candidate_recruits:
            recruit_scores.append([recruit.recruit_id, round(score, 6)])

        recommend_content = json.dumps({
            "total": len(recruit_scores),
            "recruit_scores": recruit_scores,
            "create_time": now.strftime("%Y-%m-%d %H:%M:%S"),
        }, ensure_ascii=False, separators=(',', ':'))

        # 处理用户偏好模型（驼峰命名）
        model_data = {}
        # 维度名称映射到驼峰
        dimension_mapping = {
            'postType': 'postTypeModel',
            'cityLevel': 'cityLevelModel',
            'province': 'provinceModel',
            'city': 'cityModel',
            'experience': 'experienceModel',
            'education': 'educationModel',
            'mainBusiness': 'mainBusinessModel',
            'enterpriseSize': 'enterpriseSizeModel',
            'financing': 'financingModel',
            'salary': 'salaryModel'
        }

        for dimension, prefs in user_preference.items():
            if dimension.startswith('_'):
                continue
            total_weight = sum(prefs.values())
            model_key = dimension_mapping.get(dimension, dimension)
            if total_weight > 0:
                # 主营业务需要按 / 分割后的值分组显示
                if dimension == 'mainBusiness':
                    # 按 / 分割的组合键来聚合权重
                    combined_prefs = defaultdict(float)
                    for key, value in prefs.items():
                        combined_prefs[key] += value
                    # 将分割后的值重新组合
                    merged_prefs = cls._merge_main_business(combined_prefs)
                    model_data[model_key] = [
                        {'name': key, 'value': round(value, 4)} for key, value in merged_prefs.items()
                    ]
                else:
                    model_data[model_key] = [
                        {'name': key, 'value': round(value, 4)} for key, value in prefs.items()
                    ]
            else:
                model_data[model_key] = []

        recommend_model = json.dumps({
            'algorithm': '多维度协同过滤推荐算法',
            'weights': weights,
            'timeDecayFactor': time_decay_factor,
            'viewRecordsCount': len(views) if views else 0,
            'likeRecordsCount': len(likes) if likes else 0,
            'recommendNum': recommend_num,
            'total': len(recruit_scores),
            'createTime': now.strftime("%Y-%m-%d %H:%M:%S"),
            'model': model_data
        }, ensure_ascii=False, separators=(',', ':'))

        recommend = RecommendInfo()
        recommend.user_id = user_id
        recommend.user_name = user_name
        recommend.content = recommend_content
        recommend.model_info = recommend_model
        recommend.create_time = now

        cls.insert_recommend_info(recommend)
        return recommend

    @classmethod
    def _get_candidate_recruits(cls, user_preference: Dict[str, Dict[str, float]],
                               weights: Dict[str, float],
                               limit: int) -> List[RecruitInfo]:
        """
        根据用户偏好获取候选岗位
        """
        # 从用户最偏好的维度中选择关键词
        candidate_recruits = []

        # 获取偏好最高的几个维度
        top_dims = []
        for dim, prefs in user_preference.items():
            if dim.startswith('_'):
                continue
            if prefs:
                top_value = max(prefs.values()) if prefs else 0
                if top_value > 0:
                    top_dims.append((dim, prefs, top_value))

        # 按权重排序，取前3个维度
        top_dims.sort(key=lambda x: x[2], reverse=True)
        top_dims = top_dims[:3]

        if not top_dims:
            # 没有偏好数据，返回热门岗位
            return RecruitInfoMapper.select_all_recruit_info(limit)

        # 根据偏好维度查询候选岗位
        for dim, prefs, _ in top_dims:
            if not prefs:
                continue
            # 取偏好最高的几个值
            top_values = sorted(prefs.items(), key=lambda x: x[1], reverse=True)[:3]
            top_names = [v[0] for v in top_values]

            # 根据不同维度构建查询条件
            if dim == 'postType':
                for name in top_names:
                    recruits = RecruitInfoMapper.select_recruit_info_by_post_type(name)
                    candidate_recruits.extend(recruits)
            elif dim == 'province':
                for name in top_names:
                    recruits = RecruitInfoMapper.select_recruit_info_by_province(name)
                    candidate_recruits.extend(recruits)
            elif dim == 'city':
                for name in top_names:
                    recruits = RecruitInfoMapper.select_recruit_info_by_city(name)
                    candidate_recruits.extend(recruits)

        # 去重
        if candidate_recruits:
            seen = set()
            unique_recruits = []
            for r in candidate_recruits:
                if r.recruit_id not in seen:
                    seen.add(r.recruit_id)
                    unique_recruits.append(r)
            return unique_recruits[:limit]
        else:
            # 如果没有匹配到，返回热门岗位
            return RecruitInfoMapper.select_all_recruit_info(limit)

    @classmethod
    def _calculate_user_preference(cls, user_views, user_likes, time_decay_factor,
                                   like_score: float, view_score: float,
                                   salary_range: List[int], now: datetime) -> Dict[str, Dict[str, float]]:
        """计算用户偏好"""
        preference = {
            'postType': defaultdict(float),
            'cityLevel': defaultdict(float),
            'province': defaultdict(float),
            'city': defaultdict(float),
            'experience': defaultdict(float),
            'education': defaultdict(float),
            'mainBusiness': defaultdict(float),
            'enterpriseSize': defaultdict(float),
            'financing': defaultdict(float),
            'salary': defaultdict(float)
        }

        # 处理浏览记录
        if user_views:
            for view in user_views:
                time_weight = cls._calculate_time_weight(view.create_time, now, time_decay_factor)
                score_weight = view.score if view.score is not None else view_score
                total_weight = time_weight * score_weight
                cls._accumulate_preference(preference, view, total_weight, salary_range)

        # 处理点赞记录
        if user_likes:
            for like in user_likes:
                time_weight = cls._calculate_time_weight(like.create_time, now, time_decay_factor)
                score_weight = like.score if like.score is not None else like_score
                total_weight = time_weight * score_weight
                cls._accumulate_preference(preference, like, total_weight, salary_range)

        return dict(preference)

    @classmethod
    def _accumulate_preference(cls, preference: Dict[str, Dict[str, float]],
                               record: ViewInfo | LikeInfo, weight: float,
                               salary_range: List[int]):
        """累加用户偏好"""
        if record.post_type:
            preference['postType'][record.post_type] += weight
        if record.city_level:
            preference['cityLevel'][record.city_level] += weight
        if record.province:
            preference['province'][record.province] += weight
        if record.city:
            preference['city'][record.city] += weight
        if record.experience_required:
            preference['experience'][record.experience_required] += weight
        if record.education_required:
            preference['education'][record.education_required] += weight
        # 主营业务支持 / 分割，多个值分别累加
        if record.main_business:
            for mb in record.main_business.split('/'):
                mb = mb.strip()
                if mb:
                    preference['mainBusiness'][mb] += weight
        if record.enterprise_size:
            preference['enterpriseSize'][record.enterprise_size] += weight
        if record.financing_situation:
            preference['financing'][record.financing_situation] += weight
        # 薪资区间处理
        if record.salary_month_avg:
            salary_label = cls._get_salary_range_label(record.salary_month_avg, salary_range)
            preference['salary'][salary_label] += weight

    @classmethod
    def _calculate_recruit_score(cls, recruit_list: List[RecruitInfo] = None,
                                user_preference: Dict[str, Dict[str, float]] = None,
                                weights: Dict[str, float] = None,
                                salary_range: List[int] = None,
                                recommend_num: int = 1000) -> List[Tuple[RecruitInfo, float]]:
        """计算岗位得分"""
        candidates = []

        # 预计算各维度权重总和
        pref_totals = {k: sum(v.values()) for k, v in user_preference.items() if not k.startswith('_')}

        for recruit in recruit_list:
            similarity_score = cls._calculate_similarity_score(
                recruit, user_preference, weights, salary_range, pref_totals
            )
            if similarity_score > 0:
                candidates.append((recruit, similarity_score))

        candidates.sort(key=lambda x: x[1], reverse=True)
        min_score_threshold = 1
        filtered_recruits = [item for item in candidates if item[1] >= min_score_threshold][:recommend_num]

        if not filtered_recruits:
            LogUtil.logger.info("没有找到符合条件的岗位")
            return []

        return filtered_recruits

    @classmethod
    def _calculate_similarity_score(cls, recruit: RecruitInfo,
                                    user_preference: Dict[str, Dict[str, float]],
                                    weights: Dict[str, float],
                                    salary_range: List[int],
                                    pref_totals: Dict[str, float]) -> float:
        """计算相似度分数"""
        total_score = 0

        # 岗位大类
        if recruit.post_type and pref_totals.get('postType', 0) > 0:
            score = cls._calculate_dimension_similarity_fast(
                recruit.post_type, user_preference['postType'], pref_totals['postType']
            )
            total_score += score * weights.get('postType', 0)

        # 城市等级
        if recruit.city_level and pref_totals.get('cityLevel', 0) > 0:
            score = cls._calculate_dimension_similarity_fast(
                recruit.city_level, user_preference['cityLevel'], pref_totals['cityLevel']
            )
            total_score += score * weights.get('cityLevel', 0)

        # 省份
        if recruit.province and pref_totals.get('province', 0) > 0:
            score = cls._calculate_dimension_similarity_fast(
                recruit.province, user_preference['province'], pref_totals['province']
            )
            total_score += score * weights.get('province', 0)

        # 城市
        if recruit.city and pref_totals.get('city', 0) > 0:
            score = cls._calculate_dimension_similarity_fast(
                recruit.city, user_preference['city'], pref_totals['city']
            )
            total_score += score * weights.get('city', 0)

        # 经验要求
        if recruit.experience_required and pref_totals.get('experience', 0) > 0:
            score = cls._calculate_dimension_similarity_fast(
                recruit.experience_required, user_preference['experience'], pref_totals['experience']
            )
            total_score += score * weights.get('experience', 0)

        # 学历要求
        if recruit.education_required and pref_totals.get('education', 0) > 0:
            score = cls._calculate_dimension_similarity_fast(
                recruit.education_required, user_preference['education'], pref_totals['education']
            )
            total_score += score * weights.get('education', 0)

        # 主营业务（支持 / 分割匹配）
        if recruit.main_business and pref_totals.get('mainBusiness', 0) > 0:
            # 获取用户偏好中所有的业务类型
            mb_prefs = user_preference.get('mainBusiness', {})
            # 按 / 分割岗位的主营业务，分别匹配
            recruit_mbs = [mb.strip() for mb in recruit.main_business.split('/') if mb.strip()]
            total_mb_score = 0.0
            matched_count = 0
            for mb in recruit_mbs:
                if mb in mb_prefs:
                    total_mb_score += mb_prefs[mb] / pref_totals['mainBusiness']
                    matched_count += 1
            if matched_count > 0:
                # 有匹配，加上权重分数
                mb_similarity = total_mb_score * (1 + 0.1 * (matched_count - 1)) if matched_count > 1 else total_mb_score
                total_score += mb_similarity * weights.get('mainBusiness', 0)

        # 企业规模
        if recruit.enterprise_size and pref_totals.get('enterpriseSize', 0) > 0:
            score = cls._calculate_dimension_similarity_fast(
                recruit.enterprise_size, user_preference['enterpriseSize'], pref_totals['enterpriseSize']
            )
            total_score += score * weights.get('enterpriseSize', 0)

        # 融资情况
        if recruit.financing_situation and pref_totals.get('financing', 0) > 0:
            score = cls._calculate_dimension_similarity_fast(
                recruit.financing_situation, user_preference['financing'], pref_totals['financing']
            )
            total_score += score * weights.get('financing', 0)

        # 薪资
        if recruit.salary_month_avg and pref_totals.get('salary', 0) > 0:
            salary_label = cls._get_salary_range_label(recruit.salary_month_avg, salary_range)
            score = cls._calculate_dimension_similarity_fast(
                salary_label, user_preference['salary'], pref_totals['salary']
            )
            total_score += score * weights.get('salary', 0)

        return total_score

