# this file handles the backend setup

from fastapi import FastAPI     # needed for backend setup
from phase1_script import get_recommendation, get_genre_recommendations
from fastapi.middleware.cors import CORSMiddleware  # Go into FastAPI's CORS module and import the tool that handles cross-origin requests. importing a security guard
# the middleware decides allow or block
from pydantic import BaseModel
#   BaseModel = a class that knows how to:
# - validate data
# - convert JSON into Python objects
# - generate API documentation
# - enforce data types

# Suppose React sends:

# {
#   "anime_id": 20,
#   "title": "Naruto"
# }

# FastAPI can automatically create:

# anime = Anime(
#     anime_id=20,
#     title="Naruto"
# )
from datetime import datetime   # needed to get the correct date and time for fetched_at for the caching functions
import json     # gives us access to JSON functions
import sqlite3  # Python can now talk to SQLite

# BaseModel = Pydantic's class, Anime = my custom Pydantic model
class Anime(BaseModel):     # class Anime inherits all the functionality from Pydantic's Base Model. Like how class Cat extends Animal in Java
    # this does not save anything yet. this tells FastAPI that when someone send anime data to my backend, this is the shape I expect, the object.
    # this gives me a clean anime object that i can then INSERT INTO watchlist table (inside my post function)
    anime_id: int       # must be a number
    title: str          # must be a text
    image_url: str
    synopsis: str
    genres: list        # must be a list
    
class RecommendationResponse(BaseModel):    # instead of just one result of a list of anime for recommendations, now returning an object. 
    result_source: str      # clarify if data came from Jikan or cache
    message: str        # I can give a message saying cache was used, or empty str if not
    results: list[Anime]    # a list of Anime objects. This is the newer python convention using the built in generic for list instead List and needing an import. other way is List<Anime> with an import.

# create app object
# this creates my backend server, we're creating an application object here. This "app" becomes my server, my API, my backend. Everything attaches to this object
app = FastAPI()

app.add_middleware( # Hey FastAPI, before any requests reach my routes, run them through the CORS security guard.

    CORSMiddleware,
    allow_origins = ["http://localhost:5173"],  # only allow requests from here
    allow_credentials = True,   # allows credentials (login information) if I ever need it
    allow_methods = ["*"],      # allows all request types - get, post, put, delete - this is needed since I use @app.get
    allow_headers = ["*"]       # allows all headers - header is extra information attached to a request
)


def delete_expired_cache():
    conn = sqlite3.connect("backend/anime_app.db")
    cursor = conn.cursor()
    
    cursor.execute("""     
                -- this deletes all the anime in anime_cache that were added more than 30 days. datetime('now', '-30 days') is the current dattime - 30 days. For example, July 1st is today, so the cutoff becomes June 1st.
                -- if fetched_at < June 1st (for example, May 28), it's older than 30 days, since it's less than the cutoff. so it's deleted.   
                DELETE FROM anime_cache 
                WHERE fetched_at < datetime('now', '-30 days')
               """
               )
    conn.commit()
    conn.close()
    
    
def save_to_cache(results):
    fetched_at = datetime.now().isoformat()     # datetime.now() creates a datetime object representing current day and time. isoformat() converts the object into a string. 
    # for example, the object can become 2026-07-01T18:42:15.123456 with the format of YYYY-MM-DDTHH:MM:SS.microseconds
    
    genres_text = json.dumps(results.genres)
    similar_anime_text = json.dumps(results.similar_anime)
    
    conn = sqlite3.connect("backend/anime_app.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        -- SQL command inside a Python string here.
        -- this INSERT INTO statement means these are the 6 columns I'll be filling with values
        -- will insert the values in the tuple into the table "anime_cache"
        INSERT INTO anime_cache (
            anime_id,
            title,
            image_url,
            synopsis,
            genres,
            similar_anime,
            fetched_at
        )
        
        -- We use "?" as placeholder values, since Naruto values will be different than Bleach, etc
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        
        # these are the actual values that will fill in the placeholder ?. This is a tuple. Python provides these values, SQLite combines them with the placeholder values
        (
            results.anime_id,
            results.title,
            results.image_url,
            results.synopsis,
            genres_text,
            similar_anime_text,
            fetched_at
        )
        )
    conn.commit()
    conn.close()

    
