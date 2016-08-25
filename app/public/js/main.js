var MY_APP_ID = '[apikey]';
var REST_API_KEY = '[apikey]';

var SUNLIGHT_APIKEY = 'd9eeb169a7224fe28ae0f32aca0dc93e';
var SUNLIGHT_BILLS_URI = 'http://congress.api.sunlightfoundation.com/bills';
var TAIWAN_RELEVANT_BILLS = {
    "hres494-113": {
        name: "H.Res. 494: Affirming the importance of the Taiwan Relations Act",
        link: "https://beta.congress.gov/bill/113th-congress/house-resolution/494"
    },
    "hres185-113": {
        name: "H.Res. 185: Taiwan Travel Act",
        link: "http://beta.congress.gov/bill/113th-congress/house-resolution/185"
    },
    "hres419-113": {
        name: "H.R. 419: The Taiwan Policy Act",
        link: "https://beta.congress.gov/bill/113th-congress/house-bill/419"
    },
    "hr1151-113": {
        name: "H.R. 1151: To direct the Secretary of State to develop a strategy to obtain observer status for Taiwan at the triennial International Civil Aviation Organization Assembly, and for other purposes ",
        link: "https://beta.congress.gov/bill/113th-congress/house-bill/1151"
    },
    "hconres55-113": {
        name: "H.Con.Res. 55: Expressing the sense of Congress that Taiwan and its 23,000,000 people deserve membership in the United Nations",
        link: "https://beta.congress.gov/bill/113th-congress/house-concurrent-resolution/55"
    },
    "hconres29-113": {
        name: "H.Con.Res. 29: Expressing the sense of Congress that the United States should resume normal diplomatic relations with Taiwan, and for other purposes ",
        link: "https://beta.congress.gov/bill/113th-congress/house-concurrent-resolution/29"
    },
    "hr3470-113": {
        name: "H.R.3470 - To affirm the importance of the Taiwan Relations Act, to provide for the transfer of naval vessels to certain foreign countries, and for other purposes.",
        link: "https://beta.congress.gov/bill/113th-congress/house-bill/3470"
    },
    "s12-113": {
        name: "S. 12: Naval Vessel Transfer Act of 2013",
        link: "https://beta.congress.gov/bill/113th-congress/senate-bill/12"
    },
    "s579-113": {
        name: "S. 579: A bill to direct the Secretary of State to develop a strategy to obtain observer status for Taiwan at the triennial International Civil Aviation Organization Assembly, and for other purposes",
        link: "http://beta.congress.gov/bill/113th-congress/senate-bill/579"
    }
};

Parse.initialize("PqNXb0zT1antU2yTXGg6EQltjjJAm2GUWqljxbtE", "3dbk6n78jFXe68CUHVPpJVOwVX2DX7UpfIuYL8oh");

var incumbent_with_challenger_tpl = _.template($("#incumbent-with-challenger-tpl").html());

function getLocation(zip, address) {
    var location = [];
    $.ajax('https://geoservices.tamu.edu/Services/Geocode/WebService/GeocoderWebServiceHttpNonParsed_V04_01.aspx', {
        data: {
            apiKey: 'b37c6aea99ad4425a7e5f90169dbdddb',
            version: '4.01',
            zip: zip,
            streetAddress: address
        },
        async: false,
        success: function(data) {
            var dataArray = data.split(',');
            location = [dataArray[3], dataArray[4]];
        }
    });
    return location;
}

function getDistrict(location) {
    var district = {};
    $.ajax('https://congress.api.sunlightfoundation.com/districts/locate', {
        data: {
            apikey: SUNLIGHT_APIKEY,
            latitude: location[0],
            longitude: location[1]
        },
        async: false,
        success: function(data) {
            district = data.results[0];
        }
    });
    return district;
}

