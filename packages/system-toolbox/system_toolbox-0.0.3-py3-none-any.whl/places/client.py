import urllib.parse
from decimal import Decimal
import msgspec
import requests

from places import models


USERNAME = "foxyblue"

# https://www.geonames.org/export/ws-overview.html
base = "http://api.geonames.org"

# https://open-meteo.com/en/docs#latitude=37.58333&longitude=139.65
weather_url = (
    "https://api.open-meteo.com/v1/forecast?"
    "latitude={lat}&longitude={lng}&hourly="
    "temperature_2m,relativehumidity_2m,precipitation_probability"
    ",rain,showers,snowfall,cloudcover,windspeed_10m,windgusts_10m,"
    "uv_index&timezone={timezone}&forecast_days=3&timeformat=unixtime"
)


class GeoClient:
    def __init__(self, username):
        self.username = username

    def search(self, query) -> models.Location | None:
        response = requests.get(f"{base}/searchJSON?q={query}&username={self.username}")
        if response.status_code != 200:
            print(f"Status code: {response.status_code} - {response.json()}")
            return
        payload = response.json()
        locations = payload["geonames"]
        if not locations:
            return
        return msgspec.convert(locations[0], type=models.Location)

    def timezone(self, *, lat: Decimal, lng: Decimal) -> models.TimeZone | None:
        response = requests.get(
            f"{base}/timezoneJSON?lat={lat}&lng={lng}&username={self.username}"
        )
        if response.status_code != 200:
            print(f"Status code: {response.status_code} - {response.json()}")
            return
        payload = response.json()
        return msgspec.convert(payload, type=models.TimeZone)

    def forecast(
        self, *, lat: Decimal, lng: Decimal, timezone: models.TimeZone
    ) -> models.WeatherForecast | None:
        encoded_timezone = urllib.parse.quote(timezone.timezoneId)
        response = requests.get(
            weather_url.format(lat=lat, lng=lng, timezone=encoded_timezone)
        )
        if response.status_code != 200:
            print(f"Status code: {response.status_code} - {response.json()}")
            return
        payload = response.json()
        print(payload)
        forecast = msgspec.convert(payload, type=models.WeatherForecast)
        forecast.timezone = timezone
        return forecast


_instance = GeoClient("foxyblue")

search = _instance.search
timezone = _instance.timezone
forecast = _instance.forecast

"""
Location(
    lat='37.58333',
    lng=Decimal('139.65'),
    geonameId=1854924,
    toponymName='Nozawa-machi',
    countryId='1861060',
    population=0,
    countryCode='JP',
    name='Nozawa-machi',
    fclName='country, state, region,...',
    countryName='Japan',
    adminName1='',
)
"""
