#!/usr/bin/env python3

from redis import Redis
import os
import time
import psycopg2

def get_redis():
   redis_conn = Redis(host="redis", db=0, socket_timeout=5)
   print ("connected to redis!") 
   return redis_conn

def connect_postgres(): 
   # Vva1VrSRCqqJnYKH
   dbp=os.getenv('dbpasswd') 
   host=os.getenv('POSTGRES_SERVICE_HOST') 
   print (dbp) 
   try:
      print ("connecting to the DB") 
      #conn = psycopg2.connect("host=db user=postgres password=dbp host=172.30.114.217")
      conn = psycopg2.connect ("host={} dbname={} user={} password={}".format("sample-app", "postgres", "dave", "dave") )
      print("Successfully connected to PostGres")
      
      cursor = conn.cursor()
      sqlCreateTable = "CREATE TABLE IF NOT EXISTS votes (id VARCHAR(255) NOT NULL UNIQUE, vote VARCHAR(255) NOT NULL);"
      cursor.execute(sqlCreateTable)
      print ("votes table created") 

   except Exception as e:
      print (e)

def process_votes():
    redis = get_redis() 
    while True: 
       try:  
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