// function getSenators(state) {
//     var senators = [];
//     $.ajax('https://congress.api.sunlightfoundation.com/legislators', {
//         data: {
//             apikey: SUNLIGHT_APIKEY,
//             state: state,
//             chamber: 'senate'
//         },
//         async: false,
//         success: function(data) {
//             senators = data.results;
//         }
//     });
//     return senators;
// }

// function getReps(state, district) {
//     var reps = [];
//     var data = {};
//     if (district) {
//         data = {
//             apikey: SUNLIGHT_APIKEY,
//             state: state,
//             district: district,
//             chamber: 'house'
//         };
//     } else {
//         data = {
//             apikey: SUNLIGHT_APIKEY,
//             state: state,
//             chamber: 'house'
//         };
//     }
//     var reps = [];
//     $.ajax('https://congress.api.sunlightfoundation.com/legislators', {
//         data: data,
//         async: false,
//         success: function(data) {
//             reps = data.results;
//         }
//     });
//     return sortByDistrict(reps);
// }

// function getSenatorCandidates(state) {
//     var challengers = [];
//     $.ajax('http://localhost:8080/candidates', {
//     //$.ajax('https://api.parse.com/1/classes/Challenger', {
//         type: 'GET',
//         contentType: 'application/json',
//         headers: {
//             'X-Parse-Application-Id': 'PqNXb0zT1antU2yTXGg6EQltjjJAm2GUWqljxbtE',
//             'X-Parse-REST-API-Key': '[apikey]'
//         },
//         data: {
//             state: state,
//             chamber: 'senate'
//         },
//         async: false,
//         success: function(data) {
//             challengers = data.results;
//         }
//     });
//     return challengers;
// }

// function getRepCandidates(state, district) {
//     var challengers = [];
//     var query = {};
//     query['state'] = state;
//     query['chamber'] = 'house';
//     if (district) {
//         query['district'] = parseInt(district);
//     }
//     $.ajax('https://api.parse.com/1/classes/Challenger', {
//         type: 'GET',
//         contentType: 'application/json',
//         headers: {
//             'X-Parse-Application-Id': 'PqNXb0zT1antU2yTXGg6EQltjjJAm2GUWqljxbtE',
//             'X-Parse-REST-API-Key': '[apikey]'
//         },
//         data: 'where=' + JSON.stringify(query),
//         async: false,
//         success: function(data) {
//             challengers = data.results;
//         }
//     });
//     return sortByDistrict(challengers);
// }

function getSenatorCandidates(state) {
    return $.ajax('/candidates', {
        type: 'GET',
        contentType: 'application/json',
        data: {
            chamber: 'S',
            state: state
        }
    });
}

function getRepCandidates(state, district) {
    return $.ajax('/candidates', {
        type: 'GET',
        contentType: 'application/json',
        data: {
            chamber: 'H',
            state: state,
            district: district
        }
    });
}

function getBills(){
  return $.ajax('/bills',{
	type: 'GET',
	contentType: 'application/json',
	data:{}
	});

}

function getCosponsor(){
  return $.ajax('/bills/sponsor',{
        type: 'GET',
        contentType: 'application/json',
        data:{}
        });

}

function sortByDistrict(data) {
    return _.sortBy(data, function(congress) {
        if (congress.district == '') {
            return 0;
        } else {
            return parseInt(congress.district);
        }
    });
}

function excludeCurrent(challengers, current) {
    var firstNames = _.map(current, function(c) {
        return c.first_name;
    });
    var lastNames = _.map(current, function(c) {
        return c.last_name;
    });

    return _.filter(challengers, function(c) {
        var name = c.name;
        if (_.some(firstNames, function(n) {
            return name.indexOf(n) > -1
        })) {
            return false;
        }
        if (_.some(lastNames, function(n) {
            return name.indexOf(n) > -1
        })) {
            return false;
        }
        return true;
    });
}

