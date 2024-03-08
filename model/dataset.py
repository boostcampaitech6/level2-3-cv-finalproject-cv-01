import numpy as np
from torch.utils.data import Dataset
from tqdm import tqdm
import os.path as osp
import pickle

import importlib


class StockDataset(Dataset):
    def __init__(self, window_size: int, target_day: int,  \
                 use_pickle:bool, pickle_dir: str, 
                 transform_type: str= None, csv_path: str = None):

        self.window_size = window_size
        self.target_day = target_day

        if use_pickle:
            with tqdm(total=100, desc="Pickle File Loading", unit="%", position=0) as pbar:
                with open(osp.join(pickle_dir, f'window_{self.window_size}.pkl'), 'rb') as file:
                    temp_data = pickle.load(file)
                    pbar.update(100)  
            
        else:
            module_path = 'utils.'+ transform_type
            module = importlib.import_module(module_path)
            transform_to_image = getattr(module, transform_type)

            temp_data = transform_to_image(csv_path, self.window_size)

        self.data = []
        for img, dic in temp_data:
            self.data.append([img,dic[f"ret{self.target_day}"]])


    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        image = self.data[idx][0]
        label = 1 if self.data[idx][1] >= 0 else 0
        return image, label