#API Keys
##Sunlight
Candidate and legislative bill information is access via the [Sunlight Foundation API](http://sunlightfoundation.com/api/). Apply for a key on that website.

In `/app/.env` replace `[Sunlight API Key here]` with your Sunlight API key at the line:

`SunlightAPIkey = "[Sunlight API Key here]"`

##GeocodingThe [Texas A&M Geoservices Geocoding API](https://geoservices.tamu.edu/Services/Geocode/WebService/) is used to convert a street address to lat/long which is then fed to Sunlight for a Congressional District.

In `/app/.env` replace `[Geocoding API Key here]` with your Sunlight API key at the line:

`GeocodingAPIkey = "[Geocoding API Key here]"`
