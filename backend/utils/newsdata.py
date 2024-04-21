from fastapi import FastAPI
import httpx
import html

# 네이버 Open API 인증 정보
client_id = "FKGfUdfRecj0FNIlQW33"
client_secret = "1qSarNIp0m"
naver_url = "https://openapi.naver.com/v1/search/news.json"


async def fetch_news_data(query: str):
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    params = {"query": query}
    async with httpx.AsyncClient() as client:
        response = await client.get(naver_url, headers=headers, params=params)

    if response.status_code == 200:
        response_data = response.json()
        news_data = []

        for item in response_data['items']:
            title = html.unescape(html.unescape(item['title']))
            link = item['link']
            pub_date = item['pubDate']
            source = item['originallink']
            description = html.unescape(html.unescape(item['description']))

            news_item = {
                'title': title,
                'link': link,
                'pubDate': pub_date,
                'source': source,
                'description': description,
            }

            news_data.append(news_item)

        return news_data[:3]
    else:
        return []