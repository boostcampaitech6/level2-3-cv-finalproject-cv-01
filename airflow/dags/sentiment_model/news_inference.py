import urllib.request
import json
import re
import html
import pandas as pd
from transformers import BertTokenizer, TFBertForSequenceClassification
import tensorflow as tf
import numpy as np
import tensorflow_addons as tfa
from datetime import timedelta

def get_news_df(query: str, symbol: str, client_id: str, client_secret: str, display: int = 10):

    encText = urllib.parse.quote(symbol)
    url = f"https://openapi.naver.com/v1/search/news?query={encText}&display={display}"

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)

    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    news_data = []
    
    if(rescode == 200):
        response_body = response.read()
        response_data = json.loads(response_body.decode('utf-8'))
        
        for item in response_data['items']:
            title = html.unescape(re.sub('<.*?>', '', item['title']))
            description = html.unescape(re.sub('<.*?>', '', item['description']))

            news_item = {
                'code': symbol,
                'name': query,  # 쿼리 추가
                'pubDate': item['pubDate'],
                'source': item['link'].split('/')[2].split('.')[1],
                'title': title,
                'link': item['link'],
                'description': description,
            }
            
            news_data.append(news_item)

        return news_data
        
    else:
        print("Error Code:", rescode)
        return []
    

def classify_news(descriptions, batch_size=1024):
    MODEL_NAME = "klue/bert-base"
    tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
    MODEL_PATH = "./dags/sentiment_model/sentiment_model.h5"

    model = tf.keras.models.load_model(
        MODEL_PATH,
        custom_objects={
            'TFBertForSequenceClassification': TFBertForSequenceClassification,
            'RectifiedAdam': tfa.optimizers.RectifiedAdam
        }
    )


    all_sentiments = []  # 모든 감정을 저장할 리스트

    for i in range(0, len(descriptions), batch_size):
        batch = descriptions[i:i+batch_size]
        inputs = tokenizer(batch, return_tensors="tf", max_length=64, padding='max_length', truncation=True)
        model_inputs = {
        'input_word_ids': inputs['input_ids'], 
        'input_masks': inputs['attention_mask'],
        'input_segment': inputs.get('token_type_ids', tf.zeros_like(inputs['input_ids'])) 
    }
        predicted_values = model.predict(model_inputs, verbose=0)  # verbose 옵션 추가
        # predicted_value = model.predict(model_inputs, verbose=0)  # verbose 옵션 추가
        predicted_classes = np.argmax(predicted_values, axis=1)
        class_names = ['neutral', 'positive', 'negative']
        sentiments = [class_names[predicted_class] for predicted_class in predicted_classes]
        all_sentiments.extend(sentiments)

    return all_sentiments


def get_sentiment_score(data, query):
    query_data = data[data['name'] == query]

    
    latest_date = pd.to_datetime(query_data['pubDate']).max().date()
    previous_date = latest_date - timedelta(days=1)


    latest_sentiments = query_data[pd.to_datetime(query_data['pubDate']).dt.date == latest_date]['sentiment'].value_counts().reindex(['positive', 'neutral', 'negative'],       fill_value=0)
    previous_sentiments = query_data[pd.to_datetime(query_data['pubDate']).dt.date == previous_date]['sentiment'].value_counts().reindex(['positive', 'neutral', 'negative'], fill_value=0)

    detailed_result = {
        'Date': [latest_date, previous_date],
        'Positive': [latest_sentiments.get('positive', 0), previous_sentiments.get('positive', 0)],
        'Neutral': [latest_sentiments.get('neutral', 0), previous_sentiments.get('neutral', 0)],
        'Negative': [latest_sentiments.get('negative', 0), previous_sentiments.get('negative', 0)],
    }

    return detailed_result