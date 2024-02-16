# pages/home.py
import requests
from bs4 import BeautifulSoup
import streamlit as st
from datetime import datetime
import pytz
def app():
    st.title('Dashboard')
    st.write('Welcome to the Dashboard!')




    def get_news():
        headers = {
            # 나중에 User-Agent를 바꿔야 할 수도 있음
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get('https://finviz.com/news.ashx', headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        tables = soup.find('table', {'class': 'news_time-table'})

        news_items = []

        for row in tables.find_all('tr')[2:]:

            link_tag = row.find('a')
            time_tag = row.find('td', {'class': 'text-right'})
            headline_time = time_tag.text.strip()
            headline_text = link_tag.text.strip()
            headline_link = link_tag['href'].strip()
            news_items.append((headline_time, headline_text, headline_link))

        original_news_items = news_items

        return original_news_items[:10]


    def convert_time_to_local(time_str, from_tz, to_tz):
        from_zone = pytz.timezone(from_tz)
        to_zone = pytz.timezone(to_tz)
        local_time = datetime.strptime(time_str, '%I:%M%p').replace(tzinfo=from_zone).astimezone(to_zone)
        return local_time.strftime('%I:%M %p')



    news_items = get_news()

    st.title('News')

    st.markdown("""
        <style>
        .news-item {
            display: flex;
            justify-content: start;
            align-items: center;
            padding: 2px;
            margin: 2px 0;
            border-radius: 2px;
            transition: background-color 0.3s;
        }
        .news-item:hover {
            background-color: #bbbfc4;
        }
        .news-time {
            font-weight: bold;
            color: #0078ff;
            margin-right: 15px;
            white-space: nowrap;
        }
        .news-headline {
            color: black;
            text-decoration: none;
            font-size: 18px;
        }
        </style>
    """, unsafe_allow_html=True)

    for time, headline, link in news_items:

        st.markdown(f"""
            <a href="{link}" target="_blank" style="text-decoration: none;">
                <div class="news-item" style="border-left: 3px solid #0078ff; padding: 3px; margin: 2px 0; border-radius: 2px; transition: background-color 0.3s;">
                    <span style="font-size: 18px; color: #0078ff;">{time}</span>
                    <span style="margin-left: 10px; font-size: 18px; color: #000;">{headline}</span>
                </div>
            </a>
        """, unsafe_allow_html=True)
