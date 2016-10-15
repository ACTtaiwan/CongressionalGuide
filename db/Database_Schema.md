# Database Schema

## Retrieve data from Sunlight API
[Congress API](http://tryit.sunlightfoundation.com/congress)

Api key - [apikey]

Click on "/legislators/locate", enter your zip and try it!

!!! PlEASE UPDATE /app/candidates/import_candidates.py WHENEVER THE DATABASE TABLE SCHEMA CHANGE !!!

## Table - legislators
Sourced from functions that gather data from Sunlight (both congress and FEC candidate data) and Ballopedia via Scrapy.

Field name    |   Data type 	| Explain    |    Source      |    Note
------------- | ------------- | ---------- | -------------- | --------------
bioguide_id   | string     	| **Primary key** (only for incumbents) | Sunlight
fecid   	    | string     	| from https://beta.fec.gov/ | Sunlight
first_name    | string			|            | Sunlight, Ballopedia
last_name     | string 			|            | Sunlight, Ballopedia
party         | enumerated 	|  null/R/D/I | Sunlight, Ballopedia
chamber       | enumerated		|  null/senate/house |  Sunlight, Ballopedia
state         | string 			| ex: WA     | Sunlight, Ballopedia
district      | integer			|  0 if Senate | Sunlight, Ballopedia
incumbent     | integer			|  1 if incumbent | Sunlight, Ballopedia
source        | string			| source(s) of data
phone         | string			|     		   | Sunlight | **Need to add**
office        | office # for the member’s DC office | Sunlight | **Need to add**
website       | string			|      	   | Sunlight, Ballopedia
contact_form  | string 			| **a link that you can send msg to** | Sunlight  | **Need to add**
oc_email      | string			|        	   | Sunlight  | **Need to add**
twitter_id    | string			|            | Sunlight, Ballopedia
youtube_id    | string			|       	   | Sunlight, Ballopedia
facebook_id   | string			|            | Sunlight, Ballopedia
img_src       | string			| image URL  | Ballopedia
questionnaire_response | string | HTML     | manually entered
gen\_election\_candidate | integer | 1 if made it past the primary | Ballopedia
duplicate     | integer			| 1 if a dup that is from source (so we can hide it) | manually entered
term_start    | date 			|       	   | Sunlight | **Need to add**
term_end      | date 			|      	   | Sunlight | **Need to add**

