#API Keys
##Sunlight
Candidate and legislative bill information is access via the [Sunlight Foundation API](http://sunlightfoundation.com/api/). Apply for a key on that website.

In `/app/app.js` and `/app/public/js/main.js` replace `[apikey]` with your Sunlight API key at the line:

`var SUNLIGHT_APIKEY = '[apikey]';`

##GeocodingThe [Texas A&M Geoservices Geocoding API](https://geoservices.tamu.edu/Services/Geocode/WebService/) is used to convert a street address to lat/long which is then fed to Sunlight for a Congressional District.

In `/app/public/js/main.js` replace `[apikey]` with your API key at the line:

```
$.ajax('https://geoservices.tamu.edu/Services/Geocode/WebService/GeocoderWebServiceHttpNonParsed_V04_01.aspx', {  
		data: {
            apiKey: '[apikey]'
