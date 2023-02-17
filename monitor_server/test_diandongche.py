<<<<<<< HEAD
# 电动车检测
import numpy as np
import pickle
from scipy.fftpack import fft
# class Diandongche():
#     def __init__(self,model_path='model/diandongche.pkl'):
#         with open(model_path, 'rb') as f:
#             self.predictor = pickle.load(f)
#
#     def raw_to_int_or_float(self,path):
#         with open(path) as f:
#             data = f.read()
#             data_list = data.strip().split(' ')
#         str_data_list = [(data_list[i * 2] + data_list[i * 2 + 1]) for i in range(len(data_list) // 2)]
#         bin_data_list = [bin(int(a, 16))[2:].zfill(20) for a in str_data_list]
#         int_data_list = [(-int(a[0]) * (2 ** (19)) + int(a[1:], 2)) for a in bin_data_list]
#         float_data_list = [(-float(a[0]) * (2 ** (19)) + float(int(a[1:], 2))) for a in bin_data_list]
#         return float_data_list
#
#     def predict(self,c_path,u_path):
#         list_C = self.raw_to_int_or_float(c_path)
#         list_U = self.raw_to_int_or_float(u_path)
#         list_merge = list_C + list_U
#
#         # 异常处理：数据维度错误
#         if len(list_merge)!=1020:
#             y_pre = 0
#             return y_pre
#
#         x=np.array(list_merge)
#
#         x=x.reshape(1,-1)
#         y_pre=self.predictor.predict(x)
#         return y_pre
#
# class Diandongche_U():
#     def __init__(self,model_path='model/diandongche_U_6.0.pkl'):
#         with open(model_path, 'rb') as f:
#             self.predictor = pickle.load(f)
#
#     def raw_to_int_or_float(self,path):
#         with open(path) as f:
#             data = f.read()
#             data_list = data.strip().split(' ')
#         str_data_list = [(data_list[i * 2] + data_list[i * 2 + 1]) for i in range(len(data_list) // 2)]
#         bin_data_list = [bin(int(a, 16))[2:].zfill(20) for a in str_data_list]
#         int_data_list = [(-int(a[0]) * (2 ** (19)) + int(a[1:], 2)) for a in bin_data_list]
#         float_data_list = [(-float(a[0]) * (2 ** (19)) + float(int(a[1:], 2))) for a in bin_data_list]
#         return float_data_list
#
#     def predict(self,c_path,u_path):
#         list_C = self.raw_to_int_or_float(c_path)
#         list_U = self.raw_to_int_or_float(u_path)
#         list_merge = list_U
#
#         # 异常处理：数据维度错误
#         if len(list_merge)!=510:
#             y_pre = 0
#             return y_pre
#
#         x=np.array(list_merge)
#
#         x=x.reshape(1,-1)
#         y_pre=self.predictor.predict(x)
#
#         return y_pre


class Diandongche_Feature():
    def __init__(self,model_path='model/diandongche.pkl'):
        with open(model_path, 'rb') as f:
            self.predictor = pickle.load(f)

    def raw_to_int_or_float(self,path):
        with open(path) as f:
            data = f.read()
            data_list = data.strip().split(' ')
        str_data_list = [(data_list[i * 2] + data_list[i * 2 + 1]) for i in range(len(data_list) // 2)]
        bin_data_list = [bin(int(a, 16))[2:].zfill(20) for a in str_data_list]
        int_data_list = [(-int(a[0]) * (2 ** (19)) + int(a[1:], 2)) for a in bin_data_list]
        float_data_list = [(-float(a[0]) * (2 ** (19)) + float(int(a[1:], 2))) for a in bin_data_list]
        return float_data_list
    def extract_feature(self,time_series):
        data_freq = fft(time_series)
        mdata = np.abs(data_freq)
        pdata = np.angle(data_freq)
        _feature=np.concatenate((mdata,pdata))
        return _feature
    def predict(self,u_path):
        # list_C = self.raw_to_int_or_float(c_path)
        list_U = self.raw_to_int_or_float(u_path)
        
        
        list_merge = list_U
        
        
        # 异常处理：数据维度错误
        if len(list_merge)!=510:
            y_pre = 0
            print('dim error')
            return y_pre

        x=np.array(list_merge)
        x=self.extract_feature(x)
        
        x=x.reshape(1,-1)
        # print(x.shape)
        y_pre=self.predictor.predict(x)
        
        return y_pre

#
# # 这部分若不是主函数则不运行
# if __name__ == '__main__':
#     c_path='612eea81e0242b26405bdf34_1659519043_C_16k.data'
#     u_path='612eea81e0242b26405bdf34_1659519043_U_16k.data'
#     model=Diandongche_Feature(model_path='model/svm_rbf_model_feature.pkl')
#     model=Diandongche_U('model/svm_rbf_model_u_9.pkl')
#     y_pre=model.predict(c_path,u_path)
