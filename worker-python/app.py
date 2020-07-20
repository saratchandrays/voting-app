#!/usr/bin/env python3

from redis import Redis
import os

def get_redis():
    redis_conn = Redis(host="redis", db=0, socket_timeout=5, password=os.getenv('redispasswd', "password"))
    return redis_conn


def process_votes():
    while True: 
       try:  
          redis = get_redis()
          msg = redis.rpop("votes")
          print(msg)
          sleep(10)        
   
       except Exception as e:
          print(e)


if __name__ == '__main__':
    process_votes()