import sqlite3  # Python can now talk to SQLite

conn = sqlite3.connect("anime_app.db")      # conn is now the open connection to my database. we use conn later to refer to that same database connection. 
                                            # conn is an open database file. sqlite3.connect("anime_app.db") checks if the file "anime_app.db" exists.
                                            # if it does not, it then creates it (so I do not need to manually create it)

cursor = conn.cursor()      # .cursor() is asking the conn connection to "Give me a cursor so I can send commands to the database". 
                            # that cursor is then stored in the variable cursor, since we'll use it repeatedly
                            
# .execute says to run the SQL command inside the (). The code in () is a SQL command, but it's inside """, so that makes the command a Python string, since it's a python file. SQLite can only understand SQL commands, not Python code.
# cursor.execute() then sends the SQL command (inside a Python string), to SQLite   
# execute() tells SQLite what changes you want                         
cursor.execute("""     
                CREATE TABLE IF NOT EXISTS watchlist ( 
                    -- IF NOT EXISTS avoid create duplicate tables. Create a table named "watchlist" if it does not yet exist
                    -- id is column name, INTEGER is data type, PRIMARY KEY uniquely identifies each row (actual values stored in this column). SQLite uses this as the rows identity. Row ids do not repeat 
                    id INTEGER PRIMARY KEY, 
                    
                    -- anime_id = Jikan mal_id, UNIQUE mean no duplicate values allowed. Prevents user from saving Naruto (example) multiple times
                    anime_id INTEGER UNIQUE,
                    
                    -- column name, saved as text
                    title TEXT,
                    
                    image_url TEXT,
                    
                    synopsis TEXT,
                    
                    -- actual data for genres is a Python list, but later we'll convert it to text and store it as text. Since SQLite does not understand Python lists
                    genres TEXT,
                    
                    -- same idea with genres, it's actually a Python list originally
                    similar_anime TEXT,
                    
                    -- records which live API the recommendation results came from
                    recommendation_source TEXT
                )
               """
               )

cursor.execute("""     
                CREATE TABLE IF NOT EXISTS anime_cache ( 
                    -- IF NOT EXISTS avoid create duplicate tables. Create a table named "anime_cache" if it does not yet exist
                    -- id is column name, INTEGER is data type, PRIMARY KEY uniquely identifies each row (actual values stored in this column). SQLite uses this as the rows identity. Row ids do not repeat 
                    id INTEGER PRIMARY KEY, 
                    
                    -- anime_id = Jikan mal_id, UNIQUE mean no duplicate values allowed. Prevents user from saving Naruto (example) multiple times
                    anime_id INTEGER UNIQUE,
                    
                    -- column name, saved as text
                    title TEXT,
                    
                    image_url TEXT,
                    
                    synopsis TEXT,
                    
                    -- actual data for genres is a Python list, but later we'll convert it to text and store it as text. Since SQLite does not understand Python lists
                    genres TEXT,
                    
                    -- same idea with genres, it's actually a Python list originally
                    similar_anime TEXT,
                    
                    -- see when this entry was added to the cache table
                    fetched_at TEXT,
                    
                    -- records which live API the recommendation results came from
                    recommendation_source TEXT,
                    
                    -- records which live API the similar anime results came from
                    similar_anime_source TEXT
                )
               """
               )

# watchlist table

# ┌───────────────────────────────────────┐
# │ id            INTEGER PRIMARY KEY     │
# │ anime_id      INTEGER UNIQUE          │
# │ title         TEXT                    │
# │ image_url     TEXT                    │
# │ synopsis      TEXT                    │
# │ genres        TEXT                    │
# │ similar_anime TEXT                    │
# └───────────────────────────────────────┘

# This shows what is a column and what's a row. id, anime_id, title, image_url, synopsis, genres, similar_anime are all columns in the watchlist table. Rows are the actual records stored in the table
# Each row shows all the information for that specific anime
# | id | anime_id | title           |
# | -- | -------- | --------------- |
# | 1  | 20       | Naruto          |
# | 2  | 21       | One Piece       |
# | 3  | 16498    | Attack on Titan |

conn.commit()       # commit() tells SQLite to save those changes permanently
conn.close()        # done using the database, close the connection. Like closing a file after saving it
