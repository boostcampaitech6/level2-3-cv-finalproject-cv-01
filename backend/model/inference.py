import numpy as np
import torch


def rasterize(data_frame, source_term):
    if source_term == 5:
        image_size = (32, 15)
    elif source_term == 20:
        image_size = (64, 60)

    price_slice = data_frame.iloc[-source_term:][['Open', 'High', 'Low', 'Close']].reset_index(drop=True)

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


def inference(model, data, source_term):

    rasterized_img = rasterize(data, source_term)
    
    input = preprocess(rasterized_img)
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    input = input.to(device)
    
    with torch.no_grad():
        output = model(input)[0]
    
    pred_idx = torch.argmax(output).item()
    return {"pred_idx" : pred_idx, "percentage" : output[pred_idx].item()}