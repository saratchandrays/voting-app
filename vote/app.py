from flask import Flask, render_template, request, make_response, g
from redis import Redis
import os
import socket
import random
import json

option_a = os.getenv('OPTION_A', "Python")
option_b = os.getenv('OPTION_B', "Node.js")
hostname = socket.gethostname()

# may have to have env variable for Z

app = Flask(__name__)

def get_redis():
    if (os.getenv('OS_ENV') == "Z"):
       print ("Connecting to Redis using Z connection string")
       redis_conn = Redis(host="new-redis", db=0, socket_timeout=5)  # on Z 
    else: 
       print ("Connecting to Redis using x86 connection string")
       redis_conn = Redis(host="new-redis", db=0, socket_timeout=5)
       print ("Connected to Redis") 
       #redis_conn = Redis(host="new-redis", db=0, socket_timeout=5, password=os.getenv('redispasswd', "password"))
    return redis_conn

@app.route("/", methods=['POST','GET'])
def hello():
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    vote = None

    if request.method == 'POST':
        redis = get_redis()
        vote = request.form['vote']
        data = json.dumps({'voter_id': voter_id, 'vote': vote})
        redis.rpush('votes', data)

    resp = make_response(render_template(
        'index.html',
        option_a=option_a,
        option_b=option_b,
        hostname=hostname,
        vote=vote,
    ))
    resp.set_cookie('voter_id', voter_id)
    return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
