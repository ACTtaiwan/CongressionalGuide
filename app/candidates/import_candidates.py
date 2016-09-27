#!/usr/bin/python 
import sqlite3, json, os
import logging, sys
from collections import defaultdict
from nameparser import HumanName

#
# This script moves candidate information from filename.json into the sqlite3 database
#
# !!! UPDATE HERE WHENEVER THE DATABASE TABLE SCHEMA CHANGE !!!
#
# The order matter when we want to insert the value, current schema:
# CREATE TABLE candidates (firstName TEXT, lastName TEXT, prefix TEXT, suffix TEXT, party TEXT, chamber TEXT, state TEXT, district INTEGER, incumbent INTEGER, source TEXT, bioguideId TEXT PRIMARY KEY UNIQUE, fecId TEXT UNIQUE, website TEXT, email TEXT UNIQUE, facebook TEXT UNIQUE, twitter TEXT UNIQUE, youtube TEXT UNIQUE, img_src TEXT, questionnaire_response TEXT, gen_election_candidate INTEGER DEFAULT (0), duplicate INTEGER, candidate_url TEXT UNIQUE);


logging.basicConfig(stream=sys.stderr,level=logging.DEBUG)

def getStateAbbr(s):
  try:
    return {
      'Alabama' : 'AL',
      'Montana' : 'MT',
      'Alaska' : 'AK', 
      'Nebraska' : 'NE',
      'Arizona' : 'AZ' ,
      'Nevada' : 'NV',
      'Arkansas' : 'AR' ,
      'New Hampshire' : 'NH',
      'California' : 'CA' ,
      'New Jersey' : 'NJ',
      'Colorado' : 'CO' ,
      'New Mexico' : 'NM',
      'Connecticut' : 'CT',
      'New York' : 'NY',
      'Delaware' : 'DE' ,
      'North Carolina' : 'NC',
      'Florida' : 'FL' ,
      'North Dakota' : 'ND',
      'Georgia' : 'GA' ,
      'Ohio' : 'OH',
      'Hawaii' : 'HI' ,
      'Oklahoma' : 'OK',
      'Idaho' : 'ID' ,
      'Oregon' : 'OR',
      'Illinois' : 'IL' ,
      'Pennsylvania' : 'PA',
      'Indiana' : 'IN' ,
      'Rhode Island' : 'RI',
      'Iowa' : 'IA' ,
      'South Carolina' : 'SC',
      'Kansas' : 'KS' ,
      'South Dakota' : 'SD',
      'Kentucky' : 'KY' ,
      'Tennessee' : 'TN',
      'Louisiana' : 'LA' ,
      'Texas' : 'TX',
      'Maine' : 'ME' ,
      'Utah' : 'UT',
      'Maryland' : 'MD' ,
      'Vermont' : 'VT',
      'Massachusetts' : 'MA' ,
      'Virginia' : 'VA',
      'Michigan' : 'MI' ,
      'Washington' : 'WA',
      'Minnesota' : 'MN' ,
      'West Virginia' : 'WV',
      'Mississippi' : 'MS' ,
      'Wisconsin' : 'WI',
      'Missouri' : 'MO' ,
      'Wyoming' : 'WY',
    }[s]
  except:
    print 'key ' + s + ' not found!'
    return None

dbpath = '../../db/db.sqlite3'
if not (dbpath and os.path.isfile(dbpath)):
  print 'db file not found'
  exit() 
  
try:
  db = sqlite3.connect(dbpath)
  c = db.cursor()
except sqlite3.Error:
  print 'sqlite3 error'
  db.close()


#jsonpath = '/root/CongressionalGuide/app/candidates/import.json'
jsonpath = str(sys.argv[1])
if not (jsonpath and os.path.isfile(jsonpath)):
  print 'candidates json file not found'
  exit()

congressman = json.load(open(jsonpath))


# check first/last name pair
# if exists, update_query
# else insert_query

update_query = 'UPDATE candidates SET candidate_url = ?, img_src = ?, facebook = ?, twitter = ?, website = ?, youtube = ?, source = ?, gen_election_candidate = ?, incumbent = ?, district = ? where firstName like ? and lastName like ? and state = ?'
#update_query = 'UPDATE candidates SET candidate_url = ?, img_src = ?, facebook = ?, twitter = ?, website = ?, youtube = ?, source = ?, gen_election_candidate = ?, incumbent = ? where firstName like ? and lastName like ? and state = ? and district = ?'

