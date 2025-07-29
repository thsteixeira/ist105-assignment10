import random, requests, os
#from dotenv import load_dotenv
from datetime import datetime
from django.shortcuts import render
from .forms import ContinentForm
from pymongo import MongoClient

from .models import Continent
 
#load_dotenv()
 
#MONGO_URI = 'mongodb://54.161.115.118:27017'
#client = MongoClient(MONGO_URI)
#db = client.geodata
 
OPENWEATHERMAP_API_KEY = 'e6c8a91103d088a28391d8e14b75ccca'

 
def continent_view(request):
    if request.method == 'POST':
        form = ContinentForm(request.POST)
        if form.is_valid():
            continent = form.cleaned_data['continent']
            response = requests.get(f"https://restcountries.com/v3.1/region/{continent}")
            countries = random.sample(response.json(), 5)
            results = []
            for c in countries:
                capital = c.get("capital", [""])[0]
                name = c.get("name", {}).get("common", "")
                pop = c.get("population", 0)
                try:
                    weather = requests.get(
                        f"https://api.openweathermap.org/data/2.5/weather",
                        params={"q": capital, "appid": OPENWEATHERMAP_API_KEY, "units": "metric"}
                    ).json()
                    temp = weather['main']['temp']
                    desc = weather['weather'][0]['description']
                except:
                    temp, desc = None, "Not found"
 
                results.append({
                    "country": name,
                    "capital": capital,
                    "population": pop,
                    "temperature_celsius": temp,
                    "weather_description": desc
                })
 
            record = Continent.objects.create(
                continent=continent,
                results=results
            )

            return render(request, "search_results.html", {"results": results})
    else:
        form = ContinentForm()
    return render(request, "continent_form.html", {"form": form})
 
def history_view(request):
    history = Continent.objects.order_by('-search_timestamp')
    return render(request, "history.html", {"history": history})
