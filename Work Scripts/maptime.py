import time

# Sample data (country, sunrise, sunset)
country_data = {
    "USA": ("06:00", "18:00"),
    "Japan": ("05:30", "19:30"),
    # Add more countries and their times
}

def is_daytime(sunrise, sunset):
    current_time = time.strftime("%H:%M")
    return sunrise <= current_time <= sunset

def display_map():
    for country, (sunrise, sunset) in country_data.items():
        if is_daytime(sunrise, sunset):
            print(f"{country}: ☀️  (Daytime)")
        else:
            print(f"{country}: 🌙  (Nighttime)")

if __name__ == "__main__":
    while True:
        display_map()
        time.sleep(10)  # Update every 10 seconds (adjust as needed)
