import sqlite3  # Python can now talk to SQLite

conn = sqlite3.connect("anime_app.db")      # conn is now the open connection to my database. we use conn later to refer to that same database connection