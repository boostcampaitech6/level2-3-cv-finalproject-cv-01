import os
import os.path as osp
import pandas as pd
import numpy as np
from tqdm import tqdm

def rasterize(csv_path, window_size):

    data = []

    for file_name in tqdm(os.listdir(csv_path), desc= f"Creating a pickle file for the window_size size_{window_size}"):
        file_path = osp.join(csv_path, file_name)
        df = pd.read_csv(file_path)
        
        for target_day in range(1,31):
            df[f'ret{target_day}'] = (df['Close'].pct_change(target_day)*100).shift(-target_day)

        df[f'MA'] = df['Close'].rolling(window_size).mean()
        
        df.dropna(inplace=True)
        
        for d in range(0, len(df)-window_size):
            
            price_slice = df[d:d+window_size][['Open', 'High', 'Low', 'Close']+['MA']].reset_index(drop=True)
            volume_slice = df[d:d+window_size][['Volume']].reset_index(drop=True)

            price_slice = (price_slice - np.min(price_slice.values))/(np.max(price_slice.values) - np.min(price_slice.values))
            price_slice[np.isnan(price_slice)] = 0.5

            volume_slice = (volume_slice - np.min(volume_slice.values))/(np.max(volume_slice.values) - np.min(volume_slice.values))
            volume_slice[np.isnan(volume_slice)] = 0
            
            price_slice = price_slice.apply(lambda x: x*(51-1)+13).astype(int)
            volume_slice = volume_slice.apply(lambda x: x*(12-1)).astype(int)
        
            image = np.zeros((64, window_size*3))
            for i in range(len(price_slice)):
                # 캔들 그래프
                image[price_slice.loc[i]['Open'], i*3] = 255.
                image[price_slice.loc[i]['Low']:price_slice.loc[i]['High']+1, i*3+1] = 255.
                image[price_slice.loc[i]['Close'], i*3+2] = 255.
                # 이동 평균선
                image[price_slice.loc[i]['MA'], i*3:i*3+2] = 255.
                # 거래량
                image[:volume_slice.loc[i]['Volume'], i*3+1] = 255.

            image = np.flipud(image).copy()
            
            ret_dict = {}
            for i in range(1,31):
                ret_dict[f'ret{i}'] = df.iloc[d+window_size-1][f'ret{i}']

            data.append([image, ret_dict])

    return data
    

    
    