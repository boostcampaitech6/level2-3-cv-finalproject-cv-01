import FinanceDataReader as fdr
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from sklearn.preprocessing import MinMaxScaler
import FinanceDataReader as fdr
import datetime
from dateutil.relativedelta import relativedelta

# LSTM 모델 클래스
class LSTMModel(nn.Module):
    def __init__(self, input_size=1, hidden_layer_size=100, output_size=1):
        super().__init__()
        self.hidden_layer_size = hidden_layer_size
        self.lstm = nn.LSTM(input_size, hidden_layer_size)
        self.linear = nn.Linear(hidden_layer_size, output_size)
        self.hidden_cell = (torch.zeros(1,1,self.hidden_layer_size),
                            torch.zeros(1,1,self.hidden_layer_size))

    def forward(self, input_seq):
        lstm_out, self.hidden_cell = self.lstm(input_seq.view(len(input_seq) ,1, -1), self.hidden_cell)
        predictions = self.linear(lstm_out.view(len(input_seq), -1))
        return predictions[-1]

model_state_dict = torch.load('./dags/ts_model/weight/lstm_model.pth')
model = LSTMModel()
model.load_state_dict(model_state_dict)
model.eval()

def lstm_inference(code, date):
    today = datetime.datetime.strptime(date, "%Y-%m-%d")
    bef = today - relativedelta(months=12)
    bef_str = bef.strftime("%Y-%m-%d")
    data = fdr.DataReader(code, bef_str, date)
    
    # 데이터 로딩 및 스케일링
    close_data = data[['Close']].ffill()
    scaler = MinMaxScaler(feature_range=(-1, 1))
    close_data_scaled = scaler.fit_transform(close_data.values.reshape(-1, 1))

    # 일주일 주가 예측
    future_days = 7
    seq_length = 1
    future_predictions = []
    with torch.no_grad():
        last_seq = torch.tensor(close_data_scaled[-seq_length:], dtype=torch.float32)
        for _ in range(future_days):
            pred = model(last_seq.view(1, seq_length, -1))
            future_predictions.append(pred.item())
            last_seq = torch.cat((last_seq[1:], pred.reshape(1, 1)))

    # 예측된 값을 원래 스케일로 되돌림
    future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1)).flatten()
    return future_predictions