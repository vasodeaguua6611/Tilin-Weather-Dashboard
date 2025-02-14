from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# THIS MUST COME BEFORE app.run()
@app.route('/weather', methods=['POST', 'GET'])
def get_weather():
    if request.method == 'POST':
        city = request.form['city']
        api_key = os.getenv('API_KEY')
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
        
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            weather_data = {
                'city': city,
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'condition': data['weather'][0]['main'].lower()  # Add this line
            }
            return render_template('index.html', weather=weather_data)
        else:
            error = "City not found. Please try again."
            return render_template('index.html', error=error)
    else:
        return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)