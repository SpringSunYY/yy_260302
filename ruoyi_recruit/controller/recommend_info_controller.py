from typing import List

from flask import g, request
from flask_login import login_required
from pydantic import BeforeValidator
from typing_extensions import Annotated
from werkzeug.datastructures import FileStorage

from ruoyi_common.base.model import AjaxResponse, TableResponse
from ruoyi_common.constant import HttpStatus
from ruoyi_common.descriptor.serializer import BaseSerializer, JsonSerializer
from ruoyi_common.descriptor.validator import QueryValidator, BodyValidator, PathValidator, FileDownloadValidator, \
    FileUploadValidator
from ruoyi_common.domain.enum import BusinessType
from ruoyi_common.utils.base import ExcelUtil
from ruoyi_common.utils.security_util import get_user_id, get_username
from ruoyi_framework.descriptor.log import Log
from ruoyi_framework.descriptor.permission import HasPerm, PreAuthorize, AnyPerm
from ruoyi_recruit.controller import recommend_info as recommend_info_bp
from ruoyi_recruit.domain.entity import RecommendInfo
from ruoyi_recruit.service.recommend_info_service import RecommendInfoService

# 使用 controller/__init__.py 中定义的蓝图
gen = recommend_info_bp

recommend_info_service = RecommendInfoService()


def _clear_page_context():
    if hasattr(g, "criterian_meta"):
        g.criterian_meta.page = None


@gen.route('/content', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(AnyPerm('recruit:recruitInfo:list,recruit:recruitInfo:query'))
@JsonSerializer()
def get_recommend_content():
    """查询用户推荐列表"""
    user_id = get_user_id()
    user_name = get_username()
    page_num = request.args.get('pageNum', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    result = recommend_info_service.get_recommend_content(user_id, user_name, page_num, page_size)
    return {'code': HttpStatus.SUCCESS,
            'msg': '查询成功',
            'rows': result.get('rows', []),
            'total': result.get('total', 0)
            }


@gen.route('/list', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('recruit:recommendInfo:list'))
@JsonSerializer()
def recommend_info_list(dto: RecommendInfo):
    """查询用户推荐列表"""
    recommend_info_entity = RecommendInfo()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(recommend_info_entity, attr):
            setattr(recommend_info_entity, attr, getattr(dto, attr))
    recommend_infos = recommend_info_service.select_recommend_info_list(recommend_info_entity)
    return TableResponse(code=HttpStatus.SUCCESS, msg='查询成功', rows=recommend_infos)


@gen.route('/<int:id>', methods=['GET'])
@PathValidator()
@PreAuthorize(HasPerm('recruit:recommendInfo:query'))
@JsonSerializer()
def get_recommend_info(id: int):
    """获取用户推荐详细信息"""
    recommend_info_entity = recommend_info_service.select_recommend_info_by_id(id)
    return AjaxResponse.from_success(data=recommend_info_entity)


@gen.route('', methods=['POST'])
@BodyValidator()
@PreAuthorize(HasPerm('recruit:recommendInfo:add'))
@Log(title='用户推荐管理', business_type=BusinessType.INSERT)
@JsonSerializer()
def add_recommend_info(dto: RecommendInfo):
    """新增用户推荐"""
    recommend_info_entity = RecommendInfo()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(recommend_info_entity, attr):
            setattr(recommend_info_entity, attr, getattr(dto, attr))
    result = recommend_info_service.insert_recommend_info(recommend_info_entity)
    if result > 0:
        return AjaxResponse.from_success(msg='新增成功')
    return AjaxResponse.from_error(msg='新增失败')


@gen.route('', methods=['PUT'])
@BodyValidator()
@PreAuthorize(HasPerm('recruit:recommendInfo:edit'))
@Log(title='用户推荐管理', business_type=BusinessType.UPDATE)
@JsonSerializer()
def update_recommend_info(dto: RecommendInfo):
    """修改用户推荐"""
    recommend_info_entity = RecommendInfo()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(recommend_info_entity, attr):
            setattr(recommend_info_entity, attr, getattr(dto, attr))
    result = recommend_info_service.update_recommend_info(recommend_info_entity)
    if result > 0:
        return AjaxResponse.from_success(msg='修改成功')
    return AjaxResponse.from_error(msg='修改失败')


@gen.route('/<ids>', methods=['DELETE'])
@PathValidator()
@PreAuthorize(HasPerm('recruit:recommendInfo:remove'))
@Log(title='用户推荐管理', business_type=BusinessType.DELETE)
@JsonSerializer()
def delete_recommend_info(ids: str):
    """删除用户推荐"""
    try:
        id_list = [int(id) for id in ids.split(',')]
        result = recommend_info_service.delete_recommend_info_by_ids(id_list)
        if result > 0:
            return AjaxResponse.from_success(msg='删除成功')
        return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='删除失败')
    except Exception as e:
        return AjaxResponse.from_error(msg=f'删除失败: {str(e)}')


@gen.route('/export', methods=['POST'])
@FileDownloadValidator()
@PreAuthorize(HasPerm('recruit:recommendInfo:export'))
@Log(title='用户推荐管理', business_type=BusinessType.EXPORT)
@BaseSerializer()
def export_recommend_info(dto: RecommendInfo):
    """导出用户推荐列表"""
    recommend_info_entity = RecommendInfo()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(recommend_info_entity, attr):
            setattr(recommend_info_entity, attr, getattr(dto, attr))
    _clear_page_context()
    recommend_info_entity.page_num = None
    recommend_info_entity.page_size = None
    recommend_infos = recommend_info_service.select_recommend_info_list(recommend_info_entity)
    # 使用ExcelUtil导出Excel文件
    excel_util = ExcelUtil(RecommendInfo)
    return excel_util.export_response(recommend_infos, "用户推荐数据")


@gen.route('/importTemplate', methods=['POST'])
@login_required
@BaseSerializer()
def import_template():
    """下载用户推荐导入模板"""
    excel_util = ExcelUtil(RecommendInfo)
    return excel_util.import_template_response(sheetname="用户推荐数据")


@gen.route('/importData', methods=['POST'])
@FileUploadValidator()
@PreAuthorize(HasPerm('recruit:recommendInfo:import'))
@Log(title='用户推荐管理', business_type=BusinessType.IMPORT)
@JsonSerializer()
def import_data(
        file: List[FileStorage],
        update_support: Annotated[bool, BeforeValidator(lambda x: x != "0")]
):
    """导入用户推荐数据"""
    file = file[0]
    excel_util = ExcelUtil(RecommendInfo)
    recommend_info_list = excel_util.import_file(file, sheetname="用户推荐数据")
    msg = recommend_info_service.import_recommend_info(recommend_info_list, update_support)
    return AjaxResponse.from_success(msg=msg)
