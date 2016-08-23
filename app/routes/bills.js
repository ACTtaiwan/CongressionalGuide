var express = require('express');
var router = express.Router();
var sqlite3 = require('sqlite3').verbose();
var db = new sqlite3.Database('db');

/* GET users listing. */
router.get('/', function(req, res, next) {
  var bills = [];
  var selectClause = 'SELECT billId, officialTitle,url FROM bills';
  var params;
  db.each(selectClause, params, function(err, row) {
    console.log(row);
    bills.push(row);
  }, function() {
    res.send(bills);
  });
});

module.exports = router;
