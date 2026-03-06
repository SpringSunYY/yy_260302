# -*- coding: utf-8 -*-
# @Module: ruoyi_recruit/controller

from flask import Blueprint

view_info = Blueprint('view_info', __name__, url_prefix='/recruit/viewInfo')
recruit_info = Blueprint('recruit_info', __name__, url_prefix='/recruit/recruitInfo')
recommend_info = Blueprint('recommend_info', __name__, url_prefix='/recruit/recommendInfo')
like_info = Blueprint('like_info', __name__, url_prefix='/recruit/likeInfo')
statistics_info=Blueprint('statistics_info', __name__, url_prefix='/recruit/statistics')

from . import view_info_controller
from . import recruit_info_controller
from . import recommend_info_controller
from . import like_info_controller
from . import statistics_controller
