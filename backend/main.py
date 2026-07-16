# this file handles the backend setup

from fastapi import FastAPI     # needed for backend setup
from phase1_script import get_recommendation, get_similar_anime
from fastapi.middleware.cors import CORSMiddleware  # Go into FastAPI's CORS module and import the tool that handles cross-origin requests. importing a security guard
# the middleware decides allow or block
from pydantic import BaseModel
#   BaseModel = a class that knows how to:
# - validate data
# - convert JSON into Python objects
# - generate API documentation
# - enforce data types


from datetime import datetime   # needed to get the correct date and time for fetched_at for the caching functions
import json     # gives us access to JSON functions
import sqlite3  # Python can now talk to SQLite

# BaseModel = Pydantic's class, Anime = my custom Pydantic model

# For class Anime
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

class Anime(BaseModel):     # class Anime inherits all the functionality from Pydantic's Base Model. Like how class Cat extends Animal in Java
    # this does not save anything yet. this tells FastAPI that when someone send anime data to my backend, this is the shape I expect, the object.
    # this gives me a clean anime object that i can then INSERT INTO watchlist table (inside my post function)
    anime_id: int       # must be a number
    title: str          # must be a text
    image_url: str
    synopsis: str
    genres: list        # must be a list
    recommendation_source: str | None = None    # The first None belongs to the type (str | None). The second None is the default value (= None). just syntax, the = None is an optional string field
    
    
# For class SimilarAnimeRequst
# Suppose React sends:

# {
#     "anime_id":20,

#     "genres":[
#         {
#             "name":"Action",
#             "jikan_id":1
#         }
#     ]
# }

# FastAPI can automatically create:
# request = SimilarAnimeRequest(
#     anime_id=20,

#     genres=[
#         {
#             "name":"Action",
#             "jikan_id":1
#         }
#     ]
# )

# class SimilarAnimeRequest inherits all the functionality from Pydantic's Base Model. Like how class Cat extends Animal in Java
# this does not save anything yet. this is the shape I expect, the object.
class SimilarAnimeRequest(BaseModel):
    anime_id: int
    genres: list

# get a structured returned object from similar anime endpoint, like we did with RecommendationResponse in get recommendations endpoint    
class SimilarAnimeResponse(BaseModel):
    result_source: str
    similar_anime_source: str | None = None
    message: str
    results: list[str]
    
# class RecommendationResponse inherits all the functionality from Pydantic's Base Model. Like how class Cat extends Animal in Java
# this does not save anything yet this is the shape I expect, the object.
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
    conn = sqlite3.connect("anime_app.db")
    cursor = conn.cursor()
    
    cursor.execute("""     
                -- this deletes all the anime in anime_cache that were added more than 30 days. datetime('now', '-30 days') is the current dattime - 30 days. For example, July 1st is today, so the cutoff becomes June 1st.
                -- if fetched_at < June 1st (for example, May 28), it's older than 30 days. Since it's less than the cutoff, it's deleted.   
                DELETE FROM anime_cache 
                WHERE fetched_at < datetime('now', '-30 days')
               """
               )
    conn.commit()
    conn.close()
    
    
