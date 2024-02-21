import numpy as np
import pandas as pd
from hmmlearn.hmm import GaussianHMM
from tqdm import tqdm
import itertools
import plotly.graph_objs as go

class HMM:
    def __init__(self, data):
        self.data = data
        self.train_size = int(0.8*data.shape[0])
        self.train_data = self.data.iloc[0:self.train_size]
        self.test_data = self.data.iloc[self.train_size:]

        self.num_days_to_predict = 30

    def augment_features(self, dataframe):
        fracocp = (dataframe['Close']-dataframe['Open'])/dataframe['Open']
        frachp = (dataframe['High']-dataframe['Open'])/dataframe['Open']
        fraclp = (dataframe['Open']-dataframe['Low'])/dataframe['Open']
        new_dataframe = pd.DataFrame({'delOpenClose': fracocp,
                                    'delHighOpen': frachp,
                                    'delLowOpen': fraclp})
        new_dataframe.set_index(dataframe.index)
        
        return new_dataframe

    def extract_features(self, dataframe):
        return np.column_stack((dataframe['delOpenClose'], dataframe['delHighOpen'], dataframe['delLowOpen']))

    def test_predictions(self):
        # features = self.extract_features(self.augment_features(self.train_data))
        model = GaussianHMM(n_components=10)
        feature_train_data = self.augment_features(self.train_data)
        features_train = self.extract_features(feature_train_data)
        model.fit(features_train)

        # Generating possible sequences
        test_augmented = self.augment_features(self.test_data)
        fracocp = test_augmented['delOpenClose'] # The fractional change in opening and closing prices
        frachp = test_augmented['delHighOpen'] # The fractional change in high prices
        fraclp = test_augmented['delLowOpen'] # The fractional change in low prices

        sample_space_fracocp = np.linspace(fracocp.min(), fracocp.max(), 50)
        sample_space_fraclp = np.linspace(fraclp.min(), frachp.max(), 10)
        sample_space_frachp = np.linspace(frachp.min(), frachp.max(), 10)

        possible_outcomes = np.array(list(itertools.product(sample_space_fracocp, sample_space_frachp, sample_space_fraclp)))

        # Checking predictions
        num_latent_days = 20 # the data of the last [num_latent_days] to predict the closing price of the current day
        self.num_days_to_predict = len(self.test_data) # repeat those for [num_days_to_predict] days

        predicted_close_prices = []
        for i in tqdm(range(self.num_days_to_predict)): 
            # Calculate start and end indices
            previous_data_start_index = max(0, i - num_latent_days)
            previous_data_end_index = max(0, i)
            # Acquire test data features for these days
            previous_data = self.extract_features(self.augment_features(self.test_data.iloc[previous_data_start_index:previous_data_end_index]))
            
            outcome_scores = []
            for outcome in possible_outcomes:
                # Append each outcome one by one with replacement to see which sequence generates the highest score
                total_data = np.row_stack((previous_data, outcome))
                outcome_scores.append(model.score(total_data))
                
            # Take the most probable outcome as the one with the highest score
            most_probable_outcome = possible_outcomes[np.argmax(outcome_scores)]
            # print(i, self.test_data.iloc[i])
            predicted_close_prices.append(self.test_data.iloc[i]['Open'] * (1 + most_probable_outcome[0]))
        
        return predicted_close_prices
    
    def forecast(self):
        pass 

    def visualize_hmm(self, predicted_close_prices):
        # if interval in ['1m', '2m', '5m', '15m', '30m', '60m', '90m']:
        fig = go.Figure(data=[go.Scatter(
                x = np.array(range(self.train_size)),
                y = self.train_data['Close'],
                name = 'Train',
                mode='lines',
                line=dict(color="Blue")
            ),
            go.Scatter(
                x = np.array(range(self.train_size, len(self.data))),
                y = self.test_data['Close'],
                name = 'Test',
                mode = "lines",
                line=dict(color="orange")
            ),
            go.Scatter(
                x = np.array(range(self.train_size, len(self.data))),
                y = predicted_close_prices,
                name = 'Test Predictions',
                mode='lines',
                line=dict(color="Green")
            ),
            # go.Scatter(
            #     x=np.array(range(len(self.data), predict_days)),
            #     y=predicted_close_prices,
            #     name="Forecast",
            #     mode="lines",
            #     line=dict(color="red"),
            # ),
        ])   
        fig.update_layout(
            title='Hidden Markov Model',
            yaxis_title='Price (KRW)',
            xaxis_title='Datetime',
            xaxis_rangeslider_visible=False,
            xaxis_type='category'
        )
        return fig 