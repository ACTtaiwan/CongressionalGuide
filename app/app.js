/*jshint esversion: 6 */
'use strict';

var express = require('express');
var http = require('http');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var CronJob = require('cron').CronJob;

var SUNLIGHT_APIKEY = '[apikey]';
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