// challengers is the data from DB
// congress is the single person data from sunLight API
function getCurrentContentFromDB(challengers, congress) {

    var congressFromDB =  _.filter(challengers, function(c){
        if (c.name.indexOf(congress.first_name) > -1 && c.name.indexOf(congress.last_name) > -1){
            return true;
        } else {
            return false;
        }
    })[0];

    return congressFromDB!=null ? congressFromDB.content:null;
}

// Build jQuery Ajax get to Sunlight's bill API with the given data
function buildBillCall(data) {
    data['apikey'] = SUNLIGHT_APIKEY;
    data['query'] = 'taiwan';
    return $.get(SUNLIGHT_BILLS_URI, data);
}

$(function() {
    var $loadingIcon = $('#loading-icon');
    var errorMsg = $('#error-msg');

    $('#submit-btn').click(function() {
        // Clean up previous result if any
        $('#senators').empty();
        $('#representatives').empty();

        $('.form-control').css('border', '1px solid #ccc');
        errorMsg.hide();

        var state, district;

        if ($('#address').hasClass('active')) {
            var street = $('[name="street"]').val();
            var zipcode = $('[name="zipcode"]').val();
            var location = getLocation(zipcode, street);
            var distResult = getDistrict(location);
            state = distResult['state'];
            district = distResult['district'];
        } else if ($('#district').hasClass('active')) {
            state = $('[name="state"]').val();
            district = $('[name="district"]').val();
        }

        if (!state || !district) {
            $('.form-control').each(function() {
                if (!$(this).val()) {
                    $(this).css('border', 'solid 2px red');
                    errorMsg.show();
                }
            })
            return;
        }

        $loadingIcon.show();

        var sentaorsDeferred = getSenatorCandidates(state);
        var repsDeferred = getRepCandidates(state, district);
	var bills = getBills();
	var cosponsors = getCosponsor();
	//Clear old data
	$("#senator_row").html("");
	$("#reps_row").html("");
        // Feed information fetched from DB into UI
        $.when(sentaorsDeferred, repsDeferred, bills, cosponsors).then(function(senatorsCallback, repsCallback, billsCallback, coCallback) {

            var senators = senatorsCallback[0];
            var reps = repsCallback[0];
	    var bills = billsCallback[0];
            var cosponsors = coCallback[0];
		for(var k = 0; k < senators.length; k++){	
		   senators[k].bills = [];
                if(senators[k].bioguideId){
                	for(var i = 0; i < bills.length; i++){
				if(senators[k].bioguideId === bills[i].sponsorId){
					senators[k].bills.push({title: bills[i].officialTitle,url: bills[i].url});
				}
				else{
				for(var j = 0; j < cosponsors.length; j++){
					if(cosponsors[j].billId === bills[i].billId && cosponsors[j].cosponsorId===senators[k].bioguideId){
	                                        senators[k].bills.push({title: bills[i].officialTitle,url: bills[i].url});
						break;
					}
				}
				}
			}
			
		}
		}
		for(var k = 0; k < reps.length; k++){
                   reps[k].bills = [];
                if(reps[k].bioguideId){
                                for(var i = 0; i < bills.length; i++){
                                if(reps[k].bioguideId === bills[i].sponsorId){
                                        reps[k].bills.push({title: bills[i].officialTitle,url: bills[i].url});
                                }
                                else{
                                for(var j = 0; j < cosponsors.length; j++){
                                        if(cosponsors[j].billId === bills[i].billId && cosponsors[j].cosponsorId=== reps[k].bioguideId){
                                                reps[k].bills.push({title: bills[i].officialTitle,url: bills[i].url});
						break;
                                        }
                                }
                                }
                        }

                }
	        };
            senators = _.sortBy(senators, function(candidate) {
                return !candidate.incumbent;
            });
            reps = _.sortBy(reps, function(candidate) {
                return !candidate.incumbent;
            });

            $(incumbent_with_challenger_tpl({candidates: senators})).appendTo('#senator_row');
            $(incumbent_with_challenger_tpl({candidates: reps})).appendTo('#reps_row');
	   
            $loadingIcon.hide();
        });
    });
});
