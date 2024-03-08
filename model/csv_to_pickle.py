import os
import argparse
import pickle
import importlib

# from utils.rasterize import rasterize

def csv_to_pickle(csv_path,save_dir, windows, transform_type):
    module_path = 'utils.'+ transform_type
    module = importlib.import_module(module_path)
    transform = getattr(module, transform_type)

    for window in windows:
        data = transform(csv_path,window)
    
        os.makedirs(save_dir, exist_ok=True)
        with open(f'{save_dir}/window_{window}.pkl', 'wb') as pickle_file:
            pickle.dump(data, pickle_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--transform_type", default='rasterize', type=str, help="Type of Image to Convert")
    parser.add_argument("--window_size", default=-1, type=int, help="Window Size") # 변환할 이미지 윈도우 크기 (-1 입력시 5부터 30까지 피클 생성)
    parser.add_argument("--csv_path", default= './stock_csv', type=str, help="Csv Directory Path")
    parser.add_argument("--save_dir", default='./rasterize_pkl', type=str, help="Save Directory Path")

    args = parser.parse_args()

    assert 5 <= args.window_size <= 30 or args.window_size==-1, "Error: window size should be between 5 and 30."

    window = range(5,31) if args.window_size == -1 else [args.window_size]

    csv_to_pickle(args.csv_path,args.transform_type+'_pkl', window, args.transform_type)