def limit_cache_size():
    conn = sqlite3.connect("backend/anime_app.db")
    cursor = conn.cursor()
    
    cursor.execute("""       
                -- deletes all anime saved in cache that are more than 500 entries (entries 501 onwards). it checks if the anime_id is NOT IN the top 500 entries 
                -- ORDER BY fetched_at DESC - anime_id sorted in descending order by their date time, recorded by their fetched_at values. LIMIT 500 then limits it to the first 500. So any anime_id not in that list of top 500 is deleted
                DELETE FROM anime_cache 
                WHERE anime_id NOT IN (
                    SELECT anime_id
                    FROM anime_cache
                    ORDER BY fetched_at DESC
                    LIMIT 500
                )
               """
               )
    conn.commit()
    conn.close()
    
def get_cached_results(anime_name):
    conn = sqlite3.connect("backend/anime_app.db")
    cursor = conn.cursor()
    
    cursor.execute("""
                -- SELECT * means select all the columns. So it returns anime_id, title, image_url, etc. it only selects the entries whose title is equal to the parameter, we use ? as a placeholder here          
                SELECT * 
                FROM anime_cache
                WHERE title LIKE ? 
                """,
                # comma is needed after anime_name to make sure it's a tuple - when entering multiple values, don't need to explicitly do it since it can tell
                # before it was (anime_name,). but if it's "naruto", results with "Naruto" will not show. This format with % means anything that contains the text "naruto" - can be "Naruto: Last generations", "naruto: shippuden", etc. 
                # for that reason we use LIKE instead of = for the syntax above
                f"%{anime_name}%", 
               )
    
    conn.close()


# if this url is called, run the get_recommendation function
# this says to associate this url with this function called recommendations_endpoint
# we created a separate function called recommendations_endpoint so we can use the get_recommendations function for other urls in the future
# recommendations_endpoint handles the web / API side

# static route: /recommendations/
# dynamic variable: anime_name
# this url is completely of my own making. I wrote it this way to make the most sense
# FastAPI will automatically convert the python list returned into JSON. good for frontend later
# @app.get attaches a route to the app object
# the full @app.get line is a decorator

@app.get("/recommendations/{anime_name}")
def recommendations_endpoint(anime_name):
    # call delete_expired_cache function first
    delete_expired_cache()
    
    try:
        results = get_recommendation(anime_name)
        save_to_cache(results)
        limit_cache_size()
        
        return results
    
    except:
        return get_cached_results(anime_name)
    

@app.get("/similar-anime/{genre_ids}")      # for example, receives a string like "1,2,10"
def similarAnime_endpoint(genre_ids):
    genre_ids = genre_ids.split(",")        # changes genre_ids to now a list of ["1", "2", "10"]   this is needed since get_genre_recommendations needs a list as a parameter
    return get_genre_recommendations(genre_ids)


# to start / host the backend server (make it alive), type this in "Terminal" -> "New Terminal". should be in location C:\anime-recommendation-app\backend>
# uvicorn main:app --reload.    This follows structure of "uvicorn filename:app_object --reload".  here, --reload automatically restarts the server when I make code changes
# to visit, type this url "localhost:8000/recommendations/{anime_name}", but actually insert a real anime name into the variable.
# or this: "http://127.0.0.1:8000/recommendations/naruto". Can copy the link showed at beginning of terminal, then add the search endpoint and query myself. endpoint is recommendation, query is naruto

