from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6 import uic
import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()


class WeatherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(script_dir, 'weather_appp.ui')
        uic.loadUi(ui_path, self)

        self.setFixedSize(360, 600)
        self.setWindowTitle("Weather App | Vex")

        self.API_KEY = os.getenv("WEATHER_API_KEY")
        self.city_name_button.clicked.connect(self.get_city_name)
        self.set_image('backgroundjpg.jpg', self.label_name)
        self.set_image('cloud.png', self.label_cloud)

    def set_image(self, filename, target_label):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, filename)
        pixmap = QPixmap(image_path)

        if not pixmap.isNull():
            target_label.setPixmap(pixmap)
            target_label.setScaledContents(True)
        else:
            print(f"Error: Could not find {filename}")

    def get_city_name(self):
        user_text = self.city_name_input.text().strip()

        if not user_text:
            self.label_city_name.setText("Enter a city")
            return

        self.label_city_name.setText(user_text.title())
        URL = f"http://api.openweathermap.org/data/2.5/weather?q={user_text}&appid={self.API_KEY}&units=metric"

        try:
            resp = requests.get(URL)
            data = resp.json()

            if resp.status_code == 200:
                temp = data['main']['temp']
                feeling = data['main']['feels_like']
                humid = data['main']['humidity']
                wind = data['wind']['speed']

                self.label_temperature.setText(f"{round(temp)}°C")
                self.humidity_label.setText(f"💧 Humidity: {humid}%")
                self.feels_like_label.setText(
                    f"🌡 Feels Like: {round(feeling)}°C")
                self.wind_speed_label.setText(f"💨 Wind Speed: {wind} m/s")
                self.label_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

            elif resp.status_code == 404:
                self.label_temperature.setText("Not Found")
                self.humidity_label.setText("Humidity: --")
                self.feels_like_label.setText("Feels Like: --")
                self.wind_speed_label.setText("Wind: --")
            else:
                self.label_temperature.setText("Error")

        except requests.RequestException:
            self.label_temperature.setText("Network Error")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec())
