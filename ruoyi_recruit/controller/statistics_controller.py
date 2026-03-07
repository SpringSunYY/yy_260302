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
    if (statistics_entity.address is None
            or statistics_entity.address == "中华人民共和国"
            or statistics_entity.address == ""
            or statistics_entity.address == "全国"):
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
    if (statistics_entity.address is None
            or statistics_entity.address == "中华人民共和国"
            or statistics_entity.address == ""
            or statistics_entity.address == "全国"):
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
    if (statistics_entity.address is None
            or statistics_entity.address == "中华人民共和国"
            or statistics_entity.address == ""
            or statistics_entity.address == "全国"):
        statistics_entity.address = None
    return AjaxResponse.from_success(data=service.post_type_statistics(statistics_entity))


# 学历
@gen.route('/education', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('recruit:recruitInfo:statistics'))
@JsonSerializer()
def education_statistics(request: StatisticsRequest):
    statistics_entity = StatisticsRequest()
    # 转换dto到Entity对象
    for attr in request.model_fields.keys():
        if hasattr(statistics_entity, attr):
            setattr(statistics_entity, attr, getattr(request, attr))
    if (statistics_entity.address is None
            or statistics_entity.address == "中华人民共和国"
            or statistics_entity.address == ""
            or statistics_entity.address == "全国"):
        statistics_entity.address = None
    return AjaxResponse.from_success(data=service.education_statistics(statistics_entity))


# 企业规模
@gen.route('/enterpriseSize', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('recruit:recruitInfo:statistics'))
@JsonSerializer()
def enterprise_size_statistics(request: StatisticsRequest):
    statistics_entity = StatisticsRequest()
    # 转换dto到Entity对象
    for attr in request.model_fields.keys():
        if hasattr(statistics_entity, attr):
            setattr(statistics_entity, attr, getattr(request, attr))
    if (statistics_entity.address is None
            or statistics_entity.address == "中华人民共和国"
            or statistics_entity.address == ""
            or statistics_entity.address == "全国"):
        statistics_entity.address = None
    return AjaxResponse.from_success(data=service.enterprise_size_statistics(statistics_entity))


# 经验
@gen.route('/experience', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('recruit:recruitInfo:statistics'))
@JsonSerializer()
def experience_statistics(request: StatisticsRequest):
    statistics_entity = StatisticsRequest()
    # 转换dto到Entity对象
    for attr in request.model_fields.keys():
        if hasattr(statistics_entity, attr):
            setattr(statistics_entity, attr, getattr(request, attr))
    if (statistics_entity.address is None
            or statistics_entity.address == "中华人民共和国"
            or statistics_entity.address == ""
            or statistics_entity.address == "全国"):
        statistics_entity.address = None
    return AjaxResponse.from_success(data=service.experience_statistics(statistics_entity))

#融资情况
@gen.route('/financingSituation', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('recruit:recruitInfo:statistics'))
@JsonSerializer()
def financing_situation_statistics(request: StatisticsRequest):
    statistics_entity = StatisticsRequest()
    # 转换dto到Entity对象
    for attr in request.model_fields.keys():
        if hasattr(statistics_entity, attr):
            setattr(statistics_entity, attr, getattr(request, attr))
    if (statistics_entity.address is None
            or statistics_entity.address == "中华人民共和国"
            or statistics_entity.address == ""
            or statistics_entity.address == "全国"):
        statistics_entity.address = None
    return AjaxResponse.from_success(data=service.financing_situation_statistics(statistics_entity))

# 主营业务
@gen.route('/mainBusiness', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('recruit:recruitInfo:statistics'))
@JsonSerializer()
def main_business_statistics(request: StatisticsRequest):
    statistics_entity = StatisticsRequest()
    # 转换dto到Entity对象
    for attr in request.model_fields.keys():
        if hasattr(statistics_entity, attr):
            setattr(statistics_entity, attr, getattr(request, attr))
    if (statistics_entity.address is None
            or statistics_entity.address == "中华人民共和国"
            or statistics_entity.address == ""
            or statistics_entity.address == "全国"):
        statistics_entity.address = None
    return AjaxResponse.from_success(data=service.main_business_statistics(statistics_entity))


# 技能
@gen.route('/skill', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('recruit:recruitInfo:statistics'))
@JsonSerializer()
def skill_statistics(request: StatisticsRequest):
    statistics_entity = StatisticsRequest()
    # 转换dto到Entity对象
    for attr in request.model_fields.keys():
        if hasattr(statistics_entity, attr):
            setattr(statistics_entity, attr, getattr(request, attr))
    if (statistics_entity.address is None
            or statistics_entity.address == "中华人民共和国"
            or statistics_entity.address == ""
            or statistics_entity.address == "全国"):
        statistics_entity.address = None
    return AjaxResponse.from_success(data=service.skill_statistics(statistics_entity))


# 工资
@gen.route('/salary', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('recruit:recruitInfo:statistics'))
@JsonSerializer()
def salary_statistics(request: StatisticsRequest):
    statistics_entity = StatisticsRequest()
    # 转换dto到Entity对象
    for attr in request.model_fields.keys():
        if hasattr(statistics_entity, attr):
            setattr(statistics_entity, attr, getattr(request, attr))
    if (statistics_entity.address is None
            or statistics_entity.address == "中华人民共和国"
            or statistics_entity.address == ""
            or statistics_entity.address == "全国"):
        statistics_entity.address = None
    return AjaxResponse.from_success(data=service.salary_statistics(statistics_entity))


#岗位排行
@gen.route('/postRank', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('recruit:recruitInfo:statistics'))
@JsonSerializer()
def post_rank_statistics(request: StatisticsRequest):
    statistics_entity = StatisticsRequest()
    # 转换dto到Entity对象
    for attr in request.model_fields.keys():
        if hasattr(statistics_entity, attr):
            setattr(statistics_entity, attr, getattr(request, attr))
    if (statistics_entity.address is None
            or statistics_entity.address == "中华人民共和国"
            or statistics_entity.address == ""
            or statistics_entity.address == "全国"):
        statistics_entity.address = None
    return AjaxResponse.from_success(data=service.post_rank_statistics(statistics_entity))
