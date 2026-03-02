
from typing import List

from flask import g
from flask_login import login_required
from pydantic import BeforeValidator
from typing_extensions import Annotated
from werkzeug.datastructures import FileStorage

from ruoyi_common.base.model import AjaxResponse, TableResponse
from ruoyi_common.constant import HttpStatus
from ruoyi_common.descriptor.serializer import BaseSerializer, JsonSerializer
from ruoyi_common.descriptor.validator import QueryValidator, BodyValidator, PathValidator, FileDownloadValidator, FileUploadValidator
from ruoyi_common.domain.enum import BusinessType
from ruoyi_common.utils.base import ExcelUtil
from ruoyi_framework.descriptor.log import Log
from ruoyi_framework.descriptor.permission import HasPerm, PreAuthorize
from ruoyi_recruit.controller import view_info as view_info_bp
from ruoyi_recruit.domain.entity import ViewInfo
from ruoyi_recruit.service.view_info_service import ViewInfoService

# 使用 controller/__init__.py 中定义的蓝图
gen = view_info_bp

view_info_service = ViewInfoService()


def _clear_page_context():
    if hasattr(g, "criterian_meta"):
        g.criterian_meta.page = None

@gen.route('/list', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('recruit:viewInfo:list'))
@JsonSerializer()
def view_info_list(dto: ViewInfo):
    """查询用户浏览列表"""
    view_info_entity = ViewInfo()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(view_info_entity, attr):
            setattr(view_info_entity, attr, getattr(dto, attr))
    view_infos = view_info_service.select_view_info_list(view_info_entity)
    return TableResponse(code=HttpStatus.SUCCESS, msg='查询成功', rows=view_infos)


@gen.route('/<int:id>', methods=['GET'])
@PathValidator()
@PreAuthorize(HasPerm('recruit:viewInfo:query'))
@JsonSerializer()
def get_view_info(id: int):
    """获取用户浏览详细信息"""
    view_info_entity = view_info_service.select_view_info_by_id(id)
    return AjaxResponse.from_success(data=view_info_entity)


@gen.route('', methods=['POST'])
@BodyValidator()
@PreAuthorize(HasPerm('recruit:viewInfo:add'))
@Log(title='用户浏览管理', business_type=BusinessType.INSERT)
@JsonSerializer()
def add_view_info(dto: ViewInfo):
    """新增用户浏览"""
    view_info_entity = ViewInfo()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(view_info_entity, attr):
            setattr(view_info_entity, attr, getattr(dto, attr))
    result = view_info_service.insert_view_info(view_info_entity)
    if result > 0:
        return AjaxResponse.from_success(msg='新增成功')
    return AjaxResponse.from_error(msg='新增失败')


@gen.route('', methods=['PUT'])
@BodyValidator()
@PreAuthorize(HasPerm('recruit:viewInfo:edit'))
@Log(title='用户浏览管理', business_type=BusinessType.UPDATE)
@JsonSerializer()
def update_view_info(dto: ViewInfo):
    """修改用户浏览"""
    view_info_entity = ViewInfo()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(view_info_entity, attr):
            setattr(view_info_entity, attr, getattr(dto, attr))
    result = view_info_service.update_view_info(view_info_entity)
    if result > 0:
        return AjaxResponse.from_success(msg='修改成功')
    return AjaxResponse.from_error(msg='修改失败')



@gen.route('/<ids>', methods=['DELETE'])
@PathValidator()
@PreAuthorize(HasPerm('recruit:viewInfo:remove'))
@Log(title='用户浏览管理', business_type=BusinessType.DELETE)
@JsonSerializer()
def delete_view_info(ids: str):
    """删除用户浏览"""
    try:
        id_list = [int(id) for id in ids.split(',')]
        result = view_info_service.delete_view_info_by_ids(id_list)
        if result > 0:
            return AjaxResponse.from_success(msg='删除成功')
        return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='删除失败')
    except Exception as e:
        return AjaxResponse.from_error(msg=f'删除失败: {str(e)}')


@gen.route('/export', methods=['POST'])
@FileDownloadValidator()
@PreAuthorize(HasPerm('recruit:viewInfo:export'))
@Log(title='用户浏览管理', business_type=BusinessType.EXPORT)
@BaseSerializer()
def export_view_info(dto: ViewInfo):
    """导出用户浏览列表"""
    view_info_entity = ViewInfo()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(view_info_entity, attr):
            setattr(view_info_entity, attr, getattr(dto, attr))
    _clear_page_context()
    view_info_entity.page_num = None
    view_info_entity.page_size = None
    view_infos = view_info_service.select_view_info_list(view_info_entity)
    # 使用ExcelUtil导出Excel文件
    excel_util = ExcelUtil(ViewInfo)
    return excel_util.export_response(view_infos, "用户浏览数据")

@gen.route('/importTemplate', methods=['POST'])
@login_required
@BaseSerializer()
def import_template():
    """下载用户浏览导入模板"""
    excel_util = ExcelUtil(ViewInfo)
    return excel_util.import_template_response(sheetname="用户浏览数据")

@gen.route('/importData', methods=['POST'])
@FileUploadValidator()
@PreAuthorize(HasPerm('recruit:viewInfo:import'))
@Log(title='用户浏览管理', business_type=BusinessType.IMPORT)
@JsonSerializer()
def import_data(
    file: List[FileStorage],
    update_support: Annotated[bool, BeforeValidator(lambda x: x != "0")]
):
    """导入用户浏览数据"""
    file = file[0]
    excel_util = ExcelUtil(ViewInfo)
    view_info_list = excel_util.import_file(file, sheetname="用户浏览数据")
    msg = view_info_service.import_view_info(view_info_list, update_support)
    return AjaxResponse.from_success(msg=msg)