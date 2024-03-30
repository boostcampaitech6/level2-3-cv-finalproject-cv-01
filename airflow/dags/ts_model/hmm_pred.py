import FinanceDataReader as fdr
import pandas as pd
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta
from hmmlearn.hmm import GaussianHMM
import itertools

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
        delCloseRet1 = (dataframe['ret1']-dataframe['Close'])/dataframe['Close'] # 종가 대비 다음날 종가의 변화율
        delCloseRet2 = (dataframe['ret2']-dataframe['Close'])/dataframe['Close'] # 종가 대비 이틀뒤 종가의 변화율
        delCloseRet3 = (dataframe['ret3']-dataframe['Close'])/dataframe['Close'] 
        delCloseRet4 = (dataframe['ret4']-dataframe['Close'])/dataframe['Close']
        delCloseRet5 = (dataframe['ret5']-dataframe['Close'])/dataframe['Close'] 
        delCloseRet6 = (dataframe['ret6']-dataframe['Close'])/dataframe['Close'] 
        delCloseRet7 = (dataframe['ret7']-dataframe['Close'])/dataframe['Close'] 
        
        new_dataframe = pd.DataFrame({'delCloseRet1': delCloseRet1,
                                    'delCloseRet2': delCloseRet2,
                                    'delCloseRet3': delCloseRet3,
                                    'delCloseRet4': delCloseRet4,
                                    'delCloseRet5': delCloseRet5,
                                    'delCloseRet6': delCloseRet6,
                                    'delCloseRet7': delCloseRet7,
                                    })
        
        new_dataframe.set_index(dataframe.index)
        
        return new_dataframe

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
        ret1 = augmented['delCloseRet1']
        ret2 = augmented['delCloseRet2']
        ret3 = augmented['delCloseRet3']
        ret4 = augmented['delCloseRet4']
        ret5 = augmented['delCloseRet5']
        ret6 = augmented['delCloseRet6']
        ret7 = augmented['delCloseRet7']

        # 각각 다른 시점의 주가 변화율에 대한 가능한 값들의 시퀀스
        sample_space_ret1 = np.linspace(ret1.min(), ret1.max(), 3) # 다음날의 주가 변화율에 대한 가능한 값들
        sample_space_ret2 = np.linspace(ret2.min(), ret2.max(), 3) # 이틀 후의 주가 변화율에 대한 가능한 값들
        sample_space_ret3 = np.linspace(ret3.min(), ret3.max(), 3)
        sample_space_ret4 = np.linspace(ret1.min(), ret4.max(), 3)
        sample_space_ret5 = np.linspace(ret2.min(), ret5.max(), 3)
        sample_space_ret6 = np.linspace(ret3.min(), ret6.max(), 3)
        sample_space_ret7 = np.linspace(ret1.min(), ret7.max(), 3)

        # 7일 동안의 주가 변화에 대한 모든 가능한 시나리오
        possible_outcomes = np.array(list(itertools.product(sample_space_ret1, sample_space_ret2, sample_space_ret3,
                                                            sample_space_ret4, sample_space_ret5, sample_space_ret6,
                                                            sample_space_ret7)))
        
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
        
        pred1 = self.close * (1 + most_probable_outcome[0])
        pred2 = self.close * (1 + most_probable_outcome[1])
        pred3 = self.close * (1 + most_probable_outcome[2])
        pred4 = self.close * (1 + most_probable_outcome[3])
        pred5 = self.close * (1 + most_probable_outcome[4])
        pred6 = self.close * (1 + most_probable_outcome[5])
        pred7 = self.close * (1 + most_probable_outcome[6])

        predicted_close_prices = [pred1, pred2, pred3, pred4, pred5, pred6, pred7]

        return predicted_close_prices
