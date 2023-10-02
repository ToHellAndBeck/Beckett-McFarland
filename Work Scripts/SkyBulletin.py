import sys
import requests
from datetime import datetime
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit
from PyQt5.QtGui import QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
from matplotlib.ticker import MaxNLocator

# News API configuration
NEWSAPI_API_KEY = '1f14fe829730415b8ed33c4a64e52847'

# WeatherAPI configuration
WEATHERAPI_API_KEY = '26747312217e4d72bd7164716230110'
CITY = 'Fayetteville'
COUNTRY = 'The United States'
STATE='Arkansas'

class WeatherNewsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Weather and News App')
        self.setGeometry(100, 100, 1200, 600)
        self.setStyleSheet("background-color: black; color: lightblue;")

        main_layout = QVBoxLayout()

        # Weekly weather forecast with icons
        weekly_weather = self.get_weekly_weather()
        weather_icons_layout = QHBoxLayout()
 
        for entry in weekly_weather:
            date = datetime.strptime(entry['date'], '%Y-%m-%d')
            formatted_date = date.strftime('%A, %b %d')  # Format date as desired (e.g., Monday, Sep 30)
            temperature_celsius = entry['day']['avgtemp_c']
            temperature_fahrenheit = (temperature_celsius * 9/5) + 32  # Convert to Fahrenheit
            description = entry['day']['condition']['text']
            weather_icon_url = entry['day']['condition']['icon']  # Weather icon URL
            weather_icons_pixmap = self.get_weather_icon(weather_icon_url)  # Get icon as QPixmap
            weekly_weather_text = QTextEdit()
            weekly_weather_text.setReadOnly(True)
            weekly_weather_text.append(f'{formatted_date}: {description}, Temperature: {temperature_fahrenheit:.2f} °F')
            weather_icons_layout.addWidget(weather_icons_pixmap)  # Add the weather icon
            weather_icons_layout.addWidget(weekly_weather_text)  # Add the weather forecast

        main_layout.addLayout(weather_icons_layout)

        # Temperature graphs layout
        temperature_graph_layout = QHBoxLayout()

        # Daily temperature graph
        daily_temperature_layout = QVBoxLayout()

        daily_temperature_graph = self.plot_daily_temperature_graph(weekly_weather)
        daily_temperature_layout.addWidget(daily_temperature_graph)

        temperature_graph_layout.addLayout(daily_temperature_layout)

        # Weekly temperature graph
        weekly_temperature_layout = QVBoxLayout()
        
        weekly_temperature_graph = self.plot_weekly_temperature_graph(weekly_weather)
        weekly_temperature_layout.addWidget(weekly_temperature_graph)

        temperature_graph_layout.addLayout(weekly_temperature_layout)

        main_layout.addLayout(temperature_graph_layout)

        # News stories
        news_layout = QVBoxLayout()
        news_label = QLabel('Top 5 News Stories of the Day:')
        news_layout.addWidget(news_label)

        news_text = QTextEdit()
        news_text.setReadOnly(True)
        news_layout.addWidget(news_text)

        news = self.get_top_news()
        for idx, entry in enumerate(news, start=1):
            news_text.append(f'{idx}. {entry["title"]} - {entry["url"]}')

        main_layout.addLayout(news_layout)

        self.setLayout(main_layout)
        self.show()
    
    def get_weather_icon(self, icon_url):
        response = requests.get('http:' + icon_url, stream=True)
        if response.status_code == 200:
            with open('weather_icon.png', 'wb') as f:
                for chunk in response:
                    f.write(chunk)
            pixmap = QPixmap('weather_icon.png')
            label = QLabel()
            label.setPixmap(pixmap)
            return label
    
    def get_weekly_weather(self):
        endpoint = f'https://api.weatherapi.com/v1/forecast.json?key={WEATHERAPI_API_KEY}&q={CITY},{STATE}&days=7'
        response = requests.get(endpoint)
        data = response.json()
        return data['forecast']['forecastday']
    
    def get_temperature_data(self, weekly_weather):
        dates = []
        temperatures = []
        for entry in weekly_weather:
            date = datetime.strptime(entry['date'], '%Y-%m-%d')
            avg_temp = entry['day']['avgtemp_c']
            dates.append(date)
            temperatures.append(avg_temp)
        return dates, temperatures
    
    def plot_daily_temperature_graph(self, weekly_weather):
        dates, temperatures = self.get_temperature_data(weekly_weather)

        # Convert temperatures to Fahrenheit
        temperatures_fahrenheit = [(temp * 9/5) + 32 for temp in temperatures]

        fig, ax = plt.subplots(facecolor='black')  # Set facecolor to black
        ax.plot(dates, temperatures_fahrenheit, label='Temperature (°F)', color='lightblue')  # Set line color to lightblue

        # Set labels and title with lightblue text color
        ax.set_xlabel('Date', color='lightblue')
        ax.set_ylabel('Temperature (°F)', color='lightblue')
        ax.set_title('Temperature Change Throughout the Day', color='lightblue')

        # Set x-axis and y-axis label color
        ax.xaxis.label.set_color('lightblue')
        ax.yaxis.label.set_color('lightblue')

        # Set x-axis and y-axis tick color
        ax.tick_params(axis='x', colors='lightblue')
        ax.tick_params(axis='y', colors='lightblue')

        ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))  # Format x-axis labels
        ax.xaxis.set_major_locator(MaxNLocator(nbins=6))  # Limit number of x-axis labels for readability

        canvas = FigureCanvas(fig)
        return canvas

    def plot_weekly_temperature_graph(self, weekly_weather):
        dates, temperatures = self.get_temperature_data(weekly_weather)

        # Convert temperatures to Fahrenheit
        temperatures_fahrenheit = [(temp * 9/5) + 32 for temp in temperatures]

        fig, ax = plt.subplots(facecolor='black')  # Set facecolor to black
        ax.plot(dates, temperatures_fahrenheit, label='Temperature (°F)', color='lightblue')  # Set line color to lightblue

        # Set labels and title with lightblue text color
        ax.set_xlabel('Date', color='lightblue')
        ax.set_ylabel('Temperature (°F)', color='lightblue')
        ax.set_title('Weekly Temperature Forecast', color='lightblue')

        # Set x-axis and y-axis label color
        ax.xaxis.label.set_color('lightblue')
        ax.yaxis.label.set_color('lightblue')

        # Set x-axis and y-axis tick color
        ax.tick_params(axis='x', colors='lightblue')
        ax.tick_params(axis='y', colors='lightblue')

        ax.xaxis.set_major_formatter(DateFormatter('%m-%d'))  # Format x-axis labels

        canvas = FigureCanvas(fig)
        return canvas  # Return the canvas
    def get_top_news(self):
        endpoint = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWSAPI_API_KEY}&pageSize=6'
        response = requests.get(endpoint)
        data = response.json()
        return data['articles']

if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_news_app = WeatherNewsApp()
    sys.exit(app.exec_())
