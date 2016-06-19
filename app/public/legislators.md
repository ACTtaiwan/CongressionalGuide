# Legislator

## Sunlight API

- documentation: https://sunlightlabs.github.io/congress/legislators.html
- API URL: http://sunlightfoundation.com/api/
- API Key: [apikey]

## Data.gov
- https://explore.data.gov/Contributors/FEC-Candidates/wuxv-c8xz

## Find members of Congress according to district

### By latitude & longitude
```
/legislators/locate?latitude=42.96&longitude=-108.09
```
For a given latitude and longitude, this should return up to 1 representative and 2 senators.

### By zipcode
```
/legislators/locate?zip=11216
```
Recommend **against using zip codes** to look up members of Congress since a zipcode may intersect multiple Congressional districts

## Field to display

### Background

Field name    |   Explain  |    Source
------------- | ---------- | --------------
bioguide_id   | **unique ID** | Sunlight
first_name    |            | Sunlight
last_name     |            | Sunlight
party         | R, D, or I | Sunlight
state         | ex: WA     | Sunlight
district      | **house only** | Sunlight
chamber       | senate or house |  Sunlight

### Contact info

Field name    |   Explain  |    Source
------------- | ---------- | --------------
phone         |            | Sunlight
fax           |            | Sunlight
office        | office # for the member’s DC office | Sunlight
address       |            | Data.gov
website       |            | Sunlight
contact_form  | **act like email i think** | Sunlight
e-mail        |            | **not found**

### Social media

Field name    |   Explain  |    Source
------------- | ---------- | --------------
twitter_id    |            | Sunlight
youtube_id    |            | Sunlight
facebook_id   |            | Sunlight

## Other available field
Field name    |   Explain  |    Source
------------- | ---------- | --------------
nickname      |            | Sunlight
gender        | M, F       | Sunlight
state_name    |            | Sunlight
state_rank    | junior, senior | sunlight
title         | Sen, Rep, Del, or Com | Sunlight
senate_class  | 1,2,3      | Sunlight
birthday      |            | Sunlight
term_start    |            | Sunlight
term_end      |            | Sunlight
year          |            | Data.gov







