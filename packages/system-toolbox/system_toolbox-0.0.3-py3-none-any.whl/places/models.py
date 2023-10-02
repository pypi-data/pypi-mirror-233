from itertools import repeat
from functools import cached_property
from datetime import datetime
from decimal import Decimal

from dateutil import parser, tz as dateutil_tz

import msgspec


class Location(msgspec.Struct):
    lat: Decimal
    lng: Decimal
    geonameId: int
    toponymName: str
    countryId: str
    population: int
    countryCode: str
    name: str
    fclName: str
    countryName: str
    adminName1: str

    @property
    def geoname_url(self) -> str:
        return f"https://www.geonames.org/{self.geonameId}"

    @property
    def google_maps_url(self) -> str:
        return f"https://www.google.co.uk/maps/@{self.lat},{self.lng},14z?entry=ttu"


class TimeZone(msgspec.Struct):
    sunrise: str
    sunset: str
    lng: Decimal
    lat: Decimal
    countryCode: str
    gmtOffset: int
    rawOffset: int
    timezoneId: str
    time: str

    @property
    def tz(self):
        return dateutil_tz.gettz(self.timezoneId)

    @property
    def sunrise_dt(self) -> datetime:
        dt = parser.parse(self.sunrise)
        return dt.replace(tzinfo=self.tz)

    @property
    def sunset_dt(self) -> datetime:
        dt = parser.parse(self.sunset)
        return dt.replace(tzinfo=self.tz)


class DataPoint(msgspec.Struct):
    time: datetime
    temperature_2m: Decimal
    relativehumidity_2m: int
    precipitation_probability: int
    rain: Decimal
    showers: Decimal
    snowfall: Decimal
    cloudcover: int
    windspeed_10m: Decimal
    windgusts_10m: Decimal
    uv_index: Decimal
    tz: dateutil_tz

    @property
    def localtime(self):
        return self.time.astimezone(self.tz)


class HourlyForecast(msgspec.Struct):
    # UTC
    time: list[datetime]
    # Air temperature at 2 meters above ground. (°C)
    temperature_2m: list[Decimal]
    # (%)
    relativehumidity_2m: list[int]
    # (%)
    precipitation_probability: list[int]
    # (mm)
    rain: list[Decimal]
    # (mm)
    showers: list[Decimal]
    # (cm)
    snowfall: list[Decimal]
    # (%)
    cloudcover: list[int]
    # Wind speed at 10 meters above ground. (km/h)
    windspeed_10m: list[Decimal]
    # Gusts at 10 meters above ground as a maximum of the preceding hour. (km/h)
    windgusts_10m: list[Decimal]
    # 0 - 10
    uv_index: list[Decimal]

    def iterate(self, timezone=dateutil_tz.tzutc()):
        return (
            DataPoint(*tup)
            for tup in zip(
                self.time,
                self.temperature_2m,
                self.relativehumidity_2m,
                self.precipitation_probability,
                self.rain,
                self.showers,
                self.snowfall,
                self.cloudcover,
                self.windspeed_10m,
                self.windgusts_10m,
                self.uv_index,
                repeat(timezone),
            )
        )


class WeatherForecast(msgspec.Struct):
    lat: Decimal = msgspec.field(name="latitude")
    lng: Decimal = msgspec.field(name="longitude")
    hourly: HourlyForecast
    _timezone: TimeZone | None = None

    @property
    def timezone(self) -> TimeZone:
        return self._timezone

    @timezone.setter
    def timezone(self, value):
        self._timezone = value
