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

class Anime(BaseModel):     # class Anime inherits from Base Model. Like how class Cat extends Animal in Java
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


