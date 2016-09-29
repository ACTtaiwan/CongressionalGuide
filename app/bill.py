#!/usr/bin/python 
import sqlite3, json, os
import logging, sys
import requests

# !!! UPDATE HERE WHENEVER THE DATABASE TABLE SCHEMA CHANGE !!!
#
# The order matter when we want to insert the value, current schema:
# CREATE TABLE bills (billId TEXT PRIMARY KEY REFERENCES cosponsors_bills (billId), bill_type TEXT, number INTEGER, officialTitle BLOB, sponsorId TEXT, url TEXT UNIQUE);


logging.basicConfig(stream=sys.stderr,level=logging.DEBUG)

URL = 'https://congress.api.sunlightfoundation.com/bills?apikey=d9eeb169a7224fe28ae0f32aca0dc93e&bill_id__in=hr6047-114%7Csconres38-114%7Chconres88-114%7Cs2426-114%7Chr4154-114%7Chr1853-114%7Chconres76-114%7Cs1683-113%7Chres494-113%7Chjres109-113%7Csjres31-113%7Chconres55-113%7Chconres46-113%7Chr1151-113%7Cs579-113%7Chres185-113%7Chconres29-113%7Cs12-113%7Chr419-113&fields=bill_type,number,official_title,urls.congress,sponsor_id,cosponsor_ids'

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

bills_insert_query = 'INSERT INTO bills VALUES (?,?,?,?,?,?)'
cosponsors_bills_insert_query = 'INSERT INTO cosponsors_bills VALUES (?,?,?)'

r = requests.get(URL)
js = r.json()

ai = (None,) # auto increment
for i in js['results']:

    # prepare data for db
    billid=(None,)
    title=(None,)
    sponsorid=(None,)
    url=(None,)
    cosponsorid_list = ()
    bill_type = (None,)
    number = (None)    

    for k,v in i.iteritems():
        if k == 'bill_id':
            logging.info('bill_id: %s', v)
            billid = v,
        elif k == 'cosponsor_ids':
            logging.info('cosponsor_ids LIST: %s', v)
            for cosponsorid in v:
                logging.info('cosponsor_ids ITEM: %s', cosponsorid)
                cosponsorid_list += cosponsorid,
        elif k == 'urls':
            logging.info('url: %s', v)
            url = v['congress'],
        elif k == 'sponsor_id':
            logging.info('sponsor_id: %s', v)
            sponsorid = v,
        elif k == 'official_title':
            logging.info('official_title: %s', v)
            title = v,
        elif k == 'bill_type':
        	logging.info('bill_type: %s', v)
        	bill_type = v,
        elif k == 'number':
        	logging.info('number: %s', v)
        	number = v,
        else:
            logging.warning('unknown key %s', k)        
        
    bills_insert_values = (billid + bill_type + number + title + sponsorid + url)
    logging.info('in 1: %s', bills_insert_values)
    c.execute(bills_insert_query, bills_insert_values)

    for cd in cosponsorid_list:
        cosponsors_bills_insert_values = (ai + tuple([cd]) + billid)
        logging.info('in 2: %s', cosponsors_bills_insert_values)
        c.execute(cosponsors_bills_insert_query, cosponsors_bills_insert_values)
    
    logging.info('[OK]\n\n')

db.commit()
db.close()
