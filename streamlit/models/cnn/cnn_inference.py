import numpy as np
import matplotlib.pyplot as plt
import torch
import pandas as pd
import yfinance as yf
import torch.nn as nn
from collections import OrderedDict
import matplotlib.pyplot as plt

from PIL import Image

import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)

from datetime import datetime
from dateutil.relativedelta import relativedelta

from pytorch_grad_cam import GradCAM, HiResCAM, ScoreCAM, GradCAMPlusPlus, AblationCAM, XGradCAM, EigenCAM, FullGrad
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from pytorch_grad_cam.utils.image import show_cam_on_image

class CNN5d(nn.Module):
    # Input: [N, (1), 32, 15]; Output: [N, 2]
    # Two Convolution Blocks
    
    def init_weights(self, m):
        if isinstance(m, nn.Linear) or isinstance(m, nn.Conv2d):
            torch.nn.init.xavier_uniform_(m.weight)
            m.bias.data.fill_(0.01)
    
    def __init__(self):
        super(CNN5d, self).__init__()
        self.conv1 = nn.Sequential(OrderedDict([
            ('Conv', nn.Conv2d(1, 64, (5, 3), padding=(2, 1), stride=(1, 1), dilation=(1, 1))), # output size: [N, 64, 32, 15]
            ('BN', nn.BatchNorm2d(64, affine=True)),
            ('ReLU', nn.ReLU()),
            ('Max-Pool', nn.MaxPool2d((2,1))) # output size: [N, 64, 16, 15]
        ]))
        self.conv1 = self.conv1.apply(self.init_weights)
        
        self.conv2 = nn.Sequential(OrderedDict([
            ('Conv', nn.Conv2d(64, 128, (5, 3), padding=(2, 1), stride=(1, 1), dilation=(1, 1))), # output size: [N, 128, 16, 15]
            ('BN', nn.BatchNorm2d(128, affine=True)),
            ('ReLU', nn.ReLU()),
            ('Max-Pool', nn.MaxPool2d((2,1))) # output size: [N, 128, 8, 15]
        ]))
        self.conv2 = self.conv2.apply(self.init_weights)

        self.DropOut = nn.Dropout(p=0.5)
        self.FC = nn.Linear(15360, 2)
        self.init_weights(self.FC)
        self.Softmax = nn.Softmax(dim=1)

    def forward(self, x): # input: [N, 32, 15]
        x = x.unsqueeze(1).to(torch.float32)   # output size: [N, 1, 32, 15]
        x = self.conv1(x) # output size: [N, 64, 16, 15]
        x = self.conv2(x) # output size: [N, 128, 8, 15]
        x = self.DropOut(x.view(x.shape[0], -1))
        x = self.FC(x) # output size: [N, 2]
        x = self.Softmax(x)
        
        return x
    
class CNN20d(nn.Module):
    # Input: [N, (1), 64, 60]; Output: [N, 2]
    # Three Convolution Blocks
    
    def init_weights(self, m):
        if isinstance(m, nn.Linear) or isinstance(m, nn.Conv2d):
            torch.nn.init.xavier_uniform_(m.weight)
            m.bias.data.fill_(0.01)
    
    def __init__(self):
        super(CNN20d, self).__init__()
        self.conv1 = nn.Sequential(OrderedDict([
            ('Conv', nn.Conv2d(1, 64, (5, 3), padding=(3, 1), stride=(3, 1), dilation=(2, 1))), # output size: [N, 64, 21, 60]
            ('BN', nn.BatchNorm2d(64, affine=True)),
            ('ReLU', nn.ReLU()),
            ('Max-Pool', nn.MaxPool2d((2,1))) # output size: [N, 64, 10, 60]
        ]))
        self.conv1 = self.conv1.apply(self.init_weights)
        
        self.conv2 = nn.Sequential(OrderedDict([
            ('Conv', nn.Conv2d(64, 128, (5, 3), padding=(3, 1), stride=(1, 1), dilation=(1, 1))), # output size: [N, 128, 12, 60]
            ('BN', nn.BatchNorm2d(128, affine=True)),
            ('ReLU', nn.ReLU()),
            ('Max-Pool', nn.MaxPool2d((2,1))) # output size: [N, 128, 6, 60]
        ]))
        self.conv2 = self.conv2.apply(self.init_weights)
        
        self.conv3 = nn.Sequential(OrderedDict([
            ('Conv', nn.Conv2d(128, 256, (5, 3), padding=(2, 1), stride=(1, 1), dilation=(1, 1))), # output size: [N, 256, 6, 60]
            ('BN', nn.BatchNorm2d(256, affine=True)),
            ('ReLU', nn.ReLU()),
            ('Max-Pool', nn.MaxPool2d((2,1))) # output size: [N, 256, 3, 60]
        ]))
        self.conv3 = self.conv3.apply(self.init_weights)

        self.DropOut = nn.Dropout(p=0.5)
        self.FC = nn.Linear(46080, 2)
        self.init_weights(self.FC)
        self.Softmax = nn.Softmax(dim=1)

    def forward(self, x): # input: [N, 64, 60]
        x = x.unsqueeze(1).to(torch.float32)   # output size: [N, 1, 64, 60]
        x = self.conv1(x) # output size: [N, 64, 10, 60]
        x = self.conv2(x) # output size: [N, 128, 6, 60]
        x = self.conv3(x) # output size: [N, 256, 3, 60]
        x = self.DropOut(x.view(x.shape[0], -1))
        x = self.FC(x) # output size: [N, 2]
        x = self.Softmax(x)
        
        return x
    
