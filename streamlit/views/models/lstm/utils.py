import torch
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def load_data(stock, look_back):
    data_raw = stock # convert to numpy array
    data = []
    
    # create all possible sequences of length look_back
    for index in range(len(data_raw) - look_back): 
        data.append(data_raw[index: index + look_back])
    
    data = np.array(data)
    test_set_size = int(np.round(0.2*data.shape[0]))
    train_set_size = data.shape[0] - (test_set_size)
    
    x_train = data[:train_set_size,:-1,:]
    y_train = data[:train_set_size,-1,:]
    
    x_test = data[train_set_size:,:-1]
    y_test = data[train_set_size:,-1,:]
    
    return [x_train, y_train, x_test, y_test]

def predict(n, model, close_data, look_back, scaler):
    model.eval()  # 모델을 평가 모드로 설정
    prediction_list = close_data[-look_back:]
    
    for _ in range(n):
        x = prediction_list[-look_back:]
        x = torch.from_numpy(x).float().reshape((1, look_back, 1))
        with torch.no_grad():  # 추론 시에는 기울기 계산을 하지 않음
            out = model(x).item()
        prediction_list = np.append(prediction_list, out)
    
    prediction_list = prediction_list[look_back-1:]
    return scaler.inverse_transform(prediction_list.reshape(-1, 1)).flatten()

def predict_dates(num_prediction, data_close):
    last_date = data_close.index.max()
    prediction_dates = pd.date_range(last_date, periods=num_prediction+1).tolist()
    return prediction_dates