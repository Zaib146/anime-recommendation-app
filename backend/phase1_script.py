import requests # needed to fetch json data from Jikan API   

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
        item = {"title ": anime['title'], "genres": anime['genres'], "synopsis ": anime['synopsis'], "images: ": anime['images']['jpg']['image_url']}
        
        genres = anime['genres']  # list of genres for this specific anime in this loop iteration
        genre_ids = []             # empty list to hold the id numbers of the genres of this specific anime
        for genre in genres:        # loop through list of genres for this specific anime
            genre_ids.append(genre["mal_id"])       # for each specific genre (example is Action), add its id (here 1) to the list of genre_ids. This list is dynamic based on the anime in anime_list.
        #example, for Naruto, now genre_ids = [1, 2, 10]
            
        results.append(item)
        
        
    genres = anime['genres']    
        
    # results is a list that contains dictionaries
    return results







