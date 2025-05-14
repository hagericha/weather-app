import requests

API_KEY = " "  #Add openweathermap api here
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_current_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        weather = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"]
        }
        return weather
    else:
        return {"error": "City not found or API issue."}

# For testing:
if __name__ == "__main__":
    city = input("Enter city name: ")
    result = get_current_weather(city)
    print(result)
