# -*- coding: utf-8 -*-
# @Author  : YY

# 定义常量

class HttpStatus:

    SUCCESS = 200

    CREATED = 201

    ACCEPTED = 202        # 已接受

    NO_CONTENT = 204      # 无内容

    MOVED_PERM = 301

    SEE_OTHER = 303

    NOT_MODIFIED = 304

    BAD_REQUEST = 400     # 错误的请求

    UNAUTHORIZED = 401    # 未授权

    FORBIDDEN = 403       # 禁止访问

    NOT_FOUND = 404       # 未找到

    BAD_METHOD = 405      # 方法不允许

    CONFLICT = 409        # 冲突

    UNSUPPORTED_TYPE = 415  # 请求范围不符合要求

    ERROR = 500  # 内部错误

    NOT_IMPLEMENTED = 501  # 尚未实施


class Constants:

    CAPTCHA_EXPIRATION = 2   # 2 分钟

    TOKEN = "token"

    TOKEN_HEADER = "Authorization"

    LOGIN_USER_KEY = "login_user_key"

    TOKEN_PREFIX = "Bearer "

    UTF8 = "UTF-8"

    GBK = "GBK"

    HTTP = "http://"

    HTTPS = "https://"

    WWW = "www."

    DOT = "."

    SUCCESS = "0"

    FAIL = "1"

    LOGIN_SUCCESS = "Success"

    LOGOUT = "Logout"

    REGISTER = "Register"

    LOGIN_FAIL = "Error"

    CAPTCHA_CODE_KEY = "captcha_codes:"

    LOGIN_TOKEN_KEY = "login_tokens:"

    REPEAT_SUBMIT_KEY = "repeat_submit:"

    RATE_LIMIT_KEY = "rate_limit:"

    CAPTCHA_EXPIRATION = 2

    JWT_USERID = "userid"

    JWT_USERNAME = "sub"

    JWT_AVATAR = "avatar"

    JWT_CREATED = "created"

    JWT_AUTHORITIES = "authorities"

    SYS_CONFIG_KEY = "sys_config:"

    SYS_DICT_KEY = "sys_dict:"

    RESOURCE_PREFIX = "/profile"

    LOOKUP_RMI = "rmi:";

    LOOKUP_LDAP = "ldap:";

    LOOKUP_LDAPS = "ldaps:";

    JOB_WHITELIST_STR = { "com.ruoyi" };

    JOB_ERROR_STR = { "java.net.URL", "javax.naming.InitialContext", "org.yaml.snakeyaml",
            "org.springframework", "org.apache", "com.ruoyi.common.utils.file" }; # todo


class UserConstants:

    # Unique identifier for system users within the platform
    SYS_USER = "SYS_USER"

    # Normal status
    NORMAL = "0"

    # Exception status
    EXCEPTION = "1"

    # User disabled status
    USER_DISABLE = "1"

    # Role disabled status
    ROLE_DISABLE = "1"

    # Department normal status
    DEPT_NORMAL = "0"

    # Department disabled status
    DEPT_DISABLE = "1"

    # Dictionary normal status
    DICT_NORMAL = "0"

    # Is it a system default (yes)
    YES = "Y"

    # Is it an external link menu (yes)
    YES_FRAME = "0"

    # Is it an external link menu (no)
    NO_FRAME = "1"

    # Menu type (directory)
    TYPE_DIR = "M"

    # Menu type (menu)
    TYPE_MENU = "C"

    # Menu type (button)
    TYPE_BUTTON = "F"

    # Layout component identifier
    LAYOUT = "Layout"

    # ParentView component identifier
    PARENT_VIEW = "ParentView"

    # InnerLink component identifier
    INNER_LINK = "InnerLink"

    # Validation return result codes
    UNIQUE = "0"
    NOT_UNIQUE = "1"

    # Username length restrictions
    USERNAME_MIN_LENGTH = 2
    USERNAME_MAX_LENGTH = 20

    # Password length restrictions
    PASSWORD_MIN_LENGTH = 5
    PASSWORD_MAX_LENGTH = 20

class ConfigConstants:
    # ==================== 推荐算法配置键定义 ====================
    # 维度权重配置
    CONFIG_KEY_POST_TYPE_WEIGHT = "recruit:recommend:weight:post_type"  # 岗位大类权重
    CONFIG_KEY_CITY_LEVEL_WEIGHT = "recruit:recommend:weight:city_level"  # 城市等级权重
    CONFIG_KEY_PROVINCE_WEIGHT = "recruit:recommend:weight:province"  # 省份权重
    CONFIG_KEY_CITY_WEIGHT = "recruit:recommend:weight:city"  # 城市权重
    CONFIG_KEY_EXPERIENCE_WEIGHT = "recruit:recommend:weight:experience"  # 经验要求权重
    CONFIG_KEY_EDUCATION_WEIGHT = "recruit:recommend:weight:education"  # 学历要求权重
    CONFIG_KEY_MAIN_BUSINESS_WEIGHT = "recruit:recommend:weight:main_business"  # 主营业务权重
    CONFIG_KEY_ENTERPRISE_SIZE_WEIGHT = "recruit:recommend:weight:enterprise_size"  # 企业规模权重
    CONFIG_KEY_FINANCING_WEIGHT = "recruit:recommend:weight:financing"  # 融资情况权重
    CONFIG_KEY_SALARY_WEIGHT = "recruit:recommend:weight:salary"  # 薪资权重
    CONFIG_KEY_SALARY_RANGE = "recruit:recommend:salary_range"  # 薪资区间配置

    # 算法参数配置
    CONFIG_KEY_TIME_DECAY_FACTOR = "recruit:recommend:time_decay_factor"  # 时间衰减因子
    CONFIG_KEY_VIEW_RECORD_NUM = "recruit:recommend:view_record_num"  # 浏览记录获取数量
    CONFIG_KEY_LIKE_RECORD_NUM = "recruit:recommend:like_record_num"  # 点赞记录获取数量
    CONFIG_KEY_VIEW_SCORE = "recruit:recommend:view_score"  # 浏览基础分值
    CONFIG_KEY_LIKE_SCORE = "recruit:recommend:like_score"  # 点赞基础分值
    CONFIG_KEY_RECOMMEND_NUM = "recruit:recommend:num"  # 推荐数量
    CONFIG_KEY_VIEW_NEW_RECORD_NUM = "recruit:recommend:view_new_record_num"  # 自动刷新所需新浏览数
    CONFIG_KEY_LIKE_NEW_RECORD_NUM = "recruit:recommend:like_new_record_num"  # 自动刷新所需新点赞数