def save_to_cache(results):
    fetched_at = datetime.now().isoformat()     # datetime.now() creates a datetime object representing current day and time. isoformat() converts the object into a string. 
    # for example, the object can become 2026-07-01T18:42:15.123456 with the format of YYYY-MM-DDTHH:MM:SS.microseconds
    
    conn = sqlite3.connect("anime_app.db")
    cursor = conn.cursor()
    
    # results is a list of dictionaries, each dictionary containing information about a specific anime. So we need to loop through results and add each anime dictionary in their individually into the anime_cache table. We do a cursor.execute for every anime dictionary
    # before was getting an error when I did one cursor.execute on results, and tried to insert results.anime_id. that does not exist, since a list object does not have anime_id attribute. the dictionaries inside it do. so I put the code inside this loop
    for anime in results:
        recommendation_source = anime["recommendation_source"]
        genres_text = json.dumps(anime["genres"])
        similar_anime_text = json.dumps([])
        
        # this cursor.execute() checks if this specific anime_id already exists in the anime_cache table
        cursor.execute("""
                       SELECT anime_id
                       FROM anime_cache
                       WHERE anime_id = ?
                       """,
                       (anime["anime_id"],)
                       )
        # if the id does exist (for example, let's say anime_id for Naruto is 20), existing_row = (20,) , existing_row = a tuple containing the matching row. if the anime_id does not exist, existing_row = None
        # fetchone() says give me the first row returned by that SELECT. The SELECT either finds the row, or finds nothing
        existing_row = cursor.fetchone()
        
        # if anime_id does exist in table, that means the anime is already saved in anime_cache from previous search. if we were to also update the similar_anime column with similar_anime_text, we'd overrwrite the list of previously saved
        # similar anime with [] - since before entering this cursor.execute, it's set to []. so the flow is if the anime is not in anime_cache, it's added to the table with similar_anime column set to []. If the user clicks the View Similar Anime button,
        # it only then saves the list of similar anime to the similar anime column for that specific anime. Now, if someone searches for the anime again, let's say Naruto, the save_to_cache function runs. It checks if the anime has already been added to anime_cache.
        # if it has, we do not need to set the similar_anime column to [] again. This is because after Naruto was added to anime_cache, the user MAY HAVE clicked View Similar Anime, so the similar_anime list results were saved anime_cache. Again, if the anime exists in 
        # anime_cache, that DOES NOT necessarily mean similar_anime column has data yet. We just do NOT need to set the similar_anime column to [] each time we search Naruto, since the user may have already saved its similar_anime list to anime_cache.
        # the similar_anime list in anime_cache should only be updated in the save_similar_anime_to_cache function
        
        if existing_row:    # existing_row = (20,) is True for example. Anime exists, so only update all values except similar_anime column
            cursor.execute("""
                    UPDATE anime_cache
                   SET title = ?, image_url = ?, synopsis = ?, genres = ?, fetched_at = ?, recommendation_source = ?
                   WHERE anime_id = ? 
                           """,
                           (
                               anime["title"],
                                anime["image_url"],
                                anime["synopsis"],
                                genres_text,
                                fetched_at,
                                recommendation_source
                                anime["anime_id"]
                           )
                    )
        else:           # existing_row = None is False for example. This is the first time the anime is being added to anime_cache, so insert these values fresh
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
                fetched_at,
                recommendation_source,
                similar_anime_source
            )
            
            -- We use "?" as placeholder values, since Naruto values will be different than Bleach, etc
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            
            # these are the actual values that will fill in the placeholder ?. This is a tuple. Python provides these values, SQLite combines them with the placeholder values
            (
                anime["anime_id"],
                anime["title"],
                anime["image_url"],
                anime["synopsis"],
                genres_text,
                similar_anime_text,
                fetched_at,
                recommendation_source,
                None
            )
            )
    
    conn.commit()
    conn.close()
        
        

    
def limit_cache_size():
    conn = sqlite3.connect("anime_app.db")
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
    conn = sqlite3.connect("anime_app.db")
    cursor = conn.cursor()
    
    cursor.execute("""
                -- changed it from that to explicitly stating which columns I'm using. In case the table column order changes later, this ensures I'm selecting the right columns         
                SELECT anime_id, title, image_url, synopsis, genres, similar_anime, fetched_at, recommendation_source 
                FROM anime_cache
                WHERE title LIKE ? 
                """,
                # comma is needed after anime_name to make sure it's a tuple - when entering multiple values, don't need to explicitly do it since it can tell
                # before it was (anime_name,). but if it's "naruto", results with "Naruto" will not show. This format with % means anything that contains the text "naruto" - can be "Naruto: Last generations", "naruto: shippuden", etc. 
                # for that reason we use LIKE instead of = for the syntax above
                (f"%{anime_name}%",)    # extra () needed so SQL treats this as one object. Before it treated "Naruto" as 6 objects, instead of 1 tuple which it should be 
               )
    rows = cursor.fetchall()
    
    anime_results = []
    for row in rows:
        # anime_id is at row[0] here since we did not select id as a column in cursor.execute()
        item = {"anime_id": row[0], "title": row[1], "image_url": row[2], "synopsis": row[3] or "No synposis available.", "genres": json.loads(row[4]), 
                "recommendation_source": row[7]}
        # do not currently use similar_anime and fetched_at data from the results of this function, so not in the item dictionary
        # use indices since tuples require indices, they don't use key and value
        # genres and similar_anime are still JSON strings from database, so we'll need to do json.loads() on them before returning them
        
        anime_results.append(item)    # create a new dictionary from each row, save to anime_results list
        
    # conn.commit() not needed for SELECT since only reading from the table
    conn.close()
    
    return anime_results

