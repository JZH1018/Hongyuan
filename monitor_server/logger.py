<<<<<<< HEAD
import logging
import logging.config
import os.path
import json


class Logger(object):
    def __init__(self, save_dir):
        os.makedirs(save_dir, exist_ok=True)
        self.save_dir = save_dir

    def print(self, dict_msg):  # dict_msg会传入一个字典
        t, msg_1, msg_2 = dict_msg['timeStamp'][11:], dict_msg['message'], dict_msg['message_2']
        line_id = dict_msg['lineID']
        if len(msg_1):
            msg = msg_1 + ' , ' + msg_2
            content = f"[{t}]\t\tline_id:{line_id}\t\t{msg}\n"
        else:
            content = f"[{t}]\t\tline_id:{line_id}\t\t{msg_2}\n"
        return content

    def write_log(self, msg):  # msg会传入一个json格式数据
        dict_msg = json.loads(msg)
        # 分日期建立log文件
        date = dict_msg['timeStamp'][:10]
        log_filename = date + '-log.txt'
        log_path = os.path.join(self.save_dir, log_filename)

        # 打开log文件
        if not os.path.exists(log_path):
            log_file = open(log_path, 'w+', encoding='utf-8')
        else:
            log_file = open(log_path, 'a+', encoding='utf-8')

        content = self.print(dict_msg)
        log_file.write(content)
=======
import logging
import logging.config
import os.path
import json


class Logger(object):
    def __init__(self, save_dir):
        os.makedirs(save_dir, exist_ok=True)
        self.save_dir = save_dir

    def print(self, dict_msg):  # dict_msg会传入一个字典
        t, msg_1, msg_2 = dict_msg['timeStamp'][11:], dict_msg['message'], dict_msg['message_2']
        line_id = dict_msg['lineID']
        if len(msg_1):
            msg = msg_1 + ' , ' + msg_2
            content = f"[{t}]\t\tline_id:{line_id}\t\t{msg}\n"
        else:
            content = f"[{t}]\t\tline_id:{line_id}\t\t{msg_2}\n"
        return content

    def write_log(self, msg):  # msg会传入一个json格式数据
        dict_msg = json.loads(msg)
        # 分日期建立log文件
        date = dict_msg['timeStamp'][:10]
        log_filename = date + '-log.txt'
        log_path = os.path.join(self.save_dir, log_filename)

        # 打开log文件
        if not os.path.exists(log_path):
            log_file = open(log_path, 'w+', encoding='utf-8')
        else:
            log_file = open(log_path, 'a+', encoding='utf-8')

        content = self.print(dict_msg)
        log_file.write(content)
>>>>>>> 3cf9892 (0215-version)
        log_file.flush()