def get_CNN5d_5d():
    model = CNN5d()
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    state_dict = torch.load('models/cnn/I5R5_Model.tar',map_location=torch.device(device))
    model.load_state_dict(state_dict['model_state_dict'])
    return model

def get_CNN5d_20d():
    model = CNN5d()
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    state_dict = torch.load('models/cnn/I5R20_Model.tar',map_location=torch.device(device))
    model.load_state_dict(state_dict['model_state_dict'])
    return model

def get_CNN20d_5d():
    model = CNN20d()
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    state_dict = torch.load('models/cnn/I20R5_Model.tar',map_location=torch.device(device))
    model.load_state_dict(state_dict['model_state_dict'])
    return model

def get_CNN20d_20d():
    model = CNN20d()
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    state_dict = torch.load('models/cnn/I20R20_Model.tar',map_location=torch.device(device))
    model.load_state_dict(state_dict['model_state_dict'])
    return model

def rasterize(data_frame, period):
    if period == 5:
        d = 5
        image_size = (32, 15)
    elif period == 20:
        d = 20
        image_size = (64, 60)

    price_slice = data_frame.iloc[-d:][['Open', 'High', 'Low', 'Close']].reset_index(drop=True)

    price_slice = (price_slice - np.min(price_slice.values))/(np.max(price_slice.values) - np.min(price_slice.values))

    price_slice = price_slice.apply(lambda x: x*(25-1)+7).astype(int)

    image = np.zeros(image_size)

    for i in range(len(price_slice)):
        image[price_slice.loc[i]['Open'], i*3] = 255.
        image[price_slice.loc[i]['Low']:price_slice.loc[i]['High']+1, i*3+1] = 255.
        image[price_slice.loc[i]['Close'], i*3+2] = 255.

    return image


def preprocess(image):
    input = torch.Tensor(np.array(image))
    input = input.unsqueeze(0)
    return input


def image_to_np(data,period):
    rasterized_img = rasterize(data,period)
    return rasterized_img

def image_to_tensor(data,period):
    rasterized_img = rasterize(data,period)
    tensor_img = preprocess(rasterized_img)
    return tensor_img

def inference(model, data, period):

    data.reset_index(drop=False,inplace = True)
    rasterized_img = rasterize(data, period)
    
    input = preprocess(rasterized_img)
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    input = input.to(device)
    output = model(input)[0]

    return output


def grad_cam(model, input):
    cam = GradCAM(model=model, target_layers=model.conv1)
    targets = [ClassifierOutputTarget(1)]
    grayscale_cam = cam(input_tensor=input, targets=targets)
    grayscale_cam = grayscale_cam[0, :]
    return grayscale_cam

def time_calc(duration, multiplier):
    unit = duration[-1]

    if unit == 'o':
        value = int(duration[:-2])
        delta = relativedelta(months=value)

    elif unit == 'k':
        value = int(duration[:-2])
        delta = relativedelta(weeks=value)

    elif unit == 'd':
        value = int(duration[:-1])
        delta = relativedelta(days=value)

    elif unit == 'm':
        value = int(duration[:-1])
        delta = relativedelta(minutes=value)

    else:
        raise ValueError("잘못된 시간 단위입니다.")
    
    m_delta = delta * multiplier
    result = ""
    
    if m_delta.years != 0:
        result += f"{m_delta.years}년"
        m_delta -= relativedelta(years=m_delta.years)

    if m_delta.months != 0:
        result += f" {m_delta.months}월"
        m_delta -= relativedelta(months=m_delta.months)

    if m_delta.weeks != 0:
        result += f" {m_delta.weeks}주"
        m_delta -= relativedelta(weeks=m_delta.weeks)
    
    if m_delta.days != 0:
        result += f" {m_delta.days}일"
        m_delta -= relativedelta(days=m_delta.days)

    if m_delta.hours != 0:
        result += f" {m_delta.hours}시간"
        m_delta -= relativedelta(hours=m_delta.hours)

    if m_delta.minutes != 0:
        result += f" {m_delta.minutes}분"

    return result.strip()