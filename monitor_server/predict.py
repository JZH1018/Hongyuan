<<<<<<< HEAD
import numpy as np
import pickle
from scipy.fft import rfft
import torch
import glob
import os
import torch.nn.functional as F
def MyRfft(x_test):
    xx_test = rfft(x_test)
    xx_test = abs(xx_test)
    return xx_test

def raw_to_int_or_float(data_list):
    str_data_list = [ (data_list[i*2]+data_list[i*2+1]) for i in range(len(data_list)//2) ]
    bin_data_list = [ bin(int(a,16))[2:].zfill(20) for a in str_data_list ]
    int_data_list = [( -int(a[0])*(2**(19)) + int(a[1:],2)) for a in bin_data_list]
    float_data_list = [( -float(a[0])*(2**(19)) + float(int(a[1:],2))) for a in bin_data_list]
    return float_data_list

def predict(path):
    ###注意！！这里正式测试时要修改
    content_split = []
    with open(path) as f:
        content = f.read()
        content_split = content.strip().split(' ')
    if len(content_split)==1020:
        float_list = raw_to_int_or_float(content_split)
        float_array = np.array(float_list)
        float_array = float_array.reshape((1,510))
        rfft_data = MyRfft(float_list)
    else:
        print('数据维度错误，无法预测！')
        return

    #归一化
    rfft_data[:] = rfft_data[:] / np.linalg.norm(rfft_data[:])

    #进行测试
    test = rfft_data
    with open('./model/dianhu/0104bp_model.pkl','rb') as f:
        Myclassifier = pickle.load(f)

    #模型转换为张量
    test_tensor = torch.tensor(test)
    test_tensor = test_tensor.to(torch.float32)
    logits = Myclassifier.myeval(test_tensor)
    logits = logits.unsqueeze(0)
    result = logits.argmax(1)
    return result.numpy(),float_list
if __name__ == '__main__':
    path_test = './Test/12.29电弧/电煮锅+空气净化器/电弧/'
    paths = glob.glob(os.path.join(path_test,'*电流.txt'))
    label = []
    for path in paths:
        res = predict(path)
        label.append(res[0])
    print(label)

    

=======
import numpy as np
import pickle
from scipy.fft import rfft
import torch
import glob
import os
import torch.nn.functional as F
def MyRfft(x_test):
    xx_test = rfft(x_test)
    xx_test = abs(xx_test)
    return xx_test

def raw_to_int_or_float(data_list):
    str_data_list = [ (data_list[i*2]+data_list[i*2+1]) for i in range(len(data_list)//2) ]
    bin_data_list = [ bin(int(a,16))[2:].zfill(20) for a in str_data_list ]
    int_data_list = [( -int(a[0])*(2**(19)) + int(a[1:],2)) for a in bin_data_list]
    float_data_list = [( -float(a[0])*(2**(19)) + float(int(a[1:],2))) for a in bin_data_list]
    return float_data_list

def predict(path):
    ###注意！！这里正式测试时要修改
    content_split = []
    with open(path) as f:
        content = f.read()
        content_split = content.strip().split(' ')
    if len(content_split)==1020:
        float_list = raw_to_int_or_float(content_split)
        float_array = np.array(float_list)
        float_array = float_array.reshape((1,510))
        rfft_data = MyRfft(float_list)
    else:
        print('数据维度错误，无法预测！')
        return

    #归一化
    rfft_data[:] = rfft_data[:] / np.linalg.norm(rfft_data[:])

    #进行测试
    test = rfft_data
    with open('./model/dianhu/0104bp_model.pkl','rb') as f:
        Myclassifier = pickle.load(f)

    #模型转换为张量
    test_tensor = torch.tensor(test)
    test_tensor = test_tensor.to(torch.float32)
    logits = Myclassifier.myeval(test_tensor)
    logits = logits.unsqueeze(0)
    result = logits.argmax(1)
    return result.numpy(),float_list
if __name__ == '__main__':
    path_test = './Test/12.29电弧/电煮锅+空气净化器/电弧/'
    paths = glob.glob(os.path.join(path_test,'*电流.txt'))
    label = []
    for path in paths:
        res = predict(path)
        label.append(res[0])
    print(label)

    

>>>>>>> 3cf9892 (0215-version)
