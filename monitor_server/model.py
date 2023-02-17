<<<<<<< HEAD
import torch.nn as nn
import torch
import torch.nn.functional as F
import numpy as np

def xavier_init(m):
    if type(m) == nn.Linear:
        nn.init.xavier_normal_(m.weight)#用正态分布的数据填充这个张量
        if m.bias is not None:
           m.bias.data.fill_(0.0)
class LinearLayer(nn.Module):
    def __init__(self, in_dim, out_dim):
        super().__init__()
        self.clf = nn.Sequential(nn.Linear(in_dim, out_dim))
        self.clf.apply(xavier_init)

    def forward(self, x):
        x = self.clf(x)
        return x
class MYmodel(nn.Module):
    def __init__(self,in_dim,out_dim):
        super().__init__()
        self.MyClasifier = []
        x1 = LinearLayer(in_dim,200)
        x1_1 = nn.Dropout(p=0.2)
        self.MyClasifier.append(x1)
        self.MyClasifier.append(nn.ReLU())
        self.MyClasifier.append(x1_1)
        x3 = LinearLayer(200,out_dim)
        self.MyClasifier.append(x3)
        self.MyClasifier = nn.Sequential(*self.MyClasifier)
    def forward(self,data):
        self.MyClasifier.train()
        logits = self.MyClasifier(data)
        return logits
    def myeval(self,data):
        self.MyClasifier.eval()
        with torch.no_grad():
            logits = self.MyClasifier(data)
        return logits


=======
import torch.nn as nn
import torch
import torch.nn.functional as F
import numpy as np

def xavier_init(m):
    if type(m) == nn.Linear:
        nn.init.xavier_normal_(m.weight)#用正态分布的数据填充这个张量
        if m.bias is not None:
           m.bias.data.fill_(0.0)
class LinearLayer(nn.Module):
    def __init__(self, in_dim, out_dim):
        super().__init__()
        self.clf = nn.Sequential(nn.Linear(in_dim, out_dim))
        self.clf.apply(xavier_init)

    def forward(self, x):
        x = self.clf(x)
        return x
class MYmodel(nn.Module):
    def __init__(self,in_dim,out_dim):
        super().__init__()
        self.MyClasifier = []
        x1 = LinearLayer(in_dim,200)
        x1_1 = nn.Dropout(p=0.2)
        self.MyClasifier.append(x1)
        self.MyClasifier.append(nn.ReLU())
        self.MyClasifier.append(x1_1)
        x3 = LinearLayer(200,out_dim)
        self.MyClasifier.append(x3)
        self.MyClasifier = nn.Sequential(*self.MyClasifier)
    def forward(self,data):
        self.MyClasifier.train()
        logits = self.MyClasifier(data)
        return logits
    def myeval(self,data):
        self.MyClasifier.eval()
        with torch.no_grad():
            logits = self.MyClasifier(data)
        return logits


>>>>>>> 3cf9892 (0215-version)