# !!! UPDATE HERE WHENEVER THE DATABASE TABLE SCHEMA CHANGE !!!
insert_query = 'INSERT INTO candidates VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'

for human in congressman:
  firstName=(None,)
  lastName=(None,)
  prefix=(None,)
  suffix=(None,)
  party=(None,)
  chamber=(None,)
  state=(None,)
  district=(0,)
  incumbent=(None,)
  bioguideId=(None,)
  fecId=(None,)
  source=('ballotpedia',)
  website=(None,)
  email=(None,)
  facebook=(None,)
  twitter=(None,)
  youtube=(None,)
  img_src=(None,)
  questionnaire_response=(None,)
  #TODO: NH primary election 9/13, their candidate will have null value here
  gen_election_candidate=(None,)
  candidate_url=(None,)
  duplicate=(None,)

  mesg=''
  for k,v in human.iteritems():
    mesg += '(k,v)=(' + k + ' ,' + str(v) + ')\n'
    if k == 'name':
      v = v.replace('%27','\'') #clean up scraped single quote issue
      if v.endswith(')'): #handle name like 'Bill Otto (Missouri)'
      	lp = v.find('(')
      	v = v[:lp-1]
      v = v.replace('%22','\"') #change nickname parenthesis to quotes
      fullName = HumanName(v)
      prefix = fullName.title,
      if len(fullName.first) < 3: # if only 1st initial, then need to include middle name
      	firstName = fullName.first + ' ' + fullName.middle,
      else:
      	firstName = fullName.first,
      lastName = fullName.last,
      suffix = fullName.suffix, 
    elif k == 'party':
      party = v[0],
    elif k == 'dist':
      dl = [int(d) for d in v if d.isdigit()]
      if len(dl) != 0:
        district = int(''.join(map(str, dl))),
    elif k == 'camp':
      website = v,
    elif k == 'twtr':
      tv = v[v.find('twitter.com')+len('twitter.com')+1:]
      twitter = tv[:tv.find('/')].replace('@',''),
    elif k == 'fb':
      facebook = v,
    elif k == 'state':
      state = getStateAbbr(v),
    elif k == 'pic':
      img_src = v,
    elif k == 'chamber':
      chamber = v,
    elif k == 'youtube':
      youtube = v,
    elif k == 'incumbent':
      incumbent = v,
    elif k == 'gen_election_candidate':
      gen_election_candidate = v,
    elif k == 'url':
      candidate_url = v,

  logging.debug(mesg)
  match_firstName = '%'+firstName[0]+'%',
  match_lastName = '%'+lastName[0]+'%',

# !!! UPDATE HERE WHENEVER THE DATABASE TABLE SCHEMA CHANGE !!!
  insert_values = (firstName + lastName + prefix + suffix + party + chamber + state + district + incumbent + source + bioguideId + fecId + website + email + facebook + twitter + youtube + img_src + questionnaire_response + gen_election_candidate + duplicate + candidate_url)
  update_values = (candidate_url + img_src + facebook + twitter + website + youtube + source + gen_election_candidate + incumbent + district + match_firstName + match_lastName + state)
  #update_values = (candidate_url + img_src + facebook + twitter + website + youtube + source + gen_election_candidate + incumbent + match_firstName + match_lastName + state + district)

  # Match with existing Sunlight data: lastName, first word of firstName, state and district
  # no district for senate
  c.execute('SELECT count(*) FROM candidates where firstName like ? and lastName like ? and state = ? ;', match_firstName + match_lastName + state )
  #c.execute('SELECT count(*) FROM candidates where firstName like ? and lastName like ? and state = ? and district = ?;', match_firstName + match_lastName + state + district)
  obj = c.fetchone()
  if obj[0]:
    logging.info('update_values: %s', update_values)
    c.execute(update_query, update_values)
  else:
    logging.info('insert_values: %s', insert_values)
    c.execute(insert_query, insert_values)
  logging.info('[OK]\n\n')


db.commit()
db.close()

