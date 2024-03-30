import FinanceDataReader as fdr
import pandas as pd
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta
from hmmlearn.hmm import GaussianHMM
import itertools

def min_max_normalize(data):
    min_val = np.min(data)
    max_val = np.max(data)
    if max_val == min_val: 
        return data - min_val # 0
    else:
        normalized_data = (data - min_val) / (max_val - min_val)
        return normalized_data
        
def inverse_min_max_normalize(norm_data, original_min, original_max):
    return norm_data * (original_max - original_min) + original_min

class HMM:
    def __init__(self, code, date):
        today = datetime.datetime.strptime(date, "%Y-%m-%d")
        bef = today - relativedelta(months=12)
        bef_str = bef.strftime("%Y-%m-%d")
        data = fdr.DataReader(code, bef_str, date)
        for target_day in range(1,8):
            data[f'ret{target_day}'] = data['Close'].shift(-target_day)
        self.close = data.iloc[-1]['Close']
        self.data = data.dropna()

    def augment_features(self, dataframe):
        for i in range(1,8):
            globals()[f'delCloseRet{i}'] = min_max_normalize((dataframe[f'ret{i}']-dataframe['Close'])/dataframe['Close']) # 종가 대비 i일뒤 종가의 변화율
        
        new_df = {}
        for i in range(1,8):
            new_df[f'delCloseRet{i}'] = globals()[f'delCloseRet{i}']
        new_df = pd.DataFrame(new_df)        
        new_df.set_index(dataframe.index, inplace=True)        
        return new_df

    def extract_features(self, dataframe):
        return np.column_stack((dataframe['delCloseRet1'], dataframe['delCloseRet2'], dataframe['delCloseRet3'],
                                dataframe['delCloseRet4'], dataframe['delCloseRet5'], dataframe['delCloseRet6'], dataframe['delCloseRet7']))

    def forecast(self):
        model = GaussianHMM(n_components=4)
        feature = self.augment_features(self.data)
        features = self.extract_features(feature)
        model.fit(features)

        # Generating possible sequences
        augmented = self.augment_features(self.data)
        for i in range(1,8):
            globals()[f'ret{i}'] = augmented[f'delCloseRet{i}']
            # 각각 다른 시점의 주가 변화율에 대한 가능한 값들의 시퀀스
            globals()[f'sample_space_ret{i}'] = np.linspace(globals()[f'ret{i}'].min(), globals()[f'ret{i}'].max(), 3) # i일 후의 주가 변화율에 대한 가능한 값들
        
        # 7일 동안의 주가 변화에 대한 모든 가능한 시나리오
        possible_outcomes = np.array(list(itertools.product(
            globals()['sample_space_ret1'], globals()['sample_space_ret2'], globals()['sample_space_ret3'],
            globals()['sample_space_ret4'], globals()['sample_space_ret5'], globals()['sample_space_ret6'], globals()['sample_space_ret7'])))
        
        ## Prediction
        num_latent_days = 10 # the data of the last to predict the closing price of the current day
        # Acquire test data features for these days
        previous_data = self.extract_features(self.augment_features(pd.DataFrame(self.data.iloc[-num_latent_days:])))
        
        outcome_scores = []
        for outcome in possible_outcomes:
            # Append each outcome one by one with replacement to see which sequence generates the highest score
            total_data = np.row_stack((previous_data, outcome))
            outcome_scores.append(model.score(total_data))

        # Take the most probable outcome as the one with the highest score
        most_probable_outcome = possible_outcomes[np.argmax(outcome_scores)]

        predicted_close_prices = []
        for i, change_rate_norm in enumerate(most_probable_outcome):
            change_rate = inverse_min_max_normalize(change_rate_norm, 
                                                    ((self.data[f'ret{i+1}']-self.data['Close'])/self.data['Close']).min(), 
                                                    ((self.data[f'ret{i+1}']-self.data['Close'])/self.data['Close']).max())
            predicted_close_prices.append(self.close * (1+change_rate))
            
        return predicted_close_prices
