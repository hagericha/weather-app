import tkinter as tk
from tkinter import messagebox
from weather_api import get_current_weather

from PIL import Image, ImageTk
import requests
from io import BytesIO

# --- Root Window Setup ---
root = tk.Tk()
root.title("Weather Forecast App")
root.configure(bg="#e0f7fa")  

# --- Center window on screen ---
window_width = 900
window_height = 500

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_pos = int((screen_width / 2) - (window_width / 2))
y_pos = int((screen_height / 2) - (window_height / 2))

root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

# --- App Title (Outside Main Frame) ---
title_label = tk.Label(root, text="Weather Forecast", 
                       font=("Helvetica", 24, "bold"), 
                       fg="#0d47a1", bg="#e0f7fa")
title_label.pack(pady=(30, 10)) 

# --- Search Section ---
search_frame = tk.Frame(root, bg="#e0f7fa")
search_frame.pack(pady=(10, 30))  

search_label = tk.Label(search_frame, text="Enter city :", 
                        font=("Helvetica", 14), bg="#e0f7fa", fg="#333")
search_label.pack(side=tk.LEFT, padx=(0, 10))

search_entry = tk.Entry(search_frame, font=("Helvetica", 14), width=30)
search_entry.pack(side=tk.LEFT, padx=(0, 10))

# --- Define the search_weather function here ---
def search_weather():
    city = search_entry.get()
    if not city:
        return

    api_key = " "  # <-- Replace this with your actual API key
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            location_label.config(text="City not found", fg="red")
            temp_label.config(text="")
            desc_label.config(text="")
            flag_label.config(image="")
            icon_label.config(image="")
            return

        # --- Extract Data ---
        country_code = data["sys"]["country"]
        city_name = data["name"]
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"].title()
        icon_code = data["weather"][0]["icon"]

        # --- Update Location and Temp ---
        location_label.config(text=f"{city_name}, {country_code}", fg="black")
        temp_label.config(text=f"{temperature} °C")
        desc_label.config(text=description)

        # Show main_frame only after valid search
        global main_frame_visible
        if not main_frame_visible:
            main_frame.pack(pady=(0, 30))  # Show it 2-3 cm below search bar
            main_frame_visible = True

        # --- Load Weather Icon ---
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_img = Image.open(BytesIO(requests.get(icon_url).content))
        icon_img = ImageTk.PhotoImage(icon_img)
        icon_label.config(image=icon_img)
        icon_label.image = icon_img

        # --- Load Country Flag ---
        flag_url = f"https://flagsapi.com/{country_code}/flat/64.png"
        flag_img = Image.open(BytesIO(requests.get(flag_url).content))
        flag_img = ImageTk.PhotoImage(flag_img)
        flag_label.config(image=flag_img)
        flag_label.image = flag_img

    except Exception as e:
        location_label.config(text="Error fetching data", fg="red")
        print("Error:", e)

# --- Search Button Code ---
search_button = tk.Button(search_frame, text="Search", 
                          font=("Helvetica", 12), bg="#0d47a1", fg="white",
                          padx=10, pady=2, command=search_weather)

search_button.pack(side=tk.LEFT)

# --- Frame for Content ---
main_frame = tk.Frame(root, bg="#ffffff", padx=20, pady=20, bd=2, relief=tk.GROOVE)
main_frame.pack_forget()
main_frame_visible = False 

# --- Result Components inside main_frame ---
# Flag
flag_label = tk.Label(main_frame, bg="white")
flag_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

# City and Country
location_label = tk.Label(main_frame, text="", font=("Helvetica", 16, "bold"), bg="white")
location_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))

# Temperature
temp_label = tk.Label(main_frame, text="", font=("Helvetica", 20), bg="white")
temp_label.grid(row=2, column=0, columnspan=2, pady=(0, 10))

# Weather description
desc_label = tk.Label(main_frame, text="", font=("Helvetica", 14), bg="white")
desc_label.grid(row=3, column=0, columnspan=2, pady=(0, 10))

# Weather Icon
icon_label = tk.Label(main_frame, bg="white")
icon_label.grid(row=4, column=0, columnspan=2)

# --- Run App ---
root.mainloop()
