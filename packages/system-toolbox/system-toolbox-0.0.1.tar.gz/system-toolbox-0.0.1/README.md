TODO:

- Fix saving null, or "None" under location

# Fetches locations

```
python snippet1.py
```

# Fetches weather data

```
python snippet.py
```

## Small Design

### Itinerary

I can probably just create the html for the itinerary
in python.

- parse for locations and dates to create itinerary
  insert the `geonameId`. Alternately us lng,lat
  https://www.google.co.uk/maps/@-33.934875,18.4180092,14.15z?entry=ttu
  the z level is shown too

- 2023-10-26 [Cape Town](https://www.geonames.org/3369157)
- 2023-10-30 Tokyo
- 2023-11-02 Nowaza Onsen

### Forecast

If next 3 days are shown in the itinerary, fetch weather
for all 3. Otherwise only current.

## Auth

Readd auth:
- https://github.com/foxyblue/flask-calendar/blob/master/flask_calendar/actions.py#L90-L91

## Production Config For `flask-calendar`

```
+BASE_URL = "https://travel-calendar.nfshost.com"
+HOST_IP = None

# To Update
 PASSWORD_SALT = "something random and full of non-standard characters"
 SECRET_KEY = "hahah"
 LOCALE = "en_US.UTF-8"
 # This needs to update
 TIMEZONE = "US/Central"
```

# Sync'ing data

1. Install and Configure AWS CLI

```
# Create service account
aws configure
aws s3 sync local-folder-path s3://bucket-name/
```
