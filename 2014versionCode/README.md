# Congressional Guide

## Dev Setup
Start the local server

```
python -m SimpleHTTPServer
```

Redirect your browser to
```
http://localhost:8000/
```

Public address
```
http://voterguide.americancitizensfortaiwan.org/
```

## Problem Statement

US Citizens have no easy place to go to find out if candidates for the U.S. Congress, both new and those running again, support Taiwan.

## Proposed Requirements

A website with following features:

*   Like a voter guide. [Example](http://vote.ly.g0v.tw/)
*   Search congressman or candidates by address/zip code/city/state.
	*   Need address as well because districts cross zip areas; zip+4 can be used, but not many people know their +4.
*   Show if members of Congress sponsored or cosponsored, or voted for any Taiwan related legislation.
*   Show a questionnaire for people to copy and send to candidates and members of Congress, as well as steps on how to find the contact info and send it.
*   Be able to enter in questionnaire answers or other notes for current candidates or members of Congress.
*    Refer people to register to vote to [](http://registertovote.org)[http://registertovote.org](http://registertovote.org)

A server that can save information such as candidates running, questionnaire answers/notes.

### User Flow
* User go to congressional guide page. Based on their ip address, the website displays relative house and congress details (along with candidates) to that user
     * If the ip doesn't work, we ask them to enter full address
* Congressman details
     * Their contact information: website, twitter, email
     * The answers for the questionnaire (if the questionnaire hasn't been answered, prompt user to send it to the congressman)
     * Their act related to Taiwan

**Notes**

[FEC](http://www.fec.gov/data/CandidateSummary.do?format=html&election_yr=2014) lists candidates, API is https://explore.data.gov/Contributors/FEC-Candidates/wuxv-c8xz?. However they do not list links to the candidate site or candidate contact info.

[Politics1.com](http://www.politics1.com/congress.htm) does show candidate info, but you would have to either refer people to it for them to send the questionnaire or somehow scrape the info to load into the local DB.

## Architecture Design

Design in one sentence: A single-page application (SPA) that consume data from Sunlight Foundation API and S3 (static files).

**Front End**

There are several frameworks to use at the front end:

*   [Bootstrap](http://getbootstrap.com)
* [Backbone.js](http://backbonejs.org)
	* [jQuery](http://jquery.com)
	* [Underscore.js](http://underscorejs.org)
	* [Marionette.js](http://marionettejs.com)

SPA  is chose because we want to minimize the duplication of common  HTML/CSS/JS code. Bootstrap provides lots of components that can help  developers more productive. Backbone.js with Marionette.js provides modularization, makes it better for collaboration and maintenance.

**Back End**

*   [Sunglight Foundation API](http://sunlightfoundation.com/api/)
*   [AWS S3](http://aws.amazon.com/s3/)
*   [Parse](http://parse.com)

The reason we want to use S3 is because we need a good place to host congress member profile pictures.

We still need to consider to have our own back end server in the future if lots of traffic is on the website.

## Development Notes

### APIs

The data is retrieved from Sunlight Foundation.

*   API URL: [](http://sunlightfoundation.com/api/)[http://sunlightfoundation.com/api/](http://sunlightfoundation.com/api/)
*   API Key: [apikey]

### Local Testing

To start a local server to test, run `python -m SimpleHTTPServer`in the folder.

### Source Code Organization

The source code is grouped by modules. Below is an example([source](http://stackoverflow.com/a/21054631)):

    /js
       /application
            router.js    // router here or for each module
            main.js      // app entry point
       /profile
            /collections
            /models
            /views
            /templates
            profile.js   // module entry point
       /news
            /collections
            /models
            /views
            /templates
            news.js      // module entry point

### URL (Route) Patterns

Below use **User** as an example model.

| Path | backbone function | Used for |  
|  ------   | ------    | ------    |  
| /users | listUsers | display a list of users / display search result |
|  /users/new | newUser | render a HTML form for creating a new user |  
| /users/:id | showUser | display a specific user |  
| /users/:id/edit | editUser | render a HTML form for editing a user |

## Data Source

** List of candidates **  

*   [FEC Candidate](https://explore.data.gov/Contributors/FEC-Candidates/wuxv-c8xz)  
    *   States are in the 3th and 4th character of the candidate ID  
*   [Sunlight congress API v3](http://sunlightfoundation.com/api/)  

** Information about the candidates **  

*   [Congress/senator's personal website/contact information from Politics1](http://www.politics1.com/congress.htm)

** Information about the congress district **

* Query district by ip
* Query district by address