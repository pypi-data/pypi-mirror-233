"""
/itinerary
/locations/nozawa
/current
"""

import json
import time
import urllib.parse
from datetime import datetime

import msgspec
from functools import cached_property

from places import client, models

from itinerary import utils


ROOT_DIR = "./data"


class Destination(msgspec.Struct):
    date: datetime
    name: str

    @property
    def location(self) -> models.Location | None:
        filepath = f"{ROOT_DIR}/locations/{self.safe_name}"
        try:
            payload = utils.load_json(filepath)
            return msgspec.convert(payload, models.Location)
        except FileNotFoundError:
            # We don't want to spam the API
            time.sleep(2)
            location = client.search(self.name)
            utils.write_json(filepath, msgspec.to_builtins(location))
            return location

    @property
    def safe_name(self):
        return urllib.parse.quote(self.name)


class Itinerary:
    path = f"{ROOT_DIR}/itinerary"

    def __init__(self, data):
        self.data = data

    @classmethod
    def load(cls):
        data = utils.load_json(self.path)
        return cls(data)

    def save(self):
        utils.write_json(self.path, msgspec.to_builtins(self.data))

    def from_current(self, date: datetime):
        curr = None
        for d in self:
            if d.date > date:
                if curr:
                    yield curr
                    curr = None
                yield d
            else:
                curr = d

    def __iter__(self):
        for d in self.data:
            yield d
