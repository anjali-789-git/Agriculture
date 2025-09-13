from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace with your actual OpenWeatherMap API key
WEATHER_API_KEY = 'your_openweathermap_api_key'

@app.route('/submit-farmer-data', methods=['POST'])
def submit_farmer_data():
    data = request.json
    crop_type = data.get('crop_type')
    farm_size = data.get('farm_size')
    location = data.get('location')

    # Simulate crop health status
    crop_health = "Healthy" if crop_type.lower() == "wheat" else "At Risk"

    return jsonify({
        "message": "Farmer data received",
        "crop_health": crop_health
    })

@app.route('/get-weather', methods=['GET'])
def get_weather():
    location = request.args.get('location')
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    weather_data = response.json()

    return jsonify({
        "location": location,
        "temperature": weather_data['main']['temp'],
        "condition": weather_data['weather'][0]['description']
    })

if __name__ == '__main__':
    app.run(debug=True)

    import sqlite3

def init_db():
    conn = sqlite3.connect('farming.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS farmers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            location TEXT,
            crop_type TEXT,
            farm_size REAL
        )
    ''')
    conn.commit()
    conn.close()

# Run this once to initialize the database
init_db()

from flask import Flask, request, jsonify
import sqlite3
import requests

app = Flask(__name__)
WEATHER_API_KEY = 'your_openweathermap_api_key'

def insert_farmer(name, location, crop_type, farm_size):
    conn = sqlite3.connect('farming.db')
    c = conn.cursor()
    c.execute('INSERT INTO farmers (name, location, crop_type, farm_size) VALUES (?, ?, ?, ?)',
              (name, location, crop_type, farm_size))
    conn.commit()
    conn.close()

@app.route('/submit-farmer-data', methods=['POST'])
def submit_farmer_data():
    data = request.json
    name = data.get('name')
    location = data.get('location')
    crop_type = data.get('crop_type')
    farm_size = data.get('farm_size')

    insert_farmer(name, location, crop_type, farm_size)

    crop_health = "Healthy" if crop_type.lower() == "wheat" else "At Risk"

    return jsonify({
        "message": "Farmer data saved successfully",
        "crop_health": crop_health
    })

@app.route('/get-weather', methods=['GET'])
def get_weather():
    location = request.args.get('location')
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    weather_data = response.json()

    return jsonify({
        "location": location,
        "temperature": weather_data['main']['temp'],
        "condition": weather_data['weather'][0]['description']
    })

if __name__ == '__main__':
    app.run(debug=True)