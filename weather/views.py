from django.shortcuts import render
import requests


def index(request):
    weather_data = None

    if request.method == 'POST':
        city = request.POST['city']
        latitude, longitude = get_lat_lon(city)
        if latitude and longitude:
            weather_data = get_weather(latitude, longitude, city)

    return render(request, 'weather/index.html', {'weather_data': weather_data})


def get_lat_lon(city):
    url = f"https://nominatim.openstreetmap.org/search?city={city}&format=json"
    response = requests.get(url)
    data = response.json()

    if data:
        latitude = data[0]['lat']
        longitude = data[0]['lon']
        return latitude, longitude
    return None, None


def get_weather(latitude, longitude, city_name):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"
    response = requests.get(url)
    data = response.json()

    # Extracting necessary details
    weather = {
        'city': city_name,
        'time': data['current_weather']['time'],
        'temperature': data['current_weather']['temperature'],
        'weathercode': data['current_weather']['weathercode'],
        'windspeed': data['current_weather']['windspeed'],
        'winddirection': data['current_weather']['winddirection'],
    }
    return weather
