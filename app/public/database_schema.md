# Database Schema

## Retrieve data from Sunlight API
[Congress API](http://tryit.sunlightfoundation.com/congress)

Api key - [apikey]

Click on "/legislators/locate", enter your zip and try it!


## Table - legislators

Field name    |   Data type    |    Explain  |    Source
-------------   | -------------   |   ---------- | --------------
bioguide_id   |    string     | **Primary key** | Sunlight
first_name    |    string|         | Sunlight
last_name     |      string |      | Sunlight
gender        | enumerated| null/M/F       | Sunlight
party         |enumerated |  null/R/D/I | Sunlight
state         |  string | ex: WA     | Sunlight
district      |number|  **house only** | Sunlight
chamber       | enumerated|  null/senate/house |  Sunlight
phone         |        string|     | Sunlight
fax           |   string|          | Sunlight
office        | office # for the member’s DC office | Sunlight
address       |    string|        | Data.gov
website       |      string|      | Sunlight
contact_form  | string | **a link that you can send msg to** | Sunlight
oc_email      |    string|        | Sunlight
twitter_id    |    string|        | Sunlight
youtube_id    |     string|       | Sunlight
facebook_id   |   string|         | Sunlight
term_start    |     date|       | Sunlight
term_end      |      date |      | Sunlight

