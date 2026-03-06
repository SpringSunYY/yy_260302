from ruoyi_common.base.model import AjaxResponse
from ruoyi_common.descriptor.validator import QueryValidator
from ruoyi_framework.descriptor.permission import HasPerm, PreAuthorize
from ruoyi_recruit.controller import statistics_info as statistics_bp
from ruoyi_recruit.domain.statistics.dto import StatisticsRequest
from ruoyi_recruit.service.statistics_service import StatisticsService
from ruoyi_common.descriptor.serializer import JsonSerializer

gen = statistics_bp
service = StatisticsService()
"""招聘信息数据分析统计"""

"""地图数据分析"""


@gen.route('/map', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('recruit:recruitInfo:statistics'))
@JsonSerializer()
def map_statistics(request: StatisticsRequest):
    statistics_entity = StatisticsRequest()
    # 转换dto到Entity对象
    for attr in request.model_fields.keys():
        if hasattr(statistics_entity, attr):
            setattr(statistics_entity, attr, getattr(request, attr))
    if statistics_entity.address is None or statistics_entity.address == "中华人民共和国":
        statistics_entity.address = None
    return AjaxResponse.from_success(data=service.map_statistics(statistics_entity))


# 城市等级
@gen.route('/cityLevel', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('recruit:recruitInfo:statistics'))
@JsonSerializer()
def city_level_statistics(request: StatisticsRequest):
    statistics_entity = StatisticsRequest()
    # 转换dto到Entity对象
    for attr in request.model_fields.keys():
        if hasattr(statistics_entity, attr):
            setattr(statistics_entity, attr, getattr(request, attr))
    if statistics_entity.address is None or statistics_entity.address == "中华人民共和国":
        statistics_entity.address = None
    return AjaxResponse.from_success(data=service.city_level_statistics(statistics_entity))

# 岗位
@gen.route('/postType', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('recruit:recruitInfo:statistics'))
@JsonSerializer()
def post_type_statistics(request: StatisticsRequest):
    statistics_entity = StatisticsRequest()
    # 转换dto到Entity对象
    for attr in request.model_fields.keys():
        if hasattr(statistics_entity, attr):
            setattr(statistics_entity, attr, getattr(request, attr))
    if statistics_entity.address is None or statistics_entity.address == "中华人民共和国":
        statistics_entity.address = None
    return AjaxResponse.from_success(data=service.post_type_statistics(statistics_entity))
