var express = require('express');
var router = express.Router();
var sqlite3 = require('sqlite3').verbose();
var db = new sqlite3.Database('../db/db.sqlite3');

/* GET users listing. */
router.get('/', function(req, res, next) {
  var bills = [];
  var selectClause = 'SELECT billId, officialTitle,url, sponsorId FROM bills';
  var params;
  db.each(selectClause, params, function(err, row) {
    console.log(row);
    bills.push(row);
  }, function() {
    res.send(bills);
  });
});

router.get('/sponsor', function(req, res, next) {
  var sponsors = [];
  var selectClause = 'SELECT cosponsorId, billId FROM cosponsors_bills';
  var params;
  db.each(selectClause, params, function(err, row) {
    console.log(row);
    sponsors.push(row);
  }, function() {
    res.send(sponsors);
  });
});


module.exports = router;
