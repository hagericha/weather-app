# backend.py
import requests
from datetime import datetime
from collections import defaultdict

API_KEY = "your_openweathermap_api_key"
CURRENT_URL = "current_weather_url"
FORECAST_URL = "hourly_forecast_url"

def get_current_weather(city):
    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
    response = requests.get(CURRENT_URL, params=params)
    data = response.json()

    if response.status_code == 200:
        return {
            "city": data['name'],
            "country": data['sys']['country'],
            "temp": data['main']['temp'],
            "condition": data['weather'][0]['description'].title(),
            "icon": data['weather'][0]['icon'] 
        }
    elif response.status_code == 404:
        return None  # City not found
    else:
        raise requests.exceptions.HTTPError("API error while fetching current weather.")

def get_forecast(city):
    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
    response = requests.get(FORECAST_URL, params=params)
    data = response.json()

    if response.status_code != 200:
        raise requests.exceptions.RequestException("Error fetching forecast data.")

    forecasts = data['list']
    grouped = defaultdict(list)

    for entry in forecasts:
        dt_txt = entry['dt_txt']
        dt = datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S")

        date_str = dt.strftime("%A, %B %d")
        time_str = dt.strftime("%H:%M")

        temp = entry['main']['temp']
        desc = entry['weather'][0]['description']
        icon = entry['weather'][0]['icon'] 
        grouped[date_str].append((time_str, temp, desc, icon))

    return grouped


def get_weather_news(city_name):
    NEWS_API_KEY = "your_newsapi_key"
    base_url = "news_url" 

    sections = [
        ("🌆 Local News", f"weather {city_name}"),
        ("🇮🇳 National News", "weather india"),
        ("🌍 Global News", "weather")
    ]

    news_result = []

    for title, query in sections:
        params = {
            'q': query,
            'language': 'en',
            'sortBy': 'publishedAt',
            'pageSize': 3,
            'apiKey': NEWS_API_KEY
        }

        try:
            response = requests.get(base_url, params=params)
            data = response.json()

            articles = []
            if data["status"] == "ok" and data["totalResults"] > 0:
                for article in data["articles"]:
                    articles.append({
                        "title": article["title"],
                        "source": article["source"]["name"],
                        "url": article["url"]
                    })
            else:
                articles.append({"title": "No articles found.", "source": "", "url": ""})

            news_result.append((title, articles))
        except Exception as e:
            news_result.append((title, [{"title": f"Error: {e}", "source": "", "url": ""}]))

    return news_result