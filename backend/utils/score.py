import math
import numpy as np
import pandas as pd

default_score = 50

# LSTM, AR, HMM
def TimeSeriesScore(recent_price, predict_price):
    score = (predict_price - recent_price) / recent_price * 100
    
    final_score = default_score + score * 5
    final_score = max(0, min(100, final_score))
    
    return final_score
    
# CNN
# 기본 점수 + 상승(+)/하락(-) * 예측 Confidence 0 = 하락 1 = 상승
def CNNScore(pred_result, pred_percent):
    score = 0
    if pred_result == 0:
        score = -1 * pred_percent
    elif pred_result == 1:
        score = 1 * pred_percent
        
    final_score = default_score + score * 10
    final_score = max(0, min(100, final_score))

    return final_score

# 최종 점수 = 금일 점수 + 익일 점수
# 최종 점수 = 0.7 * ( 긍정 * 1.0 + 중립 * 0.5 + 부정 * -1.0 ) + 0.3 * ( 긍정 * 1.0 + 중립 * 0.5 + 부정 * -1.0)
# BERT
def BERTScore(yesterday_positive, yesterday_neutral, yesterday_negative,
                today_positive, today_neutral, today_negative):
    score = 0.7 * ( today_positive * 1.0 + today_neutral * 0.5 + today_negative * -1.0 ) + \
            0.3 * ( yesterday_positive * 1.0 + yesterday_neutral * 0.5 + yesterday_negative * -1.0)
    
    final_score = default_score + score
    final_score = max(0, min(100, final_score))
    
    return final_score


# CANDLE
# 최종 점수 = 기본 점수 + (상승 - 하락) / (상승 + 하락) * 50 * 가중치
def CANDLEScore(candle_name):
    df = pd.read_csv('/backend/utils/candle_patterns_db.csv')

    pattern_list = candle_name.split(',')

    highest_rank = float('inf')
    highest_rank_code = None
    pattern_info = None
    
    for pattern in pattern_list:
        filtered_df = df[df['code'].str.strip() == pattern.strip()]

        if not filtered_df.empty:
                current_highest_rank_row = filtered_df.loc[filtered_df['rank'].idxmin()]
                
                # 현재 패턴의 가장 높은 rank와 해당 code를 확인
                current_highest_rank = current_highest_rank_row['rank']
                current_code = current_highest_rank_row['code']
                
                # 현재 패턴의 가장 높은 rank가 이전에 찾은 rank보다 높은 경우 업데이트
                if current_highest_rank < highest_rank:
                    highest_rank = current_highest_rank
                    highest_rank_code = current_code
                    pattern_info = current_highest_rank_row  # 패턴 정보 저장
                    
    # scoring
    up = pattern_info['up']
    down = pattern_info['down']
    efficiency_rank = pattern_info['efficiency_rank']
    
    efficiency_weight = {
                            'a+': 1.2, 'a': 1.18, 'a-': 1.16,
                            'b+': 1.14, 'b': 1.12, 'b-': 1.1,
                            'c+': 1.08, 'c': 1.06, 'c-': 1.04,
                            'd+': 1.02, 'd': 1.0, 'd-': 0.98,
                            'e+': 0.96, 'e': 0.94, 'e-': 0.92,
                            'f+': 0.9, 'f': 0.88, 'f-': 0.86,
                            'g+': 0.84, 'g': 0.82, 'g-': 0.8,
                            'h+': 0.78, 'h': 0.76, 'h-': 0.74,
                            'i+': 0.72, 'i': 0.7, 'i-': 0.68,
                            'j+': 0.66, 'j': 0.64, 'j-': 0.62
                        }
    
    base_score = 50 + ((up - down) / (up + down)) * 50
    # efficiency_rank에 대한 가중치 적용
    efficiency_multiplier = efficiency_weight.get(efficiency_rank.strip().lower(), 1)
    final_score = base_score * efficiency_multiplier
    
    final_score = max(0, min(100, final_score))
    
    return final_score