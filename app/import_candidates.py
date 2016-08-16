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

dbpath = '/Users/Mark/Google Drive/act/CongressionalGuide/app/db'
if not (dbpath and os.path.isfile(dbpath)):
  print 'db file not found'
  exit() 
  
try:
  db = sqlite3.connect(dbpath)
  c = db.cursor()
except sqlite3.Error:
  print 'sqlite3 error'
  c.close()


jsonpath = '/Users/Mark/Google Drive/act/CongressionalGuide/app/candidates/items3.json'
if not (jsonpath and os.path.isfile(jsonpath)):
  print 'json file not found'
  exit()

congressman = json.load(open(jsonpath))


# Existing schema, total of 18 columns  TODO: make sure we udpate schema 'img_src'
# alter table candidates add column src_img TEXT;

# column = (firstName, lastName , prefix , suffix , party , chamber , state , district , incumbent , bioguideId , fecId , note , website , email , facebook , twitter , youtube , img_src)

# check first/last name pair
# if exists, update_query
# else insert_query

update_query = 'UPDATE candidates SET img_src = ?, facebook = ?, twitter = ?, website = ? where lastName = ? and firstName = ?'
insert_query = 'INSERT INTO candidates VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'

#TODO: error check for bad input (k,v) range out of bound
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

  for k,v in human.iteritems():
    print '(k,v)=('+k+' ,'+v+ ')'
    if k == 'name':
      if len(v.split())!=2:
        print '### bad name ###'
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

  insert_values = (firstName + lastName + prefix + suffix  + party + chamber + state + district + incumbent + bioguideId + fecId + note + website + email + facebook + twitter + youtube + img_src)
  print 'insert_values: '
  print insert_values

  update_values = (img_src + facebook + twitter + website + lastName + firstName)
  print 'update_values: '
  print update_values

  c.execute('SELECT count(*) FROM candidates where firstName == ? and lastName == ?;', firstName+lastName)
  found = c.fetchone()[0]>0
  if found:
    print 'update'
    c.execute(update_query, update_values)
  else:
    print 'insert'
    c.execute(insert_query, insert_values)
  print '[OK]'

print '[done]'
c.close()

