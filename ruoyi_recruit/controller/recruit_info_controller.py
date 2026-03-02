from typing import List

from flask import g
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
from ruoyi_framework.descriptor.log import Log
from ruoyi_framework.descriptor.permission import HasPerm, PreAuthorize
from ruoyi_recruit.controller import recruit_info as recruit_info_bp
from ruoyi_recruit.domain.entity import RecruitInfo
from ruoyi_recruit.service.recruit_info_service import RecruitInfoService

# 使用 controller/__init__.py 中定义的蓝图
gen = recruit_info_bp

recruit_info_service = RecruitInfoService()


def _clear_page_context():
    if hasattr(g, "criterian_meta"):
        g.criterian_meta.page = None


@gen.route('/list', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('recruit:recruitInfo:list'))
@JsonSerializer()
def recruit_info_list(dto: RecruitInfo):
    """查询招聘信息列表"""
    recruit_info_entity = RecruitInfo()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(recruit_info_entity, attr):
            setattr(recruit_info_entity, attr, getattr(dto, attr))
    recruit_infos = recruit_info_service.select_recruit_info_list(recruit_info_entity)
    return TableResponse(code=HttpStatus.SUCCESS, msg='查询成功', rows=recruit_infos)


@gen.route('/<int:recruitId>', methods=['GET'])
@PathValidator()
@PreAuthorize(HasPerm('recruit:recruitInfo:query'))
@JsonSerializer()
def get_recruit_info(recruit_id: int):
    """获取招聘信息详细信息"""
    recruit_info_entity = recruit_info_service.select_recruit_info_by_id(recruit_id)
    return AjaxResponse.from_success(data=recruit_info_entity)

@gen.route('/detail/<int:recruitId>', methods=['GET'])
@PathValidator()
@PreAuthorize(HasPerm('recruit:recruitInfo:query'))
@JsonSerializer()
def get_recruit_info_detail(recruit_id: int):
    """获取招聘信息详细信息"""
    recruit_info_entity = recruit_info_service.select_recruit_info_detail_by_id(recruit_id)
    return AjaxResponse.from_success(data=recruit_info_entity)

@gen.route('', methods=['POST'])
@BodyValidator()
@PreAuthorize(HasPerm('recruit:recruitInfo:add'))
@Log(title='招聘信息管理', business_type=BusinessType.INSERT)
@JsonSerializer()
def add_recruit_info(dto: RecruitInfo):
    """新增招聘信息"""
    recruit_info_entity = RecruitInfo()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(recruit_info_entity, attr):
            setattr(recruit_info_entity, attr, getattr(dto, attr))
    result = recruit_info_service.insert_recruit_info(recruit_info_entity)
    if result > 0:
        return AjaxResponse.from_success(msg='新增成功')
    return AjaxResponse.from_error(msg='新增失败')


@gen.route('', methods=['PUT'])
@BodyValidator()
@PreAuthorize(HasPerm('recruit:recruitInfo:edit'))
@Log(title='招聘信息管理', business_type=BusinessType.UPDATE)
@JsonSerializer()
def update_recruit_info(dto: RecruitInfo):
    """修改招聘信息"""
    recruit_info_entity = RecruitInfo()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(recruit_info_entity, attr):
            setattr(recruit_info_entity, attr, getattr(dto, attr))
    result = recruit_info_service.update_recruit_info(recruit_info_entity)
    if result > 0:
        return AjaxResponse.from_success(msg='修改成功')
    return AjaxResponse.from_error(msg='修改失败')


@gen.route('/<ids>', methods=['DELETE'])
@PathValidator()
@PreAuthorize(HasPerm('recruit:recruitInfo:remove'))
@Log(title='招聘信息管理', business_type=BusinessType.DELETE)
@JsonSerializer()
def delete_recruit_info(ids: str):
    """删除招聘信息"""
    try:
        id_list = [int(id) for id in ids.split(',')]
        result = recruit_info_service.delete_recruit_info_by_ids(id_list)
        if result > 0:
            return AjaxResponse.from_success(msg='删除成功')
        return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='删除失败')
    except Exception as e:
        return AjaxResponse.from_error(msg=f'删除失败: {str(e)}')


@gen.route('/export', methods=['POST'])
@FileDownloadValidator()
@PreAuthorize(HasPerm('recruit:recruitInfo:export'))
@Log(title='招聘信息管理', business_type=BusinessType.EXPORT)
@BaseSerializer()
def export_recruit_info(dto: RecruitInfo):
    """导出招聘信息列表"""
    recruit_info_entity = RecruitInfo()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(recruit_info_entity, attr):
            setattr(recruit_info_entity, attr, getattr(dto, attr))
    _clear_page_context()
    recruit_info_entity.page_num = None
    recruit_info_entity.page_size = None
    recruit_infos = recruit_info_service.select_recruit_info_list(recruit_info_entity)
    # 使用ExcelUtil导出Excel文件
    excel_util = ExcelUtil(RecruitInfo)
    return excel_util.export_response(recruit_infos, "招聘信息数据")


@gen.route('/importTemplate', methods=['POST'])
@login_required
@BaseSerializer()
def import_template():
    """下载招聘信息导入模板"""
    excel_util = ExcelUtil(RecruitInfo)
    return excel_util.import_template_response(sheetname="招聘信息数据")


@gen.route('/importData', methods=['POST'])
@FileUploadValidator()
@PreAuthorize(HasPerm('recruit:recruitInfo:import'))
@Log(title='招聘信息管理', business_type=BusinessType.IMPORT)
@JsonSerializer()
def import_data(
        file: List[FileStorage]
):
    """导入招聘信息数据"""
    file = file[0]
    excel_util = ExcelUtil(RecruitInfo)
    recruit_info_list = excel_util.import_file(file, sheetname="招聘信息数据")
    msg = recruit_info_service.import_recruit_info(recruit_info_list)
    return AjaxResponse.from_success(msg=msg)
