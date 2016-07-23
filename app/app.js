'use strict';

var express = require('express');
var http = require('http');
var path = require('path');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var CronJob = require('cron').CronJob;

var SUNLIGHT_APIKEY = 'd9eeb169a7224fe28ae0f32aca0dc93e';


var routes = require('./routes/index');
var users = require('./routes/users');
var candidates = require('./routes/candidates');

var PORT = 8080;
var app = express();
var sqlite3 = require('sqlite3').verbose();
var db = new sqlite3.Database('db');
db.serialize(function() {
  db.run('CREATE TABLE IF NOT EXISTS candidates(name TEXT, party TEXT, chamber TEXT, state TEXT, district INT, incumbent INT, fecId TEXT)');
});

new CronJob('0 0 * * * *', function() {
  var candidateIds = [];
  db.each("SELECT fecId FROM candidates", function(err, row) {
    candidateIds.push(row.fecId);
  }, function() {
    fetchCandidatesData('http://realtime.influenceexplorer.com/api/candidates/?format=json&page=1&apikey=' + SUNLIGHT_APIKEY, candidateIds);
  });
}, null, true, 'America/Los_Angeles');


function fetchCandidatesData(url, existedCandidateIds) {
  http.get(url, (res) => {
    var jsonString = ''
    res.on('data', (d) => {
      jsonString += d;
    });
    res.on('end', () => {
      var data = JSON.parse(jsonString);
      var candidates = data.results;
      var stmt = db.prepare('INSERT INTO candidates VALUES (?, ?, ?, ?, ?, ?, ?)');
      for (var i = 0; i < candidates.length; i++) {
        if (candidates[i].election_year == 2016 && existedCandidateIds.indexOf(candidates[i].fec_id) < 0) {
          console.log('adding new candidate: ' + candidates[i].name);
          stmt.run(
            candidates[i].name,
            candidates[i].party,
            candidates[i].office,
            candidates[i].state,
            candidates[i].office_district,
            candidates[i].is_incumbent,
            candidates[i].fec_id
          );
        }
      }
      stmt.finalize();

      if (data.next) {
        fetchCandidatesData(data.next, existedCandidateIds);
      } else {
        console.log('fetch candidates completed');
        db.close();
      }
    });
  }).on('error', (e) => {
    console.log(`Got error: ${e.message}`);
  });
}





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