def get_similar_anime_cached_results(anime_id):
    conn = sqlite3.connect("anime_app.db")
    cursor = conn.cursor()
    
    cursor.execute("""
                   SELECT 
                        similar_anime,
                        similar_anime_source
                   FROM anime_cache
                   WHERE anime_id = ?
                   """,
                   (anime_id,)
    )
    
    # before fetchall, value is just 1 JSON string - it's not a tuple yet - '[{"anime_id":1,"title":"One Piece"}, {"anime_id":2,"title":"Bleach"}]'
    
    similar_anime_list = cursor.fetchall()
    
    # this is an example of what cursor.fetchall() returns, what's inside similar_anime_list. It's a list, since fetchall always returns a list of rows. Each row is represented as a tuple. Since we only selected 1 column, similar_anime,
    # each tuple has only 1 element. Contains 1 tuple whose first element is a json string.
    # start:
    # [
    # ('[{"anime_id":1,"title":"One Piece"}, {"anime_id":2,"title":"Bleach"}]',)
    # ]
    
    # the outer list has all matching rows
    # [
    # (...)
    # ]
    
   
    
    # if similar anime list has no content, return []
    if len(similar_anime_list) == 0:
        conn.close()
        return ([], None)
    
    similar_anime_text = similar_anime_list[0][0]   # similar_anime_text is a JSON formatted string that has info of the first (and only) - (first [0]) row and first (and only) column - second [0]
    # similar_anime_text = '[{"anime_id":1,"title":"One Piece"}, {"anime_id":2,"title":"Bleach"}]' - not a python list  yet
    
    # when we write similar_anime_list[0], we get the first row, or 1 tuple
    # (
    # '[{"anime_id":1,"title":"One Piece"}, {"anime_id":2,"title":"Bleach"}]',
    # )
    
    # then similar_anime_list[0][0] gives 
    # '[{"anime_id":1,"title":"One Piece"}, {"anime_id":2,"title":"Bleach"}]'. first [0] - first row, second [0] - first column of that row
    # now this is a JSON string by itself
    
    similar_anime_source = similar_anime_list[0][1]
    
    conn.close()
    
    cached_results = json.loads(similar_anime_text)       # converts json string to a python list now
    
    return cached_results, similar_anime_source
    
    # python list looks like this now
    # end:
    # [
    # {"anime_id": 1, "title": "One Piece"},
    # {"anime_id": 2, "title": "Bleach"}
    # ]
    
#     Database
#     ↓
#      JSON string

#      fetchall()
#       ↓
#   List
#   └── Tuple
#       └── JSON string

#   [0][0]
#     ↓
#   JSON string

#   json.loads()
#     ↓
#   Python list

# the tuple is created by SQLite/Python to represent a database row, while the JSON string is the actual value stored inside the similar_anime column.

# this is a helper function that saves a list of similar anime for a specific anime to the cache list, only for that anime, when the button is clicked. all other similar anime columns for different animes in cache are unaffected.
def save_similar_anime_to_cache(anime_id, similar_anime_list, similar_anime_source):
    similar_anime_list_text = json.dumps(similar_anime_list)    # converts python list to a json string - cannot saves lists to a database, so we convert it to TEXT
    conn = sqlite3.connect("anime_app.db")
    cursor = conn.cursor()
    
    cursor.execute("""
                   UPDATE anime_cache
                   SET 
                        similar_anime = ?,
                        similar_anime_source = ?
                        
                   WHERE anime_id = ?   
                   """,
                   (
                       similar_anime_list_text,
                       similar_anime_source,
                       anime_id
                    )
                )
    conn.commit()
    conn.close()        # always do this
    
    
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
        # now also include the api source here
        results1, source1 = get_recommendation(anime_name)
        
        if not results1:        # if results1 = [], that means python requests to myanimelist are not working. because in get_recommendations function inside phase1_script.py, I did if "data" not in data:
            # return []. This way at least we get [] instead of nothing. Then this will cause the frontend to say the anime data is temporarily unavailable
            results1 = get_cached_results(anime_name)
            
            response = RecommendationResponse(
                result_source= "cache",
                message= "Live anime services are currently unavailable. Results shown are from saved cache data.",
                results=results1
            )
            
            return response
        
        # does not matter which API the results are from, will still save to cache    
        save_to_cache(results1)
        limit_cache_size()
        
        response = RecommendationResponse(
            result_source= source1,     # the api source goes here
            message= "",
            results=results1
        )
        
        return response
    
    except Exception as error:      # Exception is the base class for almost all normal Python errors. It includes AttributeError, KeyError, TypeError, ValueError, sqlite3.OperationalError
        # except Exception means catch any normal Python exception. "as error" saves the actual error object into the variable named error. Now we can see what error it is in terminal.
        print("ERROR IN RECOMMENDATIONS ENDPOINT:", error)
        results1 = get_cached_results(anime_name)
        
        response = RecommendationResponse(
            result_source= "cache",
            message= "Cannot pull information from the Jikan API currently. Results shown are pulled from the saved cache data.",
            results=results1
        )
        return response
    

