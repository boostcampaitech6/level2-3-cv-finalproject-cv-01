# Model Training 
CNN 모델 학습을 위한 코드입니다.

## How to train CNN
1. yfinance를 사용한 stock_csv 생성
    ```
    python data_generate/get_stock_data.py
    ``` 
2. (Optional) pickle data 생성
    ```
    python data_generate/csv_to_pickle.py
    ``` 
3. config.json에서 csv_dir, pickle_dir 경로 및 하이퍼파라미터 지정  
4. python train.py -c config.json