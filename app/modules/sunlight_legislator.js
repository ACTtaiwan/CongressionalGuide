/*
  API documentation: https://sunlightlabs.github.io/congress/legislators.html
  Sample query: http://congress.api.sunlightfoundation.com/legislators?all_legislators=true&apikey=[apikey]

  Sample response:

{"bioguide_id":"W000819","birthday":"1969-05-20","chamber":"house","contact_form":null,"crp_id":"N00035311","district":6,"facebook_id":"RepMarkWalker","fax":"202-225-8611","fec_ids":["H4NC06052"],"first_name":"Mark","gender":"M","govtrack_id":"412670","in_office":true,"last_name":"Walker","leadership_role":null,"middle_name":null,"name_suffix":null,"nickname":null,"oc_email":"Rep.Walker@opencongress.org","ocd_id":"ocd-division/country:us/state:nc/cd:6","office":"312 Cannon House Office Building","party":"R","phone":"202-225-3065","state":"NC","state_name":"North Carolina","term_end":"2017-01-03","term_start":"2015-01-06","thomas_id":"02255","title":"Rep","twitter_id":"RepMarkWalker","website":"https://walker.house.gov"}
*/

var http = require('http');
var SUNLIGHT_APIKEY = '[apiKey]';
// TODO: Support pagination. Due to constraints, currently only able to get in_office legislators because we are using single page view.
var SUNLIGHT_LEGISLATORS_URI = 'http://congress.api.sunlightfoundation.com/legislators?per_page=all';


module.exports = {
  getFecIdToLegislatorInfoMap: function() {
    var idToLegislatorMap = {};
    var url = SUNLIGHT_LEGISLATORS_URI + "&apikey=" + SUNLIGHT_APIKEY;
    http.get(url, (res) => {
      var jsonString = ''
      res.on('data', (d) => {
        jsonString += d;
      }).on('end', () => {
        var datajson = JSON.parse(jsonString);

        var legislators = datajson.results;
        for (var i = 0; i < legislators.length; i++) {
          // Check if result has fec_id information.
          if (legislators[i].fec_ids != undefined) {
            console.log('Got legislator: ' + legislators[i].bioguide_id + ", fec_ids length: " + legislators[i].fec_ids.length);
            // Construct fed_id to legislator map
            for (var fec_id_index = 0; fec_id_index < legislators[i].fec_ids.length; fec_id_index++) {
              var fec_id = JSON.stringify(legislators[i].fec_ids[fec_id_index]);
              idToLegislatorMap[fec_id] = legislators[i];
            }
          }
        }
      });
    }).on('error', (e) => {
      console.log(`Got error: ${e.message}`);
    });

    return idToLegislatorMap;
  }
};
