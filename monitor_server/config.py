<<<<<<< HEAD
from cgi import test
import os


# IP表示服务器地址
IP = '121.36.56.110'
# HOST表示主机地址
HOST = '0.0.0.0'

# 端口
PORT = 3389

# 是否是开发环境
DEV = True


"""
配置 swagger
"""
TEMPLATE = {
    "SWAGGER": {
        "openapi": "3.0.2"
    },
    "info": {
        "title": "故障电弧及电动车识别",
        "description": " ",
        "version": "demo"
    },
    "host": "localhost:3389",
    "basePath": "/",
}


# 文件服务器目录
DATA_FILE_DIR = os.path.join('..','file_server')

# 录波指令url
SAMPLE_COMMAND_URL = 'http://121.36.11.215:8080/JalaAPI/a/algorithm/command'

# 时间格式
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_FORMAT = '%Y-%m-%d'


# 文档目录
DOC_DIR = 'doc'


# # 负载识别模型地址
# model_path = os.path.join('model','test0.pkl')
# # 模型输出类别
# test_0_dict = ['电动车充电', '笔记本电脑', '旋转台灯', '空气加湿器', '电热水壶', 
#     '电饭煲', '电饭煲（保温）', '电视机', '家用台式饮水机', '家用台式饮水机(待机)', '吸尘器', '破壁机', '冰箱']

# 最小功率阈值(单位: W)
POWER_THRES = 5
# 功率变化阈值(单位: W)
POWER_VAR_THRES = 5

# 录波文件上传时限(单位: s)
=======
from cgi import test
import os


# IP表示服务器地址
IP = '121.36.56.110'
# HOST表示主机地址
HOST = '0.0.0.0'

# 端口
PORT = 3389

# 是否是开发环境
DEV = True


"""
配置 swagger
"""
TEMPLATE = {
    "SWAGGER": {
        "openapi": "3.0.2"
    },
    "info": {
        "title": "故障电弧及电动车识别",
        "description": " ",
        "version": "demo"
    },
    "host": "localhost:3389",
    "basePath": "/",
}


# 文件服务器目录
DATA_FILE_DIR = os.path.join('..','file_server')

# 录波指令url
SAMPLE_COMMAND_URL = 'http://121.36.11.215:8080/JalaAPI/a/algorithm/command'

# 时间格式
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_FORMAT = '%Y-%m-%d'


# 文档目录
DOC_DIR = 'doc'


# # 负载识别模型地址
# model_path = os.path.join('model','test0.pkl')
# # 模型输出类别
# test_0_dict = ['电动车充电', '笔记本电脑', '旋转台灯', '空气加湿器', '电热水壶', 
#     '电饭煲', '电饭煲（保温）', '电视机', '家用台式饮水机', '家用台式饮水机(待机)', '吸尘器', '破壁机', '冰箱']

# 最小功率阈值(单位: W)
POWER_THRES = 5
# 功率变化阈值(单位: W)
POWER_VAR_THRES = 5

# 录波文件上传时限(单位: s)
>>>>>>> 3cf9892 (0215-version)
DATA_UPLOAD_TIME = 60