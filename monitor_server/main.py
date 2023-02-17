<<<<<<< HEAD
# 引入新版本特性
from __future__ import unicode_literals

# 基础网络库
from urllib import response
from flask import Flask, jsonify
from flask import Blueprint, url_for, request, render_template, session, redirect
from flask_restful import reqparse, abort, Api, Resource
from flasgger import Swagger, swag_from
import requests
import urllib
import urllib3
import json
import threading
import pandas as pd 

# 系统库
import time
from datetime import datetime, timedelta
import traceback
import json
import argparse
import os
import copy

# 算法
# 随机森林以及SVM

# 忽略警告
import warnings

warnings.filterwarnings("ignore")

# 自定义库
import config
from db_pool import POOL
from test_diandongche import Diandongche, Diandongche_U,Diandongche_Feature
import logger
import poster
from predict import predict

state = False
#test_diandongche = Diandongche_U('model/svm_rbf_model_u_1019_2.pkl')
#test_diandongche =Diandongche_U('model/svm_rbf_model_u_10.pkl')
# test_diandongche=Diandongche_Feature(model_path='model/svm_rbf_model_features_1116.pkl')
test_diandongche=Diandongche_Feature(model_path='model/knn_k=5_model_features_0104.pkl')

url = "http://121.36.11.215:8080/JalaAPI/a/highspeed/alarmInfo"
ret_logger = logger.Logger(save_dir='./log')
post_logger = poster.Logger(save_dir='./post_log')
myret_logger = logger.Logger(save_dir='./log3')
headers = {'Content-Type': 'application/json'}

