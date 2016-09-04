var SUNLIGHT_APIKEY = '[apikey]';
var SUNLIGHT_BILLS_URI = 'http://congress.api.sunlightfoundation.com/bills';

var incumbent_with_challenger_tpl = _.template($("#incumbent-with-challenger-tpl").html());

function getLocation(zip, address) {
    var location = [];
    $.ajax('https://geoservices.tamu.edu/Services/Geocode/WebService/GeocoderWebServiceHttpNonParsed_V04_01.aspx', {
        data: {
            apiKey: '[apikey]',
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

        var senatorsDeferred = getSenatorCandidates(state);
        var repsDeferred = getRepCandidates(state, district);
	var bills = getBills();
	var cosponsors = getCosponsor();
	//Clear old data
	$("#senator_row").html("");
	$("#reps_row").html("");
        // Feed information fetched from DB into UI
        $.when(senatorsDeferred, repsDeferred, bills, cosponsors).then(function(senatorsCallback, repsCallback, billsCallback, coCallback) {

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
