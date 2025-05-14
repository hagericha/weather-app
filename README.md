# Weather Forecast App

A clean and responsive desktop weather application built with **Python** and **Tkinter** that allows users to search for any city and get real-time weather data including temperature, weather description, and the national flag of the location.

## Features

- Search weather by **city name**
- Displays:
  - **Temperature** (in Celsius)
  - **Weather condition** (with icon)
  - **City & Country**
  - **National flag** of the country
- Dynamic content loading – the result section appears only after a successful search
- Simple and modern UI with centered layout
- Error handling for invalid city names or connection issues

## Technologies Used

- **Python** (Tkinter for GUI)
- **OpenWeatherMap API** – for real-time weather data
- **FlagsAPI** – to fetch national flags
- **Pillow (PIL)** – for image handling (weather icons and flags)
- **Requests** – for API communication

## Installation

1. Clone the Repository
  ```
  git clone https://github.com/hagericha/Ecommerce-website
  ```

2. Create and Activate a Virtual Environment
  ```
  python -m venv env
  ```

  ```
  #Activate virtual environment
  env\Scripts\activate
  ```

3. Run the Flask App
  ```
  python main.py
  ```
