from torch.utils.data import Dataset
from tqdm import tqdm
import os
import os.path as osp
import pickle
import torch
import importlib


class StockDataset(Dataset):
    def __init__(self, window_size: int, target_day: int, \
                transform_type: str= None, pickle_dir: str = None, csv_dir: str = None):

        self.window_size = window_size
        self.target_day = target_day
        self.transform_type = transform_type

        assert transform_type != None, "이미지 변환 타입을 지정해야함"
        assert pickle != None or csv_dir != None, "둘중에 하나는 있어야 한다."


        if pickle_dir != None and f'window_{self.window_size}.pkl' in os.listdir(osp.join(pickle_dir,f'{self.transform_type}_pkl')):
            # 피클 파일 사용가능
            with tqdm(total=100, desc="Pickle File Loading", unit="%", position=0) as pbar:
                with open(osp.join(pickle_dir,f'{transform_type}_pkl', f'window_{self.window_size}.pkl'), 'rb') as file:
                    temp_data = pickle.load(file)
                    pbar.update(100)  
        else:
            # 피클파일 없이 수행
            module_path = 'data_generate.transform_func.'+ transform_type
            module = importlib.import_module(module_path)
            generate_image = getattr(module, transform_type)
            print(csv_dir, self.window_size)
            temp_data = generate_image(csv_dir, self.window_size)


        self.data = []
        for img, dic in temp_data:
            self.data.append([img,dic[f"ret{self.target_day}"]])


    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        image = self.data[idx][0]
        image = torch.from_numpy(image)
        label = 1 if self.data[idx][1] >= 0 else 0

        return image, label


    
                

        
    
