from .rasterize import rasterize
from .cnn_model import get_cnn_model
import torch



def inference(stock_image):
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    stock_image = stock_image.to(device)

    pred_list = []
    for pred_day in range(1,8):
        model = get_cnn_model(pred_day).to(device)
        output = model(stock_image)[0]
        
        idx = torch.argmax(output).item()
        pct = output[idx].item()

        pred_list.append([idx,pct])

    return pred_list
