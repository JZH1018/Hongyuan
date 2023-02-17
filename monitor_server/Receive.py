# 引入新版本特性
from __future__ import unicode_literals
from pydantic import BaseModel
from fastapi import FastAPI
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


url = "http://121.36.11.215:8080/JalaAPI/a/highspeed/alarmInfo"
ret_logger = logger.Logger(save_dir='./log2')
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

def get_db_info(device_id: str, line_id: str, last_datetime: str,creat_time:time):
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
            t_data_C = t_list_C[-5:]
            #这里要更改
            diff = []
            for item in t_data_C:
                dt = item[1]
                stamp = int(time.mktime(dt.timetuple()))
                diff.append(abs(stamp-creat_time))
            min_index = diff.index(min(diff))
            t_data_C = t_data_C[min_index]
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
        # 获取数据库的信息
        t_ret = get_db_info(device_id, line_id, last_datetime,last_time)
        if t_ret['status']:
            ret.update(t_ret)
            break
    return ret

class Detect(Resource):
    """
    异常检测
    """

    def post(self, deviceid,lineid,creat_time):
        # 返回值
        ret = {'status': 'normal'}
        t_result_1 = check_db_info(device_id=deviceid, line_id=lineid, last_datetime="1660907586", last_time=creat_time)
        # 数据库上没有新的数据文件信息,异常处理1
        if not t_result_1['status']:
            ret = {'status': "abnormal", 'deviceCode': deviceid,'lineID': lineid, 'timeStamp': t_result_1['create_date'].strftime(config.DATETIME_FORMAT),
                   'message': "", 'message_2': "数据库上没有新的数据文件信息"}
            response = json.dumps(ret)
            return response

        # 处理数据
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
        #diandongche_type = test_diandongche.predict(C_file_path, U_file_path)  # 电动车负载检测
        dianhu_type,array_i = predict(U_file_path)
      
        '''
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
        '''
        # if dianhu_type == [1]:
        #     myret_string += "存在电弧"

        # elif dianhu_type == [0]:
        #     myret_string += ""
        #     time.sleep(5)
        # else:
        #     # 异常处理3
        #     ret = {'status': "abnormal", 'deviceCode': deviceid,'lineID': lineid,
        #            'timeStamp': t_result_1['create_date'].strftime(config.DATETIME_FORMAT), 'message': "",
        #            'message_2': "数据文件特征维度错误"}
        #     response = json.dumps(ret)
        #     return response
        # myret={}
        # for key in ret:
        #     if key == 'message':
        #         myret[key] = myret_string
        #     else:
        #         myret[key] = ret[key]

        ret_string = "存在电弧"
        ret.update({'deviceCode': deviceid, 'lineID': lineid,
                    'timeStamp': t_result_1['create_date'].strftime(config.DATETIME_FORMAT), \
                    'message': ret_string, 'message_2': "检测程序运行正常"})
        if dt>600:
            ret['too_old']=1
            ret['message_2']= "数据创建时间与被检测到时间间隔超过10分钟，too old!"
        tt=t_result_1['create_date'].strftime(config.DATETIME_FORMAT)
        
        #array_i=raw_to_int_or_float(U_file_path)
        ret['array_i']=array_i
        
        response = json.dumps(ret)

        
        return response


def mymain(deviceid,lineid,creat_time):
    
    detect = Detect()
    print("—————————————————————")
    print("初始化完成，开始监测：")

    resp = detect.post(deviceid,lineid,creat_time)
    ret_logger.write_log(resp)
    req = requests.post(url, data=resp, headers=headers)
    return 'success'

app = FastAPI()
 
class Item(BaseModel):
    deviceid: str = None
    lineid: str = None
    timestamp: int = None

@app.post('/test')
def calculate(request_data: Item):
    a = request_data.deviceid
    b = request_data.lineid
    c = request_data.timestamp
    mystate = mymain(a,b,c)
    return 'success'

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app,
                host="0.0.0.0",
                port=5009,
                workers=1)


