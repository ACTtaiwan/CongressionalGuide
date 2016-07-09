var express = require('express');
var router = express.Router();
var sqlite3 = require('sqlite3').verbose();
var db = new sqlite3.Database('db');

/* GET users listing. */
router.get('/', function(req, res, next) {
  var candidates = [];
  db.each("SELECT name, party, chamber, state, district FROM candidates", function(err, row) {
  	console.log(row);
  	candidates.push(row);
  }, function() {
  	res.send('count: '+candidates.length);
  });
});

module.exports = router;
