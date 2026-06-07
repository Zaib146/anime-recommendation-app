# this file handles the backend setup

from fastapi import FastAPI     # needed for backend setup
from phase1_script import get_recommendation
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
    similar_anime: list

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
    return get_recommendation(anime_name)


# to start / host the backend server (make it alive), type this in "Terminal" -> "New Terminal". should be in location C:\anime-recommendation-app\backend>
# uvicorn main:app --reload.    This follows structure of "uvicorn filename:app_object --reload".  here, --reload automatically restarts the server when I make code changes
# to visit, type this url "localhost:8000/recommendations/{anime_name}", but actually insert a real anime name into the variable.
# or this: "http://127.0.0.1:8000/recommendations/naruto". Can copy the link showed at beginning of terminal, then add the search endpoint and query myself. endpoint is recommendation, query is naruto

# this function saves anime to a watchlist
@app.post("/watchlist")
def watchlist_endpoint(anime: Anime):   # anime: Anime - this says that the parameter anime is of type Anime, which is an object - it's an instance of Anime Pydantic model
    # this endpoint receives an anime object
    
    genres_text = json.dumps(anime.genres)      # turns Python list of genres into JSON string - needed since SQLite cannot store a list, it can only store a string value
    similar_anime_text = json.dumps(anime.similar_anime)    # same idea as genres_text
    
    conn = sqlite3.connect("anime_app.db")      # here anime_app.db already exists, so it'll just reopen the existing database created when database_setup.py first ran
                                                        # conn is now the open connection to my database. we use conn later to refer to that same database connection. conn is an open database file
                                                        
    cursor = conn.cursor()  # .cursor() is asking the conn connection to "Give me a cursor so I can send commands to the database". 
                            # that cursor is then stored in the variable cursor, since we'll use it repeatedly
    
    # .execute says to run the SQL command inside the (). The code in () is a SQL command, but it's inside """, so that makes the command a Python string, since it's a python file. SQLite can only understand SQL commands, not Python code.
    # cursor.execute() then sends the SQL command (inside a Python string), to SQLite  
    
    try:  
        cursor.execute("""
        -- SQL command inside a Python string here.
        -- this INSERT INTO statement means these are the 6 columns I'll be filling with values
        INSERT INTO watchlist (
            anime_id,
            title,
            image_url,
            synopsis,
            genres,
            similar_anime
        )
        
        -- We use "?" as placeholder values, since Naruto values will be different Bleach, etc
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        
        # these are the actual values that will fill in the placeholder ?. This is a tuple. Python provides these values, SQLite combines them with the placeholder values
        (
            anime.anime_id,
            anime.title,
            anime.image_url,
            anime.synopsis,
            genres_text,
            similar_anime_text
        )
        )
    
        conn.commit()       # commit() tells SQLite to save those changes permanently
        
        return {"message": "Anime saved to watchlist"}
    
    except sqlite3.IntegrityError:      # Prevents saving duplicate anime. prevents multiple anime with the same title (therefore have the same anime_id) to be entered in the table. 
        # sqlite3.IntegrityError - "The database refused the operation because it would violate one of the table's rules (constraints)." Here SQLite raises this error because the UNIQUE constraint in anime_id INTEGER UNIQUE 
        # would be violated
        return {"message": "Anime already in watchlist"}
    
    finally:
        conn.close()    # this will run no matter what. done using the database, close the connection. Like closing a file after saving it