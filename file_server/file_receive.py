<<<<<<< HEAD
# -*- coding: utf-8 -*-
# 高并发相关
from gevent import monkey
monkey.patch_all()
from gevent.pywsgi import WSGIServer
from gevent.lock import BoundedSemaphore
from threading import Thread,Lock

# 系统库
import time
import os
import copy
import traceback
import json
import argparse
from datetime import datetime
from datetime import date

# 基础网络库
from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flasgger import Swagger,swag_from
from werkzeug.datastructures import FileStorage

# 自定义库
import config
import utils

start_time = time.time()


"""
命令行参数解析
"""
cmd_parser = argparse.ArgumentParser(description='file server.')
cmd_parser.add_argument('--host', type=str, default=config.HOST)
cmd_parser.add_argument('--ip', type=str, default=config.IP)
cmd_parser.add_argument('--port', type=int, default=config.PORT)
cmd_parser.add_argument('--dev', type=bool, default=config.DEV)
cmd_args = cmd_parser.parse_args()

'''
初始化flask
'''
app = Flask(__name__)
api = Api(app)
print('flask init success!')


'''
参数解析器+参数校验
'''
parser = reqparse.RequestParser()
parser.add_argument('file', type=FileStorage, location='files')
parser.add_argument('devicename', type=str)



class Test(Resource):
    """
    测试上传文件
    """
    def post(self):
        args = parser.parse_args()
        try:
            file = args['file']
            device_id = args['devicename']

            # save file
            date_str = date.today().strftime(config.DATE_FORMAT)
            save_dir = '%s/%s'%(config.file_dir, date_str)
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            save_path = '%s/%s'%(save_dir,file.filename)
            file.save(save_path)
            print(save_path, device_id)
            # save file info
            utils.save_info(file.filename,save_path,device_id)

        except:
            t_reason = traceback.format_exc()
            print(t_reason)
            response = jsonify({'reason':t_reason ,'status':'fail'})
            response.status_code = 500
            return response

        response = jsonify({'file':file.filename ,'devicename':device_id,'status':'success'})
        response.status_code = 200
        return response


# 映射地址
api.add_resource(Test, '/test')



if __name__ == '__main__':
    if cmd_args.dev:
        print('development server start at %s:%d!'%(cmd_args.host, cmd_args.port))
        end_time = time.time()
        print('time cost: %.4f s'%(end_time-start_time))
        app.run(host=cmd_args.host, port=cmd_args.port, debug=True, threaded=False)  # 开发环境
    else:
        # 单进程+多协程
        print('production server start at %s:%d!'%(cmd_args.host, cmd_args.port))
        end_time = time.time()
        print('time cost: %.4f s' % (end_time - start_time))
        WSGIServer((cmd_args.host, cmd_args.port), app).serve_forever()  # 生产环境
=======
# -*- coding: utf-8 -*-
# 高并发相关
from gevent import monkey
monkey.patch_all()
from gevent.pywsgi import WSGIServer
from gevent.lock import BoundedSemaphore
from threading import Thread,Lock

# 系统库
import time
import os
import copy
import traceback
import json
import argparse
from datetime import datetime
from datetime import date

# 基础网络库
from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flasgger import Swagger,swag_from
from werkzeug.datastructures import FileStorage

# 自定义库
import config
import utils

start_time = time.time()


"""
命令行参数解析
"""
cmd_parser = argparse.ArgumentParser(description='file server.')
cmd_parser.add_argument('--host', type=str, default=config.HOST)
cmd_parser.add_argument('--ip', type=str, default=config.IP)
cmd_parser.add_argument('--port', type=int, default=config.PORT)
cmd_parser.add_argument('--dev', type=bool, default=config.DEV)
cmd_args = cmd_parser.parse_args()

'''
初始化flask
'''
app = Flask(__name__)
api = Api(app)
print('flask init success!')


'''
参数解析器+参数校验
'''
parser = reqparse.RequestParser()
parser.add_argument('file', type=FileStorage, location='files')
parser.add_argument('devicename', type=str)



class Test(Resource):
    """
    测试上传文件
    """
    def post(self):
        args = parser.parse_args()
        try:
            file = args['file']
            device_id = args['devicename']

            # save file
            date_str = date.today().strftime(config.DATE_FORMAT)
            save_dir = '%s/%s'%(config.file_dir, date_str)
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            save_path = '%s/%s'%(save_dir,file.filename)
            file.save(save_path)
            print(save_path, device_id)
            # save file info
            utils.save_info(file.filename,save_path,device_id)

        except:
            t_reason = traceback.format_exc()
            print(t_reason)
            response = jsonify({'reason':t_reason ,'status':'fail'})
            response.status_code = 500
            return response

        response = jsonify({'file':file.filename ,'devicename':device_id,'status':'success'})
        response.status_code = 200
        return response


# 映射地址
api.add_resource(Test, '/test')



if __name__ == '__main__':
    if cmd_args.dev:
        print('development server start at %s:%d!'%(cmd_args.host, cmd_args.port))
        end_time = time.time()
        print('time cost: %.4f s'%(end_time-start_time))
        app.run(host=cmd_args.host, port=cmd_args.port, debug=True, threaded=False)  # 开发环境
    else:
        # 单进程+多协程
        print('production server start at %s:%d!'%(cmd_args.host, cmd_args.port))
        end_time = time.time()
        print('time cost: %.4f s' % (end_time - start_time))
        WSGIServer((cmd_args.host, cmd_args.port), app).serve_forever()  # 生产环境
>>>>>>> 3cf9892 (0215-version)
