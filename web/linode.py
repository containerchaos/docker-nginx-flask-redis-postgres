from flask import Flask, jsonify
import logging
import psycopg2
import redis
import sys

app = Flask(__name__)
cache = redis.StrictRedis(host='redis', port=6379)

# Configure Logging
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)

def PgFetch(query, method):

    # Connect to an existing database
    conn = psycopg2.connect("host='postgres' dbname='linode' user='postgres' password='linode123'")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Query the database and obtain data as Python objects
    dbquery = cur.execute(query)

    if method == 'GET':
        result = cur.fetchone()
    else:
        result = ""

    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()
    return result

@app.route('/')
def hello_world():
    return jsonify(1)

@app.route('/resetcounter')
def resetcounter():
    cache.delete('visitor_count')
    PgFetch("UPDATE visitors set visitor_count = 0 where site_id = 1;", "POST")
    app.logger.debug("reset visitor count")
    return "Successfully deleted redis and postgres counters"