def raw_to_int_or_float(self,path):
        with open(path) as f:
            data = f.read()
            data_list = data.strip().split(' ')
        str_data_list = [(data_list[i * 2] + data_list[i * 2 + 1]) for i in range(len(data_list) // 2)]
        bin_data_list = [bin(int(a, 16))[2:].zfill(20) for a in str_data_list]
        int_data_list = [(-int(a[0]) * (2 ** (19)) + int(a[1:], 2)) for a in bin_data_list]
        float_data_list = [(-float(a[0]) * (2 ** (19)) + float(int(a[1:], 2))) for a in bin_data_list]
        return float_data_list

def get_db_info(device_id: str, line_id: str, last_datetime: str):
    # 检查数据库中的文件信息
    ret = {'status': False}
    sql_C = \
        '''select file_path, create_date from jala_file_upload where line_id='%s' and file_type='C' and UNIX_TIMESTAMP(create_date)>'%s';''' \
        % (line_id, last_datetime)
    # 从连接池获取数据库连接
    conn_hybackup_C = POOL.connection()
    cursor_hybackup_C = conn_hybackup_C.cursor()

    try:
        t_count_C = cursor_hybackup_C.execute(sql_C)

        if t_count_C > 0:
            t_list_C = list(cursor_hybackup_C.fetchall())
            t_list_C.sort(key=lambda x: x[1])
            t_data_C = t_list_C[-1]

            ret.update({'status': True, 'C_file_path': t_data_C[0], 'U_file_path': t_data_C[0].replace("C", "U"),
                        'create_date': t_data_C[1]})
    except:
        # 异常处理
        traceback.print_exc()
        return ret

    # 释放数据库连接
    cursor_hybackup_C.close()
    conn_hybackup_C.close()

    return ret


def check_db_info(device_id: str, line_id: str, last_datetime: str, last_time: time):
    # 检查数据库信息
    ret = {'status': False}
    # 　while (time.time() - float(last_time)) < config.DATA_UPLOAD_TIME:

    # 可以设定在一定时间内运行
    while_end_time = time.time() + 30
    while (time.time() < while_end_time):
        time.sleep(1)
        # 获取数据库的信息
        t_ret = get_db_info(device_id, line_id, last_datetime)
        if t_ret['status']:
            ret.update(t_ret)
            break
    return ret


def read_excel(list_dic):
    data = pd.read_excel('D:\hy_projcet\show_demo\doc\深圳试点60套安装点位.xlsx', usecols=[4, 6]).dropna(how='all')
    data = data.fillna(method='ffill')
    data.columns = ['deviceid', 'lineid']
    head_list = list(data.columns) 
    
    for i in data.values:
        a_line = dict(zip(head_list, i)) 
        list_dic.append(a_line)

    return list_dic

lineid_time_map={}
class Detect(Resource):
    """
    异常检测
    """

    def post(self, **dict):
        deviceid = dict['deviceid'].strip()
        lineid = dict['lineid'].strip()
        # 返回值
        ret = {'status': 'normal'}

        clock_0 = time.time()
        t_result_1 = check_db_info(device_id=deviceid, line_id=lineid, last_datetime="1660907586", last_time=clock_0)
        # 数据库上没有新的数据文件信息,异常处理1
        if not t_result_1['status']:
            ret = {'status': "abnormal", 'deviceCode': deviceid,'lineID': lineid, 
                #    'timeStamp': t_result_1['create_date'].strftime(config.DATETIME_FORMAT),
                   'message': "", 'message_2': "数据库上没有新的数据文件信息"}
            response = json.dumps(ret)
            return response

        # 处理数据
        # time.sleep(5)
        C_file_path = os.path.join(config.DATA_FILE_DIR, t_result_1['C_file_path'])
        U_file_path = os.path.join(config.DATA_FILE_DIR, t_result_1['U_file_path'])
        if (not os.path.exists(C_file_path)) or (not os.path.exists(U_file_path)):  # 异常处理2
            ret = {'status': "abnormal", 'deviceCode': deviceid,'lineID': lineid,
                   'timeStamp': t_result_1['create_date'].strftime(config.DATETIME_FORMAT), 'message': "",
                   'message_2': "出现丢包情况"}
            response = json.dumps(ret)
            return response

        c_time = t_result_1['create_date']
        a = datetime.now()
        dt = (a - c_time).total_seconds()
        #if dt > 240:
        #    ret = {'too_old': 1, 'deviceCode': deviceid, 'lineID': lineid,
        #           'timeStamp': t_result_1['create_date'].strftime(config.DATETIME_FORMAT),
        #           'message': "", 'message_2': "数据创建时间与被检测到时间间隔超过4分钟，too old!"}
        #    print(ret)
        #    response = json.dumps(ret)
        #    return response

        # time.sleep(3)

        diandongche_type = test_diandongche.predict(C_file_path, U_file_path)  # 电动车负载检测
        dianhu_type,array_i = predict(U_file_path)
        if diandongche_type == [1]:
            ret_string = "存在电动车充电情况"

        elif diandongche_type == [0]:
            ret_string = ""
            time.sleep(5)
        else:
            # 异常处理3
            ret = {'status': "abnormal", 'deviceCode': deviceid,'lineID': lineid,
                   'timeStamp': t_result_1['create_date'].strftime(config.DATETIME_FORMAT), 'message': "",
                   'message_2': "数据文件特征维度错误"}
            response = json.dumps(ret)
            return response
        
        if dianhu_type == [1]:
            ret_string += "存在电弧"

        elif dianhu_type == [0]:
            ret_string += ""
            time.sleep(5)
        else:
            # 异常处理3
            ret = {'status': "abnormal", 'deviceCode': deviceid,'lineID': lineid,
                   'timeStamp': t_result_1['create_date'].strftime(config.DATETIME_FORMAT), 'message': "",
                   'message_2': "数据文件特征维度错误"}
            response = json.dumps(ret)
            return response

        ret.update({'deviceCode': deviceid, 'lineID': lineid,
                    'timeStamp': t_result_1['create_date'].strftime(config.DATETIME_FORMAT), \
                    'message': ret_string, 'message_2': "检测程序运行正常"})
        if dt>600:
            ret['too_old']=1
            ret['message_2']= "数据创建时间与被检测到时间间隔超过10分钟，too old!"
        tt=t_result_1['create_date'].strftime(config.DATETIME_FORMAT)
        if lineid_time_map[lineid]==tt:
                ret['too_old']=1
                ret['message_2']="已经报过"
        else:
                lineid_time_map[lineid]=tt
        
        #array_i=raw_to_int_or_float(U_file_path)
        ret['array_i']=array_i
        
        response = json.dumps(ret)

        
        return response


class MyThread(threading.Thread):
    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args

    def run(self):
        for arg in self.args:
            resp = self.func(**arg)
            if 'timeStamp' in json.loads(resp).keys():
                ret_logger.write_log(resp)  # 写日志
                if 'too_old' in json.loads(resp).keys():  # 该情况不向服务器发送post请求
                    continue
                else:
                    req = requests.post(url, data=resp, headers=headers)
                    post_logger.write_log(resp,req)


def multi_thread(my_device, thread_num, func):  # 60个设备开4个线程
    div_cnt = int(len(my_device) / thread_num)

    threadList = []
    for i in range(thread_num):
        if not i == thread_num - 1:
            task = my_device[i * div_cnt:i * div_cnt + div_cnt]
        else:
            task = my_device[i * div_cnt:]
        _thread = MyThread(func, task)
        threadList.append(_thread)
        _thread.start()

    for i in range(thread_num):
        threadList[i].join()


if __name__ == '__main__':
    
    detect = Detect()
    
    list_dic = []
    # list_dic.append({
    # 'deviceid': '6233e327fc28c11dc87e26c2',
    # 'lineid': '62fb6f68fb28c21ae4008989'
    # })
    # list_dic.append({
    # 'deviceid': '62352470fb28c213a865fedb',
    # 'lineid': '62fb6e91fb28c21ae4008981'
    # })
    # list_dic.append({
    # 'deviceid': '6235266ffb28c213a865ff5c',
    # 'lineid': '62f742fbfb28c21a3c38146f'
    # })
    # list_dic.append({
    # 'deviceid': '619df7bae0242a31602c57d2',
    # 'lineid': '612eea81e0242b26405bdf34'
    # })
    # list_dic.append({
    # 'deviceid':'619de69ee0242b3908a3f3a9',
    # 'lineid':'6141a42ee0242c2ed83c25b7'
    # })
    list_dic.append({
    'deviceid':'6233e327fc28c11dc87e26c2',
    'lineid':'62fae2b7fb28c21ae4006b4b'
    })
    list_dic.append({
    'deviceid':'62352470fb28c213a865fedb',
    'lineid':'62fb2c00fb28c21ae4007921'
    })
    list_dic.append({
    'deviceid':'6235266ffb28c213a865ff5c',
    'lineid':'62fb0f05fb28c21ae40074e7'
    })
    list_dic.append({
    'deviceid':'619de69ee0242b3908a3f3a9',
    'lineid':'62fb0657fb28c21ae400733e'
    })

    Mydevices=list_dic


    for ele in Mydevices:
            did=ele['deviceid']
            lid=ele['lineid']
            lineid_time_map[lid]=''

    print("—————————————————————")
    print("初始化完成，开始监测：")

    while 1:
        multi_thread(Mydevices, 2, detect.post)
=======
# 引入新版本特性
from __future__ import unicode_literals

# 基础网络库
from urllib import response
from flask import Flask, jsonify
from flask import Blueprint, url_for, request, render_template, session, redirect
from flask_restful import reqparse, abort, Api, Resource
from flasgger import Swagger, swag_from
import requests
import urllib
import urllib3
import json
import threading
import pandas as pd 
import redis

# 系统库
import time
from datetime import datetime, timedelta
import traceback
import json
import argparse
import os
import copy
import pickle

# 算法
# 随机森林以及SVM

# 忽略警告
import warnings


warnings.filterwarnings("ignore")

# 自定义库
import config
from db_pool import POOL
from test_diandongche import Diandongche_Feature
import logger
import poster
from predict1105 import predict

state = False
test_diandongche=Diandongche_Feature(model_path='D:\hy_projcet\show_demo\model\knn_k=5_model_features_0213.pkl')

# 低频检测
low_svm_model = pickle.load(open("D:\hy_projcet\show_demo\model\low_svm_model.pkl", "rb"))
# 低频检测连接池
low_pool = redis.ConnectionPool(host="121.36.11.215", port="6378", db=0,password="830844")
rc = redis.StrictRedis(connection_pool=low_pool)
ps = rc.pubsub()
ps.subscribe("algorithm") 
low_listen = ps.listen()


url = "http://121.36.11.215:8080/JalaAPI/a/highspeed/alarmInfo"
ret_logger = logger.Logger(save_dir='./log')
post_logger = poster.Logger(save_dir='./post_log')
headers = {'Content-Type': 'application/json'}

def raw_to_int_or_float(self,path):
        with open(path) as f:
            data = f.read()
            data_list = data.strip().split(' ')
        str_data_list = [(data_list[i * 2] + data_list[i * 2 + 1]) for i in range(len(data_list) // 2)]
        bin_data_list = [bin(int(a, 16))[2:].zfill(20) for a in str_data_list]
        int_data_list = [(-int(a[0]) * (2 ** (19)) + int(a[1:], 2)) for a in bin_data_list]
        float_data_list = [(-float(a[0]) * (2 ** (19)) + float(int(a[1:], 2))) for a in bin_data_list]
        return float_data_list

# def get_db_info(device_id: str, line_id: str, last_datetime: str):
#     # 检查数据库中的文件信息
#     ret = {'status': False}
#     sql_C = \
#         '''select file_path, create_date from jala_file_upload where line_id='%s' and file_type='C' and UNIX_TIMESTAMP(create_date)>'%s';''' \
#         % (line_id, last_datetime)
#     # 从连接池获取数据库连接
#     conn_hybackup_C = POOL.connection()
#     cursor_hybackup_C = conn_hybackup_C.cursor()

#     try:
#         t_count_C = cursor_hybackup_C.execute(sql_C)

#         if t_count_C > 0:
#             t_list_C = list(cursor_hybackup_C.fetchall())
#             t_list_C.sort(key=lambda x: x[1])
#             t_data_C = t_list_C[-1]

#             ret.update({'status': True, 'C_file_path': t_data_C[0], 'U_file_path': t_data_C[0].replace("C", "U"),
#                         'create_date': t_data_C[1]})
#     except:
#         # 异常处理
#         traceback.print_exc()
#         return ret

#     # 释放数据库连接
#     cursor_hybackup_C.close()
#     conn_hybackup_C.close()

#     return ret
def get_db_info(device_id: str, line_id: str, last_datetime: str):
    # 检查数据库中的文件信息
    ret = {'status': False}
    sql_C = \
        '''select file_path, create_date from jala_file_upload where line_id='%s' and file_type='U' and UNIX_TIMESTAMP(create_date)>'%s';''' \
        % (line_id, last_datetime)
    # 从连接池获取数据库连接
    conn_hybackup_C = POOL.connection()
    cursor_hybackup_C = conn_hybackup_C.cursor()

    try:
        t_count_C = cursor_hybackup_C.execute(sql_C)

        if t_count_C > 0:
            t_list_C = list(cursor_hybackup_C.fetchall())
            t_list_C.sort(key=lambda x: x[1])
            t_data_C = t_list_C[-1]

            ret.update({'status': True, 'U_file_path': t_data_C[0], 'create_date': t_data_C[1]})
    except:
        # 异常处理
        traceback.print_exc()
        return ret

    # 释放数据库连接
    cursor_hybackup_C.close()
    conn_hybackup_C.close()

    return ret

def check_db_info(device_id: str, line_id: str, last_datetime: str, last_time: time):
    # 检查数据库信息
    ret = {'status': False}
    # 　while (time.time() - float(last_time)) < config.DATA_UPLOAD_TIME:

    # 可以设定在一定时间内运行,已修改
    # while_end_time = time.time() + 3
    # while (time.time() < while_end_time):
        # 获取数据库的信息
    t_ret = get_db_info(device_id, line_id, last_datetime)
    if t_ret['status']:
        ret.update(t_ret)
    return ret


def read_excel():
    list_dic = []
    data = pd.read_excel('D:\hy_projcet\show_demo\doc\深圳试点60套安装点位.xlsx', usecols=[4, 6]).dropna(how='all')
    data = data.fillna(method='ffill')
    data.columns = ['deviceid', 'lineid']
    head_list = list(data.columns) 
    
    for i in data.values:
        a_line = dict(zip(head_list, i)) 
        list_dic.append(a_line)

    return list_dic

lineid_time_map={}
class Detect(Resource):
    """
    异常检测
    """
    def post(self, **dict):
        deviceid = dict['deviceid'].strip()
        lineid = dict['lineid'].strip()
        # 返回值
        ret = {'status': 'normal'}

        clock_0 = time.time()
        t_result_1 = check_db_info(device_id=deviceid, line_id=lineid, last_datetime="1660907586", last_time=clock_0)
        # 数据库上没有新的数据文件信息,异常处理1
        if not t_result_1['status']:
            ret = {'status': "abnormal", 'deviceCode': deviceid,'lineID': lineid, 
                #    'timeStamp': t_result_1['create_date'].strftime(config.DATETIME_FORMAT),
                   'message': "", 'message_2': "数据库上没有新的数据文件信息"}
            response = json.dumps(ret)
            return response

        # 处理数据
        # time.sleep(5)
        # C_file_path = os.path.join(config.DATA_FILE_DIR, t_result_1['C_file_path'])
        U_file_path = os.path.join(config.DATA_FILE_DIR, t_result_1['U_file_path'])
        # if (not os.path.exists(C_file_path)) or (not os.path.exists(U_file_path)):  (原)
        if not os.path.exists(U_file_path): # 异常处理2
            ret = {'status': "abnormal", 'deviceCode': deviceid,'lineID': lineid,
                   'timeStamp': t_result_1['create_date'].strftime(config.DATETIME_FORMAT), 'message': "",
                   'message_2': "出现丢包情况"}
            response = json.dumps(ret)
            return response

        c_time = t_result_1['create_date']
        a = datetime.now()
        dt = (a - c_time).total_seconds()

        # diandongche_type = test_diandongche.predict(C_file_path, U_file_path)  # 电动车负载检测(原)
        diandongche_type = test_diandongche.predict(U_file_path)  # 电动车负载检测
        dianhu_type,array_i = predict(U_file_path)


        # 该位置加入低频检测算法
        if diandongche_type == [1]:
            for low_listen_data in low_listen:
                if((type(low_listen_data["data"]))==type(1)):
                    pass
                else :
                    data_list = json.loads(low_listen_data["data"].decode())["lines"]
                    for data in data_list:
                        if lineid==data['deviceLine'].split("_")[1] :
                            detect_line = [data["current"], data["power"]]
                            diandongche_type = low_svm_model.predict([detect_line])
                            break
                    break
        # 修改结束


        if diandongche_type == [1]:
            ret_string = "存在电动车充电情况"

        elif diandongche_type == [0]:
            ret_string = ""
            time.sleep(5)
        else:
            # 异常处理3
            ret = {'status': "abnormal", 'deviceCode': deviceid,'lineID': lineid,
                   'timeStamp': t_result_1['create_date'].strftime(config.DATETIME_FORMAT), 'message': "",
                   'message_2': "数据文件特征维度错误"}
            response = json.dumps(ret)
            return response
        
        if dianhu_type == [1]:
            ret_string += "存在电弧"

        elif dianhu_type == [0]:
            ret_string += ""
            time.sleep(5)
        else:
            # 异常处理3
            ret = {'status': "abnormal", 'deviceCode': deviceid,'lineID': lineid,
                   'timeStamp': t_result_1['create_date'].strftime(config.DATETIME_FORMAT), 'message': "",
                   'message_2': "数据文件特征维度错误"}
            response = json.dumps(ret)
            return response

        ret.update({'deviceCode': deviceid, 'lineID': lineid,
                    'timeStamp': t_result_1['create_date'].strftime(config.DATETIME_FORMAT), \
                    'message': ret_string, 'message_2': "检测程序运行正常"})
        if dt>600:
            ret['too_old']=1
        #     ret['message_2']= "数据创建时间与被检测到时间间隔超过10分钟，too old!"
        tt=t_result_1['create_date'].strftime(config.DATETIME_FORMAT)
        if lineid_time_map[lineid]==tt:
                ret['too_old']=1
                ret['message_2']="已经报过"
        else:
                lineid_time_map[lineid]=tt
        
        # array_i=raw_to_int_or_float(U_file_path)
        ret['array_i']=array_i
        
        response = json.dumps(ret)
        return response


class MyThread(threading.Thread):
    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args

    def run(self):
        for arg in self.args:
            resp = self.func(**arg)
            print(json.loads(resp))
            if 'timeStamp' in json.loads(resp).keys():
                if 'too_old' in json.loads(resp).keys():  # 该情况不向服务器发送post请求
                    continue
                else:
                    ret_logger.write_log(resp)  # 写日志
                    req = requests.post(url, data=resp, headers=headers)
                    post_logger.write_log(resp,req)


def multi_thread(my_device, thread_num, func): 
    div_cnt = int(len(my_device) / thread_num)

    threadList = []
    for i in range(thread_num):
        if not i == thread_num - 1:
            task = my_device[i * div_cnt:i * div_cnt + div_cnt]
        else:
            task = my_device[i * div_cnt:]
        _thread = MyThread(func, task)
        threadList.append(_thread)
        _thread.start()

    for i in range(thread_num):
        threadList[i].join()


if __name__ == '__main__':
    
    detect = Detect()
    
    Mydevices = read_excel()

    for ele in Mydevices:
            did=ele['deviceid']
            lid=ele['lineid']
            lineid_time_map[lid]=''

    print("—————————————————————")
    print("初始化完成，开始监测:")

    while 1:
        multi_thread(Mydevices, 700, detect.post)
>>>>>>> 3cf9892 (0215-version)
