#!/usr/bin/python 
import sqlite3, json, os
import logging, sys
import requests

logging.basicConfig(stream=sys.stderr,level=logging.DEBUG)

URL = 'https://congress.api.sunlightfoundation.com/bills?apikey=' os.environ['SunlightAPIkey'] '&bill_id__in=sconres38-114%7Chconres88-114%7Cs2426-114%7Chr4154-114%7Chr1853-114%7Chconres76-114%7Cs1683-113%7Chres494-113%7Chjres109-113%7Csjres31-113%7Chconres55-113%7Chconres46-113%7Chr1151-113%7Cs579-113%7Chres185-113%7Chconres29-113%7Cs12-113%7Chr419-113&fields=official_title,urls.congress,sponsor_id,cosponsor_ids'

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

bills_insert_query = 'INSERT INTO bills VALUES (?,?,?,?)'
cosponsors_bills_insert_query = 'INSERT INTO cosponsors_bills VALUES (?,?,?)'

r = requests.get(URL)
js = r.json()

ai = (None,) # auto increment
for i in js['results']:

    # prepare data for db
    bid=(None,)
    ot=(None,)
    sid=(None,)
    url=(None,)
    cid_list = () 

    for k,v in i.iteritems():
        if k == 'bill_id':
            logging.info('bill_id: %s', v)
            bid = v,
        elif k == 'cosponsor_ids':
            logging.info('cosponsor_ids LIST: %s', v)
            for cid in v:
                logging.info('cosponsor_ids ITEM: %s', cid)
                cid_list += cid,
        elif k == 'urls':
            logging.info('url: %s', v)
            url = v['congress'],
        elif k == 'sponsor_id':
            logging.info('sponsor_id: %s', v)
            sid = v,
        elif k == 'official_title':
            logging.info('official_title: %s', v)
            ot = v,
        else:
            logging.warning('unknown key %s', k)        
        
    bills_insert_values = (bid + ot + sid + url)
    logging.info('in 1: %s', bills_insert_values)
    c.execute(bills_insert_query, bills_insert_values)

    for cd in cid_list:
        cosponsors_bills_insert_values = (ai + tuple([cd]) + bid)
        logging.info('in 2: %s', cosponsors_bills_insert_values)
        c.execute(cosponsors_bills_insert_query, cosponsors_bills_insert_values)
    
    logging.info('[OK]\n\n')

db.commit()
db.close()
