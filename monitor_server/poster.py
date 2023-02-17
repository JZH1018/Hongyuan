import os.path
import time
import config
import json

class Logger(object):
    def __init__(self, save_dir):
        os.makedirs(save_dir, exist_ok=True)
        self.save_dir = save_dir

    def print(self, t, resp, req):
        ret = json.loads(resp)

        lineid = ret['lineID']
        msg = ret['message'] + ret['message_2']
        timeStamp = ret['timeStamp']
        status_code = req.status_code

        # msg = req.text.encode().decode("unicode_escape")
        content = f"[{t}]\t\t\t状态码:{status_code}\t\t\t线路id:{lineid}\t\t\t数据创建时间:{timeStamp}\n返回信息:{msg}\n\n"

        return content

    def write_log(self, resp, req):
        # 分日期建立log文件
        create_time = time.localtime()
        create_time = time.strftime(config.DATETIME_FORMAT, create_time)
        date = create_time[:10]
        t = create_time[11:]
        log_filename = date + '_postlog.txt'
        log_path = os.path.join(self.save_dir, log_filename)

        # 打开log文件
        if not os.path.exists(log_path):
            log_file = open(log_path, 'w+', encoding='utf-8')
        else:
            log_file = open(log_path, 'a+', encoding='utf-8')

        content = self.print(t, resp, req)
        log_file.write(content)
        log_file.flush()