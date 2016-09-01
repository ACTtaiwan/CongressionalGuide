var express = require('express');
var router = express.Router();
var sqlite3 = require('sqlite3').verbose();
var db = new sqlite3.Database('../db/db.sqlite3');

/* GET candidates listing. */
router.get('/', function(req, res, next) {
  var candidates = [];
  var selectClauseGenElect = 'SELECT coalesce(max(gen_election_candidate), \'0\') AS generalElection FROM candidates';
  var selectClause = 'SELECT img_src, bioguideId, firstName, lastName, party, chamber, state, district, incumbent, website, email, facebook, twitter, youtube FROM candidates';

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

  db.serialize(function() {
      var generalElection = '';
	  // Find out if we only need to show General Election candidates
	  db.get(selectClauseGenElect + whereClause, params, function(err, row) {
	  	if (row.generalElection == 1) {
			whereClause = updateWhereClause(whereClause, 'gen_election_candidate = 1');
	  	}
	  	// Now select candidates
	  	db.each(selectClause + whereClause, params, function(err, row) {
			candidates.push(row);
	  	}, function() {
		res.send(candidates);
	  	});
	  });
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
