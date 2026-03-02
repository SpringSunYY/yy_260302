
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
from ruoyi_recruit.controller import like_info as like_info_bp
from ruoyi_recruit.domain.entity import LikeInfo, RecruitInfo
from ruoyi_recruit.service.like_info_service import LikeInfoService
from ruoyi_recruit.service.recruit_info_service import RecruitInfoService

# 使用 controller/__init__.py 中定义的蓝图
gen = like_info_bp

like_info_service = LikeInfoService()
recruit_info_service = RecruitInfoService()


def _clear_page_context():
    if hasattr(g, "criterian_meta"):
        g.criterian_meta.page = None

@gen.route('/list', methods=["GET"])
@QueryValidator(is_page=True)
@PreAuthorize(HasPerm('recruit:likeInfo:list'))
@JsonSerializer()
def like_info_list(dto: LikeInfo):
    """查询用户点赞列表"""
    like_info_entity = LikeInfo()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(like_info_entity, attr):
            setattr(like_info_entity, attr, getattr(dto, attr))
    like_infos = like_info_service.select_like_info_list(like_info_entity)
    return TableResponse(code=HttpStatus.SUCCESS, msg='查询成功', rows=like_infos)


@gen.route('/<int:id>', methods=['GET'])
@PathValidator()
@PreAuthorize(HasPerm('recruit:likeInfo:query'))
@JsonSerializer()
def get_like_info(id: int):
    """获取用户点赞详细信息"""
    like_info_entity = like_info_service.select_like_info_by_id(id)
    return AjaxResponse.from_success(data=like_info_entity)


@gen.route('', methods=['POST'])
@BodyValidator()
@PreAuthorize(HasPerm('recruit:likeInfo:add'))
@Log(title='用户点赞管理', business_type=BusinessType.INSERT)
@JsonSerializer()
def add_like_info(dto: LikeInfo):
    """新增用户点赞"""
    like_info_entity = LikeInfo()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(like_info_entity, attr):
            setattr(like_info_entity, attr, getattr(dto, attr))
    result = like_info_service.insert_like_info(like_info_entity)
    if result > 0:
        return AjaxResponse.from_success(msg='新增成功')
    return AjaxResponse.from_error(msg='新增失败')


@gen.route('', methods=['PUT'])
@BodyValidator()
@PreAuthorize(HasPerm('recruit:likeInfo:edit'))
@Log(title='用户点赞管理', business_type=BusinessType.UPDATE)
@JsonSerializer()
def update_like_info(dto: LikeInfo):
    """修改用户点赞"""
    like_info_entity = LikeInfo()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(like_info_entity, attr):
            setattr(like_info_entity, attr, getattr(dto, attr))
    result = like_info_service.update_like_info(like_info_entity)
    if result > 0:
        return AjaxResponse.from_success(msg='修改成功')
    return AjaxResponse.from_error(msg='修改失败')



@gen.route('/<ids>', methods=['DELETE'])
@PathValidator()
@PreAuthorize(HasPerm('recruit:likeInfo:remove'))
@Log(title='用户点赞管理', business_type=BusinessType.DELETE)
@JsonSerializer()
def delete_like_info(ids: str):
    """删除用户点赞"""
    try:
        id_list = [int(id) for id in ids.split(',')]
        result = like_info_service.delete_like_info_by_ids(id_list)
        if result > 0:
            return AjaxResponse.from_success(msg='删除成功')
        return AjaxResponse.from_error(code=HttpStatus.ERROR, msg='删除失败')
    except Exception as e:
        return AjaxResponse.from_error(msg=f'删除失败: {str(e)}')


@gen.route('/export', methods=['POST'])
@FileDownloadValidator()
@PreAuthorize(HasPerm('recruit:likeInfo:export'))
@Log(title='用户点赞管理', business_type=BusinessType.EXPORT)
@BaseSerializer()
def export_like_info(dto: LikeInfo):
    """导出用户点赞列表"""
    like_info_entity = LikeInfo()
    # 转换PO到Entity对象
    for attr in dto.model_fields.keys():
        if hasattr(like_info_entity, attr):
            setattr(like_info_entity, attr, getattr(dto, attr))
    _clear_page_context()
    like_info_entity.page_num = None
    like_info_entity.page_size = None
    like_infos = like_info_service.select_like_info_list(like_info_entity)
    # 使用ExcelUtil导出Excel文件
    excel_util = ExcelUtil(LikeInfo)
    return excel_util.export_response(like_infos, "用户点赞数据")

@gen.route('/importTemplate', methods=['POST'])
@login_required
@BaseSerializer()
def import_template():
    """下载用户点赞导入模板"""
    excel_util = ExcelUtil(LikeInfo)
    return excel_util.import_template_response(sheetname="用户点赞数据")

@gen.route('/importData', methods=['POST'])
@FileUploadValidator()
@PreAuthorize(HasPerm('recruit:likeInfo:import'))
@Log(title='用户点赞管理', business_type=BusinessType.IMPORT)
@JsonSerializer()
def import_data(
    file: List[FileStorage],
    update_support: Annotated[bool, BeforeValidator(lambda x: x != "0")]
):
    """导入用户点赞数据"""
    file = file[0]
    excel_util = ExcelUtil(LikeInfo)
    like_info_list = excel_util.import_file(file, sheetname="用户点赞数据")
    msg = like_info_service.import_like_info(like_info_list, update_support)
    return AjaxResponse.from_success(msg=msg)


@gen.route('/like/<int:recruitId>', methods=['POST'])
@PathValidator()
@PreAuthorize(HasPerm('recruit:likeInfo:add'))
@Log(title='用户点赞管理', business_type=BusinessType.INSERT)
@JsonSerializer()
def toggle_like(recruit_id: int):
    """点赞或取消点赞"""
    # 先查询招聘信息详情
    recruit_info = recruit_info_service.select_recruit_info_by_id(recruit_id)
    if not recruit_info:
        return AjaxResponse.from_error(msg='招聘信息不存在')

    # 执行点赞或取消点赞
    result = like_info_service.toggle_like(recruit_info)
    if result.get('is_liked') is not None:
        return AjaxResponse.from_success(data={"isLiked": result['is_liked']}, msg=result['msg'])
    return AjaxResponse.from_error(msg=result.get('msg', '操作失败'))
