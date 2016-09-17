/*jshint esversion: 6 */
'use strict';

//require dotenv to store our project key-value in .env
var dotenv = require('dotenv').config();

var express = require('express');
var http = require('http');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var CronJob = require('cron').CronJob;

/*
* storing APIkey in .env file
* reference: https://github.com/motdotla/dotenv
*/
var SUNLIGHT_APIKEY = process.env.APIkey; 
var LEGISTLATOR_URL = 'http://congress.api.sunlightfoundation.com/legislators';
var BILL_URL = 'http://congress.api.sunlightfoundation.com/bills?fields=official_title,urls.congress,sponsor_id,cosponsor_ids';

var BILL_RANGE = '&bill_id__in=sconres38-114|hconres88-114|s2426-114|hr4154-114|hr1853-114|hconres76-114|s1683-113|hres494-113|hjres109-113|sjres31-113|hconres55-113|hconres46-113|hr1151-113|s579-113|hres185-113|hconres29-113|s12-113|hr419-113';

var routes = require('./routes/index');
var users = require('./routes/users');
var candidates = require('./routes/candidates');
var bills = require('./routes/bills');
var sunlight_legislator = require('./modules/sunlight_legislator');

var PORT = 8080;
var app = express();
var sqlite3 = require('sqlite3').verbose();
var db = new sqlite3.Database('../db/db.sqlite3');
db.serialize(function() {
  db.run('CREATE TABLE IF NOT EXISTS candidates(' +
    'firstName TEXT, ' +
    'lastName TEXT, ' +
    'prefix TEXT, ' +
    'suffix TEXT, ' +
    'party TEXT, ' +
    'chamber TEXT, ' +
    'state TEXT, ' +
    'district INTEGER, ' +
    'incumbent INTEGER, ' +
    'source TEXT, ' +
    'bioguideId TEXT,' +
    'fecId TEXT,' +
    'website TEXT,' +
    'email TEXT,' +
    'facebook TEXT,' +
    'twitter TEXT,' +
    'youtube TEXT,' +
    'img_src TEXT, ' +
    'questionnaire_response TEXT,' +
    'gen_election_candidate INTEGER' +
    ')');

  db.run('CREATE TABLE IF NOT EXISTS bills(' +
    'billId TEXT, ' +
    'officialTitle BLOB, ' +
    'sponsorId TEXT, ' +
    'url TEXT' +
  ')');

  db.run('CREATE TABLE IF NOT EXISTS cosponsors_bills(' +
    'cid INTEGER PRIMARY KEY ASC, ' +
    'cosponsorId TEXT REFERENCES candidates (bioguideId), ' +
    'billId TEXT REFERENCES bills (billId)' +
  ')');
});

// Run midnight job to fetch 
// new CronJob('0 0 * * * *', function() {
//   var candidateFecIds = [];
//   fecId should be a good unique ID for candidate
//   db.each("SELECT fecId FROM candidates", function(err, row) {
//     candidateFecIds.push(row.fecId);
//   }, function() {
// 	fetchCandidatesData(
// 	'http://realtime.influenceexplorer.com/api/candidates/?format=json&page=1&apikey=' + 
// 	SUNLIGHT_APIKEY, candidateFecIds);
//   });
// }, null, true, 'America/Los_Angeles');
// 
// function fetchCandidatesData(url, existedCandidateFecIds) {
// http.get(url, (res) => {
//  var jsonString = '';
//  res.on('data', (d) => {
//    jsonString += d;
//  });
//  res.on('end', () => {
//    var data = JSON.parse(jsonString);
//    var candidates = data.results;
// 
//    var stmt = db.prepare('INSERT INTO candidates (firstName, lastName, party, chamber, state, district, incumbent, fecId) ' +
// 	 'VALUES ($firstName, $lastName, $party, $chamber, $state, $district, $incumbent, $fecId)');
//    for (var i = 0; i < candidates.length; i++) {
// 	 if ((candidates[i].office === 'H' || candidates[i].office === 'S') &&
// 		 candidates[i].election_year == 2016 && 
// 		 existedCandidateFecIds.indexOf(candidates[i].fec_id) < 0) {
// 	   console.log('adding new candidate: ' + candidates[i].name);
// 	   var name = candidates[i].name.split(',');
// 	   var lastName, firstName;
// 	   if (name.length === 2) {
// 		 lastName = toTitleCase(name[0].trim());
// 		 firstName = toTitleCase(name[1].trim());
// 	   } else {
// 		 lastName = null;
// 		 firstName = name;
// 	   }
// 
// 	   stmt.run({
// 		 $firstName: firstName,
// 		 $lastName: lastName,
// 		 $party: candidates[i].party,
// 		 $chamber: candidates[i].office,
// 		 $state: candidates[i].state,
// 		 $district: candidates[i].office_district,
// 		 $incumbent: candidates[i].is_incumbent,
// 		 $fecId: candidates[i].fec_id
// 	   });
// 	 }
//    }
//    stmt.finalize();
// 
//    if (data.next) {
// 	 fetchCandidatesData(data.next, existedCandidateFecIds);
//    } else {
// 	 console.log('fetch candidates completed');
// 	 db.close();
//    }
//  });
// }).on('error', (e) => {
//  console.log(`Got error: ${e.message}`);
// });
// }
//  
// function toTitleCase(str) {
// 	return str.replace(/\b\w+/g,function(s){return s.charAt(0).toUpperCase() + 
// 		s.substr(1).toLowerCase();});
// }

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

// uncomment after placing your favicon in /public
//app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', routes);
app.use('/users', users);
app.use('/candidates', candidates);
app.use('/bills', bills);
// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  next(err);
});

// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
  app.use(function(err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
      message: err.message,
      error: err
    });
  });
}

// production error handler
// no stacktraces leaked to user
app.use(function(err, req, res, next) {
  res.status(err.status || 500);
  res.render('error', {
    message: err.message,
    error: {}
  });
});

app.listen(PORT);
module.exports = app;
