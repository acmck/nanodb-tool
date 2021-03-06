#!/usr/bin/python

import lmdb
import argparse
import sys
import os

lmdb_datadir = "Raiblocks"
lmdb_dbfile = "data.ldb"

def db_list():
   global db
   open_env()
   main_db = env.open_db(txn=txn)
   main_curs = txn.cursor(main_db)
   db = []
   for k, v in main_curs:
        db.append(k)
   return db

def open_env():
   global env,txn
   env = lmdb.open(env_path, subdir=False, readonly=True, max_dbs=128)
   txn = env.begin(buffers=True)

def values_dump(db):
   curr_db = env.open_db(key=db, txn=txn)
   cursor = txn.cursor(curr_db)
   if int(txn.stat(curr_db).values()[5]) >= 1:
      with open('{}.vals'.format(db), 'w') as outfile:
         for k,v in cursor:
            outfile.write('{0!s},{1!s}\n'.format(k[:].encode('hex'),v[:].encode('hex')))

def make_argparser():
   global args
   parser = argparse.ArgumentParser(description='Nano LMDB tool.')
   parser._action_groups.pop()
   optional = parser._action_groups.pop()
   required = parser.add_argument_group('required arguments')
   required.add_argument('-e','--env', help='Directory containing ldb file.')
   optional.add_argument('-r','--records', help='Dump number of records/entries.',action='store_true', default=False )
   optional.add_argument('-l','--list', help='Lists databases in lmdb env.',action='store_true', default=False)
   optional.add_argument('-v','--values', help='Dumps k:v (hex encoded) from all dbs',action='store_true', default=False)
   optional.add_argument('-d','--decode', help='Dumps decoded values for supported dbs.',action='store_true', default=False)
   parser._action_groups.append(optional)
   args = parser.parse_args()
   return args

def decode_send():
   print 'I would run decode_send()'

def decode_open():
   # all open blocks 	= 200b
   # Output: k[hash(32b)],v[previous(32b), rep(32b), source(32b), sig(64b), work(8b), next(32b)]
   curr_db = env.open_db(key='open', txn=txn)
   cursor = txn.cursor(curr_db)
   print 'Exporting {!s} records to open.csv'.format(txn.stat(curr_db).values()[5])
   with open('open.csv', 'w') as outfile:
      for k,v in cursor:
         work = bytearray(v[160:168])
         work.reverse()
         outfile.write('{0!s},{1!s},{2!s},{3!s},{4!s},{5!s},{6!s}\n'.format(k[:].encode('hex'),v[0:32].encode('hex'),v[32:64].encode('hex'),v[64:96].encode('hex'),v[96:160].encode('hex'),str(work).encode('hex'),v[168:200].encode('hex')))

def decode_change():
   # all change blocks = 168b
   # Output: hash(32b) = [previous(32b), acc(32b), sig(64b), work(8b), next(32b)]
   curr_db = env.open_db(key='change', txn=txn)
   cursor = txn.cursor(curr_db)
   print 'Exporting {!s} records to change.csv'.format(txn.stat(curr_db).values()[5])
   with open('change.csv', 'w') as outfile:
      for k,v in cursor:
      # flip endian for 'work'
         work = bytearray(v[128:136])
         work.reverse()
         outfile.write('{0!s},{1!s},{2!s},{3!s},{4!s},{5!s}\n'.format(k[:].encode('hex'),v[0:32].encode('hex'),v[32:64].encode('hex'),v[64:128].encode('hex'),str(work).encode('hex'),v[136:].encode('hex')))

def decode_receive():
   print 'I would run decode_receive()'

args = make_argparser()

if not args:
   sys.stderr.write('nanodb-tool: Please specify a command (see --help)\n')
   raise SystemExit(1)
if args.env:
   env_path = os.path.join(args.env, lmdb_dbfile)
else:
   env_path = os.path.join(os.environ['HOME'], lmdb_datadir, lmdb_dbfile) 

if args.records is True:
   open_env()
   for db in db_list():
      cur_db = env.open_db(key=db, txn=txn)
      print '{0},{1}'.format(db, str(txn.stat(cur_db).values()[5]))

if args.list is True:
   open_env()
   for db in db_list():
      print db

if args.values is True:
   open_env()
   for db in db_list():
      values_dump(db)

if args.decode is True:
   supported_dbs = ['open','change']
   open_env()
   for db in db_list():
      if str(db) in supported_dbs:
         decoder = globals().get('decode_'+str(db))
         decoder()
      else:
         continue