# this function saves anime to a watchlist
@app.post("/watchlist")
def watchlist_endpoint(anime: Anime):   # anime: Anime - this says that the parameter anime is of type Anime, which is an object - it's an instance of Anime Pydantic model
    # this endpoint receives an anime object
    
    genres_text = json.dumps(anime.genres)      # turns Python list of genres into JSON string - needed since SQLite cannot store a list, it can only store a string value
    
    conn = sqlite3.connect("backend/anime_app.db")      # here anime_app.db already exists, so it'll just reopen the existing database created when database_setup.py first ran
                                                        # conn is now the open connection to my database. we use conn later to refer to that same database connection. conn is an open database file, a connection object
                                                        
    cursor = conn.cursor()  # .cursor() is asking the conn connection to "Give me a cursor so I can send commands to the database". .cursor() is a method from sqlite3, called on conn
                            # that cursor is then stored in the variable cursor, since we'll use it repeatedly
    
    # .execute says to run the SQL command inside the (). The code in () is a SQL command, but it's inside """, so that makes the command a Python string, since it's a python file. SQLite can only understand SQL commands, not Python code.
    # cursor.execute() then sends the SQL command (inside a Python string), to SQLite  
    # database works
    try:  
        cursor.execute("""
        -- SQL command inside a Python string here.
        -- this INSERT INTO statement means these are the 6 columns I'll be filling with values
        -- will insert the values in the tuple into the table "watchlist"
        INSERT INTO watchlist (
            anime_id,
            title,
            image_url,
            synopsis,
            genres
        )
        
        -- We use "?" as placeholder values, since Naruto values will be different than Bleach, etc
        VALUES (?, ?, ?, ?, ?)
        """,
        
        # these are the actual values that will fill in the placeholder ?. This is a tuple. Python provides these values, SQLite combines them with the placeholder values
        (
            anime.anime_id,
            anime.title,
            anime.image_url,
            anime.synopsis,
            genres_text,
        )
        )
    
        conn.commit()       # commit() tells SQLite to save those changes permanently
        
        return {"message": "Anime saved to watchlist"}
    
    except sqlite3.IntegrityError:      # Prevents saving duplicate anime. prevents multiple anime with the same title (therefore have the same anime_id) to be entered in the table. 
        # sqlite3.IntegrityError - "The database refused the operation because it would violate one of the table's rules (constraints)." Here SQLite raises this error because of the UNIQUE constraint in anime_id INTEGER UNIQUE 
        # would be violated
        return {"message": "Anime already in watchlist"}
    
    finally:
        conn.close()    # this will run no matter what. done using the database, close the connection. Like closing a file after saving it

# this function is to read from the watchlist      
@app.get("/watchlist")
def watchlist2_endpoint():
    conn = sqlite3.connect("anime_app.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    -- selecting which columns from the table to read, must type each individually
    SELECT anime_id, title, image_url, synopsis, genres
    FROM watchlist 
                   """)
    # conn.commit() not needed here - no changes to database made. still want conn.close() later
    rows = cursor.fetchall()    # put all the rows returned by the select query into the python variable "rows" as a list - list with rows as tuples
    # with a small watchlist, this is fine. With large watchlists with tons of users, set limits (top 20 first), then they can click "Show More", see next 20, etc. For later.
    
    # print(type(rows[0])) - each row is a tuple. need to convert each row into a dictionary, since react works better with dictionaries.
    # this is an example of each row inside the variable "rows"
    # [
    # (16870, "The Last: Naruto the Movie", ...),
    # (28755, "Boruto: Naruto the Movie", ...),
    # (20, "Naruto", ...)
    # ]
    
    saved_anime = []
    for row in rows:
        item = {"anime_id": row[0], "title": row[1], "genres": json.loads(row[4]), "synopsis": row[3], "images": row[2]}
        # use indices since tuples require indices, they don't use key and value
        # genres and similar_anime are still JSON strings from database, so we'll need to do json.loads() on them before returning them
        
        saved_anime.append(item)    # create a new dictionary from each row, save to saved_anime list
    
    conn.close()    # close the database connection, must do before returning
    
    return saved_anime      # list with rows as dictionaries, so FastAPI converts the Python dictionaries into JSON

@app.delete("/watchlist/{anime_id}")
def watchlist3_endpoint(anime_id):
    conn = sqlite3.connect("anime_app.db")
    cursor = conn.cursor()
    
    cursor.execute (""" 
    DELETE FROM watchlist WHERE anime_id = ? """, (anime_id,))      # this specifies which row (which anime_id) we'll be deleting from the watchtable. allows us to delete specific anime for watchlist
    # we do (anime_id,) as a parameter, like we did with the INSERT INTO. Except here, since we have one value of anime_id, we write it as "anime_id,". The comma at the end tells SQLite this is a tuple, NOT an integer.
    # the parameter must be a tuple. in INSERT INTO, we had 6 values inside (), so that was clearly a tuple, so no comma needed at the end
    
    conn.commit()
    conn.close()
    
    return {"message": "Anime removed from watchlist"}