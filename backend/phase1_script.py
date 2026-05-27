import requests # needed to fetch json data from Jikan API
from fastapi import FastAPI     # needed for backend setup

# this creates my backend server, we're creating an application object here. This "app" becomes my server, my API, my backend. Everything attaches to this object
app = FastAPI()

#  enter anime name. from requests library, use get method to get json data from Jikan API. Returns raw JSON data into variable "response"
#  use the .json() method on response to parse the json data and return it as python dictionaries and lists. Store that into variable data.

# this function handles the actual recommendation logic
def get_recommendation(anime_name):
    anime_search_url = f"https://api.jikan.moe/v4/anime?q={anime_name}"
    response = requests.get(anime_search_url)
    data = response.json()
    
    # anime list here represents the values held at key "data" in the dictionary variable data (the json to now python data)
    # outer structure - data["data"] = dictionary access by key "data"
    # inner structure - anime_list[0] =  list access by index
#     anime_list[0] = first item in the list "anime_list". That item is a dictionary. so anime_list[0] is a dictionary
#     anime_list[0]["title"] is list access 1st, then dictionary access 2nd by key "title" (returns the value associated with the key "title")

    # numbers usually mean list indexes
    # strings usually mean dictionary keys
    # but numbers could also be dictionary keys
    
    # structure is below
#     anime_list
# ↓
# [
     # first item in list is this dictionary
#    {
#       "title": "Naruto",
#       "synopsis": "...",
#    },

     # 2nd item in list is this dictionary
#    {
#       "title": "Bleach",
#       "synopsis": "...",
#    }
# ]
    
    
    # data is a dictionary variable. anime_list is a list that contains dictionaries
    anime_list = data["data"]
    # how to check this is a list
    # print(type(data["data"]))
    
    # will store our selected information
    results = []
    
    # what's happening for each list in the loop
    # item (1st loop iteration) = {"title ": data["data"][0]['title'], "synopsis ": data["data"][0]['synopsis'], "images: ": data["data"][0]['images']['jpg']['image_url']}
    # item (2nd loop iteration)= {"title ": data["data"][1]['title'], "synopsis ": data["data"][1]['synopsis'], "images: ": data["data"][1]['images']['jpg']['image_url']}
    # index increments through how many items are in anime list
    
    for anime in anime_list:
        item = {"title ": anime['title'], "synopsis ": anime['synopsis'], "images: ": anime['images']['jpg']['image_url']}
        results.append(item)
    # results is a list that contains dictionaries
    return results

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





