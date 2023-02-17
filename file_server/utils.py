<<<<<<< HEAD
from datetime import datetime
from db_pool import POOL
import traceback
import config
import os
import requests
import json

def sent_info_to_db(device_id:str, line_id:str,
                    file_path:str, file_type:str,
                    frequency:int, create_date:datetime, 
                    comment:str):
    """
    表名:
    jala_file_upload
    属性:
    id: 每条记录的主键，插入数据时自动生成（类似 00017aa476fe4844810013dea7de0b8c）
    device_id: 网关id（类似 5e6726854c1d6e26f8152666）
    line_id: 线路id（类似 5df31a6b4c1d6e2da886dd7a）
    file_path: 文件路径（字符串，长度不定）
    file_type: 文件类型（字符串，长度不定）
    frequency: 采样频率（整型，单位为Hz）
    create_date: 数据采集时间（datetime类型）
    comment: 备注信息（字符串，长度不定）
    """

    sql = "INSERT INTO jala_file_upload "\
        "(id,device_id,line_id,file_path,file_type,frequency,create_date,comment) "\
        "VALUES ( REPLACE(UUID(),'-',''),'%s','%s','%s','%s','%s','%s','%s');"\
                %(device_id,line_id,file_path,file_type,frequency,
                create_date.strftime(config.DATETIME_FORMAT),comment)
    # 从连接池获取数据库连接
    conn_hy = POOL.connection()
    cursor_hy = conn_hy.cursor()
    try:
        ret = cursor_hy.execute(sql)
        cursor_hy.connection.commit()
    except:
        # 异常处理
        reason = traceback.format_exc()
        return False, reason
    # 释放数据库连接
    cursor_hy.close()
    conn_hy.close()

    return True, 'success'


# 6141a42ee0242c2ed83c25b7_1642495513_C_16k.data
# 61bc3fe7e0242b1f343b179a_1640136602_16k.data
def save_info(file_name:str,save_path:str,device_id:str,comment='',file_type='test'):

    file_name = file_name.split('.')[0]
    file_name_split = file_name.split('_')
    line_id = file_name_split[0]
    time_stamp = int(file_name_split[1])
    create_date = datetime.fromtimestamp(time_stamp)
    file_type = file_name_split[2]
    frequency = int(file_name_split[3][:-1])*1000
    # db excute
    flag, reason = sent_info_to_db(device_id,line_id,save_path,file_type,frequency,create_date,comment)
    return flag, reason


def send_sample_command(device_id:str, line_id:str, value:int):
    """
    {"status":" success | fail | offline | not exist "}
    value:(目前电流电压的文件标号是反的，实际是C代表电流，U代表电压)
        0:电流(实际是电压)
        1:电压(实际是电流)
        2:电流+电压
    """
    url = config.SAMPLE_COMMAND_URL
    send_obj = {
        "deviceId":device_id,
        "lineId":line_id,
        "value":value
    }
    send_json = json.dumps(send_obj)
    ret = requests.post(url,data=send_json)
    ret_dict = json.loads(ret.text)

    return ret_dict['status']


if __name__ == '__main__':

    file_path = '6141a42ee0242c2ed83c25b7_1642495513_C_16k.data'
    # file_path = '61bc239ce0242b1f343b11ac_1640591857_16k.data'
    device_id = '619dddf0df242a042c6cddf0'
    line_id = '61bc239ce0242b1f343b11ac'

    flag, reason = save_info(file_path,device_id)
    # print(flag)
    # print(reason)

    # ret = send_sample_command(device_id,line_id)
    # print(ret)
=======
from datetime import datetime
from db_pool import POOL
import traceback
import config
import os
import requests
import json

def sent_info_to_db(device_id:str, line_id:str,
                    file_path:str, file_type:str,
                    frequency:int, create_date:datetime, 
                    comment:str):
    """
    表名:
    jala_file_upload
    属性:
    id: 每条记录的主键，插入数据时自动生成（类似 00017aa476fe4844810013dea7de0b8c）
    device_id: 网关id（类似 5e6726854c1d6e26f8152666）
    line_id: 线路id（类似 5df31a6b4c1d6e2da886dd7a）
    file_path: 文件路径（字符串，长度不定）
    file_type: 文件类型（字符串，长度不定）
    frequency: 采样频率（整型，单位为Hz）
    create_date: 数据采集时间（datetime类型）
    comment: 备注信息（字符串，长度不定）
    """

    sql = "INSERT INTO jala_file_upload "\
        "(id,device_id,line_id,file_path,file_type,frequency,create_date,comment) "\
        "VALUES ( REPLACE(UUID(),'-',''),'%s','%s','%s','%s','%s','%s','%s');"\
                %(device_id,line_id,file_path,file_type,frequency,
                create_date.strftime(config.DATETIME_FORMAT),comment)
    # 从连接池获取数据库连接
    conn_hy = POOL.connection()
    cursor_hy = conn_hy.cursor()
    try:
        ret = cursor_hy.execute(sql)
        cursor_hy.connection.commit()
    except:
        # 异常处理
        reason = traceback.format_exc()
        return False, reason
    # 释放数据库连接
    cursor_hy.close()
    conn_hy.close()

    return True, 'success'


# 6141a42ee0242c2ed83c25b7_1642495513_C_16k.data
# 61bc3fe7e0242b1f343b179a_1640136602_16k.data
def save_info(file_name:str,save_path:str,device_id:str,comment='',file_type='test'):

    file_name = file_name.split('.')[0]
    file_name_split = file_name.split('_')
    line_id = file_name_split[0]
    time_stamp = int(file_name_split[1])
    create_date = datetime.fromtimestamp(time_stamp)
    file_type = file_name_split[2]
    frequency = int(file_name_split[3][:-1])*1000
    # db excute
    flag, reason = sent_info_to_db(device_id,line_id,save_path,file_type,frequency,create_date,comment)
    return flag, reason


def send_sample_command(device_id:str, line_id:str, value:int):
    """
    {"status":" success | fail | offline | not exist "}
    value:(目前电流电压的文件标号是反的，实际是C代表电流，U代表电压)
        0:电流(实际是电压)
        1:电压(实际是电流)
        2:电流+电压
    """
    url = config.SAMPLE_COMMAND_URL
    send_obj = {
        "deviceId":device_id,
        "lineId":line_id,
        "value":value
    }
    send_json = json.dumps(send_obj)
    ret = requests.post(url,data=send_json)
    ret_dict = json.loads(ret.text)

    return ret_dict['status']


if __name__ == '__main__':

    file_path = '6141a42ee0242c2ed83c25b7_1642495513_C_16k.data'
    # file_path = '61bc239ce0242b1f343b11ac_1640591857_16k.data'
    device_id = '619dddf0df242a042c6cddf0'
    line_id = '61bc239ce0242b1f343b11ac'

    flag, reason = save_info(file_path,device_id)
    # print(flag)
    # print(reason)

    # ret = send_sample_command(device_id,line_id)
    # print(ret)
>>>>>>> 3cf9892 (0215-version)
    passs