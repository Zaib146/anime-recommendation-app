import sqlite3  # Python can now talk to SQLite

conn = sqlite3.connect("anime_app.db")      # conn is now the open connection to my database. we use conn later to refer to that same database connection. 
                                            # conn is an open database file. sqlite3.connect("anime_app.db") checks if the file "anime_app.db" exists.
                                            # if it does not, it then creates it (so I do not need to manually create it)

cursor = conn.cursor()      # .cursor() is asking the conn connection to "Give me a cursor so I can send commands to the database". 
                            # that cursor is then stored in the variable cursor, since we'll use it repeatedly
                            
cursor.execute("""
                CREATE TABLE IF NOT EXISTS watchlist (
                    id INTEGER PRIMARY KEY,
                    anime_id INTEGER UNIQUE,
                    title TEXT,
                    image_url TEXT,
                    synopsis TEXT,
                    genres TEXT,
                    similar_anime TEXT
                )
               """
               )