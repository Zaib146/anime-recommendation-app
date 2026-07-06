import requests # needed to fetch json data from Jikan API   

#  enter anime name. from requests library, use get method to get json data from Jikan API. Returns raw JSON data into variable "response"
#  use the .json() method on response to parse the json data and return it as python dictionaries and lists. Store that into variable data.

# this function handles the actual recommendation logic
def get_recommendation(anime_name):
    anime_search_url = f"https://api.jika.moe/v4/anime?q={anime_name}"
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
    
    # print("JIKAN SEARCH RESPONSE:", data) - used to debug when getting blank page on frontend
    # data is a dictionary variable. anime_list is a list that contains dictionaries
    
    if "data" not in data:      # if python requests to myanimelist are not working, at least we get [] instead of nothing. Then this will cause the frontend to say the anime data is temporarily unavailable.
        return []
    
    anime_list = data["data"]
    # how to check this is a list
    # print(type(data["data"]))
    
    # will store our selected information
    results = []

    # print(recommendations) to see what recommendations holds
    
    # what's happening for each list in the loop
    # item (1st loop iteration) = {"title ": data["data"][0]['title'], "genres ": data["data"][0]['genres'], synopsis ": data["data"][0]['synopsis'], "images: ": data["data"][0]['images']['jpg']['image_url']}
    # item (2nd loop iteration)= {"title ": data["data"][1]['title'], "genres ": data["data"][1]['genres'], "synopsis ": data["data"][1]['synopsis'], "images: ": data["data"][1]['images']['jpg']['image_url']}
    # index increments through how many items are in anime list
    
    for anime in anime_list:

        item = {"anime_id": anime["mal_id"], "title": anime['title'], "genres": anime['genres'], "synopsis": anime['synopsis'] or "No synposis available.", "image_url": anime['images']['jpg']['image_url']}
        
        results.append(item)
          
    # removed calling similar anime list for each anime in the list. Load time for the page was too long. Now will only be called with a button. Therefore, deleted the logic that extracted the genre ids from anime in anime list.
    # since the genre-id extraction will happen in React when the user clicks the button, because React already has access to anime.genres as a part of Anime pydantic model. Don't need that here, since not calling similar anime 
    # each time automatically now    
    # results is a list that contains dictionaries
    return results


def get_genre_recommendations(genre_ids):
    genre_string = ",".join(str(id) for id in genre_ids)    # from previous example, genre_string = "1,2,10" (parameter was ["1", "2", "10"]). 
    # str(id) converts each id number to a string while looping through ids in the original list. ",".join puts a comma between each id value
    genre_search_url = f"https://api.jika.moe/v4/anime?genres={genre_string}"      # build url using string of genre_string
    response = requests.get(genre_search_url)       # gets json data of the genres
    data = response.json()      # parse through the json data and return it as a list of genres
    
    # print(data)       # to see what data holds
    
    if "data" not in data:
        return []
    
    genre_list = data["data"]   # data is a dictionary variable. genre_list is a list that contains dictionaries
    anime_list = []             # empty list to hold titles of other anime with same genres
    
    for anime in genre_list:        # loop through each anime that has the same genres
        anime_list.append(anime['title'])       # add the title of each of those animes to anime_list
    
    # print(anime_list[:5])     # to see what's being returned
    return anime_list       # this returns a list of other animes that have the same genres as the original anime



