import tkinter as tk
from datetime import datetime, timedelta
import requests

API_KEY = "1f14fe829730415b8ed33c4a64e52847"
NEWS_API_URL = "https://newsapi.org/v2/everything"

def get_top_geopolitics_news(api_key, from_date, to_date, page_size=10):
    query = "geopolitics"

    params = {
        "apiKey": api_key,
        "pageSize": page_size,
        "from": from_date,
        "to": to_date,
        "q": query,
        "language": "en"
    }
    response = requests.get(NEWS_API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        return articles
    else:
        print("Error fetching news:", response.status_code)
        print("Error message:", response.json().get("message", "Unknown error"))
        return None

def display_articles():
    to_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    # Define the variable here so it's accessible within this function
    geopolitics_articles = get_top_geopolitics_news(API_KEY, from_date, to_date)

    if geopolitics_articles:
        canvas.delete("all")  # Clear previous content if any
        for index, article in enumerate(geopolitics_articles[:10], start=1):
            article_frame = tk.Frame(canvas, relief=tk.GROOVE, borderwidth=2, padx=10, pady=10, bg="white")
            canvas.create_window((10, index * 150), window=article_frame, anchor='w')

            title_label = tk.Label(article_frame, text=f"News {index}: {article.get('title')}", font=("Arial", 12, "bold"), bg="white")
            title_label.pack(anchor="w", pady=(0, 5))

            source_label = tk.Label(article_frame, text=f"Source: {article.get('source', {}).get('name')}", bg="white")
            source_label.pack(anchor="w", pady=(0, 5))

            description_label = tk.Label(article_frame, text=f"Description: {article.get('description')}", bg="white")
            description_label.pack(anchor="w", pady=(0, 5))

            url_label = tk.Label(article_frame, text=f"URL: {article.get('url')}", fg="blue", cursor="hand2", bg="white")
            url_label.pack(anchor="w", pady=(0, 5))
            url_label.bind("<Button-1>", lambda e, url=article.get('url'): open_url(url))

            published_at_label = tk.Label(article_frame, text=f"Published At: {article.get('publishedAt')}", bg="white")
            published_at_label.pack(anchor="w", pady=(0, 5))

        # Update the canvas scroll region to match the new content
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
    else:
        no_articles_label = tk.Label(canvas, text="No geopolitics news articles found.", bg="white")
        canvas.create_window((10, 10), window=no_articles_label, anchor='w')

def open_url(url):
    import webbrowser
    webbrowser.open_new(url)

# Function to handle mouse wheel scrolling
def on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

window = tk.Tk()
window.title("Geopolitics News Viewer")
window.geometry("800x600")
window.configure(bg="lightblue")

# Create a canvas with a vertical scrollbar
canvas = tk.Canvas(window)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(window, command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Bind mouse wheel event to scroll the canvas
canvas.bind_all("<MouseWheel>", on_mousewheel)

display_articles_button = tk.Button(canvas, text="Display Geopolitics Articles", command=display_articles, bg="blue", fg="white", font=("Arial", 12))
canvas.create_window((10, 10), window=display_articles_button, anchor='nw')

window.mainloop()
