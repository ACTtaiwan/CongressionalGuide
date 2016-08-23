#!/usr/bin/python 
import sqlite3, json, os
import logging, sys
from collections import defaultdict

#
# This script dump candidates information from filename.json into our sqlite3 database
#

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

dbpath = '/root/CongressionalGuide/db/db.sqlite3'
if not (dbpath and os.path.isfile(dbpath)):
  print 'db file not found'
  exit() 
  
try:
  db = sqlite3.connect(dbpath)
  c = db.cursor()
except sqlite3.Error:
  print 'sqlite3 error'
  db.close()


jsonpath = '/root/CongressionalGuide/app/candidates/senate.json'
if not (jsonpath and os.path.isfile(jsonpath)):
  print 'json file not found'
  exit()

congressman = json.load(open(jsonpath))


# Existing schema, total of 18 columns  
# alter table candidates add column img_src TEXT;

# column = (firstName, lastName , prefix , suffix , party , chamber , state , district , incumbent , bioguideId , fecId , note , website , email , facebook , twitter , youtube , img_src)

# check first/last name pair
# if exists, update_query
# else insert_query

update_query = 'UPDATE candidates SET img_src = ?, facebook = ?, twitter = ?, website = ?, youtube = ? where firstName like ? and lastName like ? and state = ? and district = ?'
insert_query = 'INSERT INTO candidates VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'

#TODO: error check for bad input (k,v) range out of bound

for human in congressman:
  firstName=(None,)
  lastName=(None,)
  prefix=(None,)
  suffix=(None,)
  party=(None,)
  chamber=(None,)
  state=(None,)
  district=(None,)
  incumbent=(False,)
  bioguideId=(None,)
  fecId=(None,)
  note=(None,)
  website=(None,)
  email=(None,)
  facebook=(None,)
  twitter=(None,)
  youtube=(None,)
  img_src=(None,)

  mesg=''
  for k,v in human.iteritems():
    mesg += '(k,v)=('+k+' ,'+v+ ')\n'
    if k == 'name':
      firstName = v.split()[0],
      lastName = v.split()[-1], 
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

  logging.debug(mesg)
  match_firstName = '%'+firstName[0]+'%',
  match_lastName = '%'+lastName[0]+'%',
  insert_values = (firstName + lastName + prefix + suffix + party + chamber + state + district + incumbent + bioguideId + fecId + note + website + email + facebook + twitter + youtube + img_src)
  update_values = (img_src + facebook + twitter + website + youtube + match_firstName + match_lastName + state + district)

  # Match with existing Sunlight data: lastName, first word of firstName, state and district
  c.execute('SELECT count(*) FROM candidates where firstName like ? and lastName like ? and state = ? and district = ?;', match_firstName + match_lastName + state + district)
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

