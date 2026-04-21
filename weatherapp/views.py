import requests
from django.shortcuts import render
from django.conf import settings

def index(request):
    data = None
    city = ""

    if request.method == 'POST':
        city = request.POST.get('city', '').strip()

        if city:
            try:
                api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={settings.OPENWEATHER_API_KEY}"
                
                response = requests.get(api_url)
                list_of_data = response.json()

                if list_of_data.get("cod") != 200:
                    data = {"error": list_of_data.get("message", "City not found")}
                else:
                    data = {
                        "city": city.capitalize(),
                        "country_code": list_of_data['sys']['country'],
                        "coordinate": f"{list_of_data['coord']['lon']}, {list_of_data['coord']['lat']}",
                        "temp": f"{list_of_data['main']['temp']} °C",
                        "pressure": list_of_data['main']['pressure'],
                        "humidity": list_of_data['main']['humidity'],
                        "main": list_of_data['weather'][0]['main'],
                        "description": list_of_data['weather'][0]['description'],
                        "icon": list_of_data['weather'][0]['icon'],
                    }

            except Exception as e:
                data = {"error": f"Error: {str(e)}"}

    return render(request, "main/index.html", {
        "data": data,
        "city": city
    })