# switched to a POST endpoint (originally was a GET endpoint that took in anime_id and genre_ids in the url).
# switched because now frontend sends nested JSON objects instead (genres is a list of dictionaries / objects, whereas genre_ids was 1 string).
# a URL is not designed for sending nested JSON objects like this. That's exactly what an HTTP request body is for.

# So React now sends:

# POST /similar-anime

# with the JSON body:

# {
#   "anime_id": 20,
#   "genres": [
#     {
#       "name": "Action",
#       "jikan_id": 1
#     },
#     {
#       "name": "Adventure",
#       "jikan_id": 2
#     }
#   ]
# }

# FastAPI then automatically creates

# request = SimilarAnimeRequest(...)

# which is much cleaner.


@app.post("/similar-anime")     # this creates the endpoint
# When React sends a POST request to /similar-anime, FastAPI calls similar_anime_endpoint()
def similar_anime_endpoint(request: SimilarAnimeRequest):   # we never manually create this parameter, FastAPI does
    # like how in def watchlist_endpoint(anime: Anime): FastAPI automatically creates anime from the JSON, now it creates request instead
    try:
        similar_anime_list, source = get_similar_anime(
            request.anime_id,
            request.genres
        )
    
        if similar_anime_list:
            save_similar_anime_to_cache(request.anime_id, similar_anime_list, source)       # save the similar anime list to the specific anime correlating to this anime_id in the anime_cache table
            return SimilarAnimeResponse(
                result_source = source,
                similar_anime_source = source,
                message = "",
                results = similar_anime_list
            )
        
        else:   # if list of similar anime is empty (jikan returns empty), we check cached results of similar anime for this specific anime to see if it was saved there at some point
            cached_results, cached_source = get_similar_anime_cached_results(request.anime_id)
            return SimilarAnimeResponse(
                result_source = "cache",
                similar_anime_source= cached_source,
                message = "Live similar-anime services are currently unavailable. Saved results are shown.",
                results = cached_results
            )
        
    except Exception as error:      # Exception is the base class for almost all normal Python errors. It includes AttributeError, KeyError, TypeError, ValueError, sqlite3.OperationalError
#         # except Exception means catch any normal Python exception. "as error" saves the actual error object into the variable named error. Now we can see what error it is in terminal.
        print("ERROR IN SIMILAR ANIME ENDPOINT:", error)    # if Jikan API not working, get cached results
        
        cached_results, cached_source = get_similar_anime_cached_results(request.anime_id)
        return SimilarAnimeResponse(
            result_source = "cache",
            similar_anime_source= cached_source,
            message = "Live similar-anime services are currently unavailable. Saved results are shown.",
            results = cached_results
            )

    


# to start / host the backend server (make it alive), type this in "Terminal" -> "New Terminal". should be in location C:\anime-recommendation-app\backend>
# uvicorn main:app --reload.    This follows structure of "uvicorn filename:app_object --reload".  here, --reload automatically restarts the server when I make code changes
# to visit, type this url "localhost:8000/recommendations/{anime_name}", but actually insert a real anime name into the variable.
# or this: "http://127.0.0.1:8000/recommendations/naruto". Can copy the link showed at beginning of terminal, then add the search endpoint and query myself. endpoint is recommendation, query is naruto

# this function saves anime to a watchlist
@app.post("/watchlist")
def watchlist_endpoint(anime: Anime):   # anime: Anime - this says that the parameter anime is of type Anime, which is an object - it's an instance of Anime Pydantic model
    # this endpoint receives an anime object
    
    genres_text = json.dumps(anime.genres)      # turns Python list of genres into JSON string - needed since SQLite cannot store a list, it can only store a string value
    
    conn = sqlite3.connect("anime_app.db")      # here anime_app.db already exists, so it'll just reopen the existing database created when database_setup.py first ran
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
            genres,
            recommendation_source
        )
        
        -- We use "?" as placeholder values, since Naruto values will be different than Bleach, etc
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        
        # these are the actual values that will fill in the placeholder ?. This is a tuple. Python provides these values, SQLite combines them with the placeholder values
        (
            anime.anime_id,
            anime.title,
            anime.image_url,
            anime.synopsis,
            genres_text,
            anime.recommendation_source
        )
        )
    
        conn.commit()       # commit() tells SQLite to save those changes permanently
        
        return {"message": "Anime saved to watchlist"}
    
    except sqlite3.IntegrityError:      # Prevents saving duplicate anime. prevents multiple anime with the MAL ID (therefore have the same anime_id) to be entered in the table. 
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
    SELECT anime_id, title, image_url, synopsis, genres, recommendation_source
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
        item = {"anime_id": row[0], "title": row[1], "genres": json.loads(row[4]), "synopsis": row[3], "image_url": row[2], "recommendation_source": row[5]}
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