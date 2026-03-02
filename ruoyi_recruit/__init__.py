# -*- coding: utf-8 -*-
# @Module: recruit
# @Author: YY

def init_app(app):
    """
    初始化模块，注册蓝图
    
    Args:
        app: Flask应用实例
    """
    # 导入 controller 模块，自动注册所有蓝图
    # 使用 pythonModelName 生成 Python 导入路径
    from ruoyi_recruit.controller import view_info
    app.register_blueprint(view_info)
    # 使用 pythonModelName 生成 Python 导入路径
    from ruoyi_recruit.controller import recruit_info
    app.register_blueprint(recruit_info)
    # 使用 pythonModelName 生成 Python 导入路径
    from ruoyi_recruit.controller import recommend_info
    app.register_blueprint(recommend_info)
    # 使用 pythonModelName 生成 Python 导入路径
    from ruoyi_recruit.controller import like_info
    app.register_blueprint(like_info)