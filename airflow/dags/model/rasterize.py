import FinanceDataReader as fdr
import numpy as np
import torch

def rasterize(stock_code, date):
    window_size = 20

    # OHLC Rasterize
    df = fdr.DataReader(stock_code, None, date)[-39:]
    df[f'MA'] = df['Close'].rolling(window_size).mean()
    df.dropna(inplace=True)

    price_slice = df[:][['Open', 'High', 'Low', 'Close']+['MA']].reset_index(drop=True)
    volume_slice = df[:][['Volume']].reset_index(drop=True)

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

    # image = np.flipud(image).copy()
    image = torch.Tensor(np.array(image))
    image = image.unsqueeze(0)
    return image