var express = require('express');
var router = express.Router();
var sqlite3 = require('sqlite3').verbose();
var db = new sqlite3.Database('db');

/* GET users listing. */
router.get('/', function(req, res, next) {
  var candidates = [];
  var selectClause = 'SELECT firstName, lastName, party, chamber, state, district, incumbent, website, email, facebook, twitter, youtube FROM candidates';

  var whereClause = '';
  var params = {};

  if (req.query.chamber) {
    whereClause = updateWhereClause(whereClause, 'chamber = $chamber');
    params.$chamber = req.query.chamber;
  }

  if (req.query.state) {
    whereClause = updateWhereClause(whereClause, 'state = $state');
    params.$state = req.query.state;
  }

  if (req.query.district) {
    whereClause = updateWhereClause(whereClause, 'district = $district');
    params.$district = req.query.district;
  }

  db.each(selectClause + whereClause, params, function(err, row) {
    console.log(row);
    candidates.push(row);
  }, function() {
    res.send(candidates);
  });
});

function updateWhereClause(whereClause, condition) {
  if (!whereClause.length) {
    whereClause += ' WHERE ';
  } else {
    whereClause += ' AND ';
  }
  whereClause += condition;
  return whereClause;
}

module.exports = router;
