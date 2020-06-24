# Basic Python Flask Url Shorten Service

This little project was a challenge to be completed in under one hour. Hence there may be a few flaws here and there. See the Security and Validation Notice.

## Service
For every long URL (and the `time.time()` value) a SHA-256 hash is generated.
A random part of the hash is then used to represent the long URL.

Let's look at an example, we have a long url: `https://github.com/MisterXY89`. The app gives us
`short.io/b61982` (Notice that `short.io` is an example `BASE_URL`). The app then looks up the
hash code `b61982` in the DB and returns the long URL `https://github.com/MisterXY89`

## Security & Validation Notice
At the moment the URL input gets not validated and no escaped! Keep that in mind when using.

Furthermore no extra precautions for security have been taken.


## UI
The user interface is very basic since this was created with a time limit. I used the CSS framework [Beauter](beauter.outboxcraft.com/).

## Database
This implementation uses a sqlite3 database, if you want to create the table yourself, here is the SQL statement:

```sql
CREATE TABLE "urls" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"shortUrl"	TEXT NOT NULL DEFAULT '<<CUSTOM DEFAULT>>',
	"longUrl"	TEXT NOT NULL,
	"hash"	TEXT NOT NULL UNIQUE,
	"created"	TEXT NOT NULL
)
```
## Run it on your machine
In `app.py` you have to configure some options:
```python
# YOUR TIMEZONE
os.environ["TZ"] = "Europe/Berlin"
time.tzset()

# HOSTNAME, here let's say it is short.io / localhost:500 for dev
BASE_URL = "short.io"

# URL_DB FILENAME
DB_FILE = "urls.db"
```
Make sure you created the DB, close the connection from the editor and install the requirements.

Then you can simply run the application via: `flask run` or `python3 app.py`.
