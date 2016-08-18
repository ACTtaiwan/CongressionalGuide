#!/usr/bin/python 
import sqlite3, json, os
from collections import defaultdict

# Dump candidates information from items.json into our sqlite3 database

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

dbpath = '/root/CongressionalGuide/app/db'
if not (dbpath and os.path.isfile(dbpath)):
  print 'db file not found'
  exit() 
  
try:
  db = sqlite3.connect(dbpath)
  c = db.cursor()
except sqlite3.Error:
  print 'sqlite3 error'
  db.close()


jsonpath = '/root/CongressionalGuide/app/candidates/item1.json'
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

update_query = 'UPDATE candidates SET img_src = ?, facebook = ?, twitter = ?, website = ? where lastName = ? and firstName = ?'
insert_query = 'INSERT INTO candidates VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'

#TODO: error check for bad input (k,v) range out of bound
ns = set()

for human in congressman:
  skip = False

  firstName=(None,)
  lastName=(None,)
  prefix=(None,)
  suffix=(None,)
  party=(None,)
  chamber=('H',)
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
      if v in ns:
        print 'dup'
        skip = True
        break
      ns.add(v)
      if len(v.split())!=2:
        print 'bad name, skip it'
        skip = True 
      else:
        firstName = v.split()[0],
        lastName = v.split()[1], 
    elif k == 'party':
      party = v[0],
    elif k == 'dist':
      dl = [int(d) for d in v if d.isdigit()]
      if len(dl) != 0:
        district = int(''.join(map(str, dl))),
    elif k == 'camp':
      website = v,
    elif k == 'twtr':
      twitter = v,
    elif k == 'fb':
      facebook = v,
    elif k == 'state':
      state = getStateAbbr(v),
    elif k == 'pic':
      img_src = v,

  if skip:
    print '[skip]'
    continue
  print mesg

  insert_values = (firstName + lastName + prefix + suffix  + party + chamber + state + district + incumbent + bioguideId + fecId + note + website + email + facebook + twitter + youtube + img_src)

  update_values = (img_src + facebook + twitter + website + lastName + firstName)

  row_count = c.execute('SELECT count(*) FROM candidates where firstName = ? and lastName = ?;', firstName+lastName)
  if row_count > 0:
    print 'update_values: '
    print update_values
    c.execute(update_query, update_values)
  else:
    print 'insert_values: '
    print insert_values
    c.execute(insert_query, insert_values)
  print '[OK]'


print 'Total updates: ' + str(len(ns))
db.commit()
db.close()

