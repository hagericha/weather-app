import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import webbrowser

from weather_backend import get_current_weather, get_forecast, get_weather_news

# --- Global Setup ---
root = tk.Tk()
root.title("Weather Forecasting App")
root.configure(bg="#e6f7ff")  # App background

# 🔹 Top Frame to hold Entry and Button
top_frame = tk.Frame(root, bg="#e6f7ff")
top_frame.pack(pady=(10, 5))

city_label = tk.Label(top_frame, text="Enter City,CountryCode (e.g., Mumbai,IN)", font=("Arial", 10), bg="#e6f7ff", fg="black")
city_label.pack(side="top", pady=(0, 2))

city_entry = tk.Entry(top_frame, width=40, font=("Arial", 12))
city_entry.pack(side="top", pady=(0, 5))

# Create a master canvas (scrollable)
canvas = tk.Canvas(root, bg="#e6f7ff", highlightthickness=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)

scrollable_frame = tk.Frame(canvas, bg="#e6f7ff")

# Add scrollable frame inside canvas
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Enable mousewheel scrolling
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)


# --- UI Frames ---
current_frame = tk.Frame(scrollable_frame, bd=2, relief="groove", padx=10, pady=10, bg="#e6f2ff")

hourly_frame = tk.Frame(scrollable_frame, bg="white")
#hourly_frame.pack(padx=10, pady=5, anchor="center")

news_frame = tk.Frame(scrollable_frame, bg="white")
#news_frame.pack(padx=10, pady=10, anchor="center")

# --- Widgets ---
temp_label = tk.Label(current_frame, text="", font=("Arial", 32), bg="#e6f2ff")
temp_label.pack()

icon_label = tk.Label(current_frame, bg="#e6f2ff")
icon_label.pack(pady=5)

condition_label = tk.Label(current_frame, text="", font=("Arial", 16), bg="#e6f2ff")
condition_label.pack()


# --- Utility Functions ---
def open_url(url):
    webbrowser.open_new(url)

# --- Display Functions ---
def display_current_weather(current):

    temp_label.config(text=f"{current['temp']}\u00b0C")
    condition_label.config(text=current['condition'])

    icon_code = current.get("icon", "01d")
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
    try:
        response = requests.get(icon_url)
        image_data = response.content
        img = Image.open(BytesIO(image_data))
        photo = ImageTk.PhotoImage(img)
        icon_label.config(image=photo)
        icon_label.image = photo
    except:
        icon_label.config(image="", text="🌤")

def display_hourly_forecast(forecast):
    for widget in hourly_frame.winfo_children():
        widget.destroy()

    for day_index, (day, entries) in enumerate(forecast.items()):
        if day_index >= 5:
            break

        tk.Label(hourly_frame, text=f"📅 {day}", font=("Arial", 12, "bold"), bg="white").pack(anchor="w", pady=(10, 0))
        row_frame = tk.Frame(hourly_frame, bg="white")
        row_frame.pack(fill="x", pady=5)

        for time_str, temp, desc, icon_code in entries:
            card = tk.Frame(row_frame, bg="#f0f0f0", padx=8, pady=5)
            card.pack(side="left", padx=5)
            tk.Label(card, text=time_str, font=("Arial", 10, "bold"), bg="#f0f0f0").pack()
            tk.Label(card, text=f"{temp}\u00b0C", font=("Arial", 10), bg="#f0f0f0").pack()
            try:
                icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                response = requests.get(icon_url)
                img_data = response.content
                img = Image.open(BytesIO(img_data))
                photo = ImageTk.PhotoImage(img)
                label = tk.Label(card, image=photo, bg="#f0f0f0")
                label.image = photo
                label.pack()
            except:
                tk.Label(card, text="🌡️", bg="#f0f0f0").pack()

def display_news(city_only):
    for widget in news_frame.winfo_children():
        widget.destroy()

    tk.Label(news_frame, text="🗞️ Weather-Related News Headlines", font=("Arial", 14, "bold"), bg="white").pack(anchor="w", pady=(0, 5))
    news_sections = get_weather_news(city_only)

    for section_title, articles in news_sections:
        tk.Label(news_frame, text=section_title, font=("Arial", 12, "bold"), bg="white", fg="#003366").pack(anchor="w", pady=(10, 0))

        for i, article in enumerate(articles, 1):
            title = article['title']
            source = article.get('source', '')
            url = article.get('url', '')

            tk.Label(news_frame, text=f"{i}. {title}", wraplength=600, justify="left", bg="white", font=("Arial", 10)).pack(anchor="w")
            if source:
                tk.Label(news_frame, text=f"   📰 {source}", bg="white", font=("Arial", 9, "italic"), fg="gray").pack(anchor="w")
            if url:
                link = tk.Label(news_frame, text=f"   🔗 {url}", fg="blue", bg="white", cursor="hand2", font=("Arial", 9, "underline"))
                link.pack(anchor="w")
                link.bind("<Button-1>", lambda e, url=url: open_url(url))

# --- Main Controller Function ---
def show_weather():
    city_input = city_entry.get().strip()
    if not city_input:
        messagebox.showwarning("Input Error", "Please enter city and country code.")
        return

    current = get_current_weather(city_input)
    if "error" in current:
        messagebox.showerror("Error", current["error"])
        return

    forecast = get_forecast(city_input)
    city_only = city_input.split(",")[0]

    # Repack in correct order
    current_frame.pack_forget()
    hourly_frame.pack_forget()
    news_frame.pack_forget()

    current_frame.pack(padx=10, pady=10, anchor="center")
    hourly_frame.pack(padx=10, pady=5, anchor="center")
    news_frame.pack(padx=10, pady=10, anchor="center")

    display_current_weather(current)
    display_hourly_forecast(forecast)
    display_news(city_only)

    # Fix scrolling range after content is added
    scrollable_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

get_weather_btn = tk.Button(top_frame, text="Get Weather", command=show_weather)
get_weather_btn.pack()


# --- Run App ---
root.mainloop()

