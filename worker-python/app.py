#!/usr/bin/env python3

from redis import Redis
import os
import time
import psycopg2

def get_redis():
   redis_conn = Redis(host="redis", db=0, socket_timeout=5, password=os.getenv('redispasswd', "password"))
   return redis_conn

def connect_postgres(): 
   # Vva1VrSRCqqJnYKH
   dbp=os.getenv('dbpasswd') 
   host=os.getenv('POSTGRES_SERVICE_HOST') 
   print dbp 
   try:
      #conn = psycopg2.connect("host=db user=postgres password=dbp host=172.30.114.217")
      conn = psycopg2.connect ("host={} db={} user={} password={}".format(host, "db", "postgres", dbp) )
      print("Successfully connected to PostGres")
   except Exception as e:
      print (e)

def process_votes():
    while True: 
       try:  
          redis = get_redis()
          msg = redis.rpop("votes")
          print(msg)
          # will look like this
          # {"vote": "a", "voter_id": "71f0caa7172a84eb"}
          time.sleep(10)        
   
       except Exception as e:
          print(e)


if __name__ == '__main__':
    connect_postgres()
    process_votes()


