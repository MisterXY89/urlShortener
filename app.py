
import os
import time
import random
import sqlite3
from hashlib import sha256
from flask import Flask, redirect, url_for, render_template, request

app = Flask("urlShortener")

# disable caching
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

# YOUR TIMEZONE
os.environ["TZ"] = "Europe/Berlin"
time.tzset()

# HOSTNAME, here let's say it is short.io / localhost:500 for dev
BASE_URL = "short.io"

# URL_DB FILENAME
DB_FILE = "urls.db"


def randomInterval():
    start = random.randint(0, 150)
    end = start + 7
    return {"start": start, "end": end}


def create_connection():
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
    except Exception as e:
        print(e)
    return conn


def updateUrlDb(urlDict):
    conn = create_connection()
    sql = f"INSERT INTO urls(shortUrl,longUrl,hash, created) VALUES('{urlDict['shortUrl']}','{urlDict['longUrl']}','{urlDict['hash']}','{urlDict['time']}')"
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return cur.lastrowid


def readLongUrl(hash):
    conn = create_connection()
    sql = f"SELECT longUrl from urls WHERE hash LIKE '{hash}'"
    cur = conn.cursor()
    cur.execute(sql)
    res = cur.fetchall()
    conn.commit()
    try:
        longUrl = res[0]
        longUrl = str(longUrl[0])
    except Exception as e:
        longUrl = "localhost:5000"
    finally:
        return longUrl


@app.route('/<string:hash>/')
def redirectToUrl(hash):
    longUrl = readLongUrl(hash)
    return redirect(longUrl, code=302)


@app.route("/a/result")
def result():
    if "longUrl" in request.args and "shortUrl" in request.args:
        longUrl = request.args["longUrl"]
        shortUrl = request.args["shortUrl"]
        return render_template("result.html", shortUrl = shortUrl, longUrl = longUrl)
    return redirect(url_for("index"))


@app.route("/a/shorten", methods=["POST"])
def shorten():
    url = request.form["longUrl"]
    urlHash = sha256((url+str(time.time())).encode('utf-8')).hexdigest()
    interval = randomInterval()
    shortUrlHash = urlHash[interval["start"]:interval["end"]]

    # TODO: escape url!!
    shortUrl = BASE_URL + "/" + shortUrlHash

    urlDict = {
        "shortUrl": shortUrl,
        "longUrl": url,
        "time": str(time.time()),
        "hash": shortUrlHash
    }
    res = updateUrlDb(urlDict)
    print(res)
    return redirect(url_for("result", shortUrl = shortUrl, longUrl = url))


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
