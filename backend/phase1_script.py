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
    
    main_anime = anime_list[0]      # main_anime is the first anime in anime_list (probably the main series)
    genres = main_anime['genres']   # list of genres for the first anime in anime list
    genre_ids = []             # empty list to hold the id numbers of the genres of this specific anime
    
    for genre in genres:        # loop through list of genres for this specific anime
        genre_ids.append(genre["mal_id"])       # for each specific genre (example is Action), add its id (here 1) to the list of genre_ids. This list is dynamic based on the anime in anime_list.
    
    #example, for Naruto, now genre_ids = [1, 2, 10]
        
    recommendations = get_genre_recommendations(genre_ids)
    results.append({"similar anime": recommendations})  # will show the similar anime at the very top. other option was to put it at the very bottom, but that doesn't seem user-friendly
    # also now have similar anime only in relation to first anime. it keeps it similar, don't need similar anime for all anime
    
    
    # print(recommendations) to see what recommendations holds
    
    # what's happening for each list in the loop
    # item (1st loop iteration) = {"title ": data["data"][0]['title'], "genres ": data["data"][0]['genres'], synopsis ": data["data"][0]['synopsis'], "images: ": data["data"][0]['images']['jpg']['image_url']}
    # item (2nd loop iteration)= {"title ": data["data"][1]['title'], "genres ": data["data"][1]['genres'], "synopsis ": data["data"][1]['synopsis'], "images: ": data["data"][1]['images']['jpg']['image_url']}
    # index increments through how many items are in anime list
    
    for anime in anime_list:
        item = {"title ": anime['title'], "genres": anime['genres'], "synopsis ": anime['synopsis'], "images: ": anime['images']['jpg']['image_url']}
        
        genres = anime['genres']  # list of genres for this specific anime in this loop iteration
        
        results.append(item)
          
        
    # results is a list that contains dictionaries
    return results


def get_genre_recommendations(genre_ids):
    genre_string = ",".join(str(id) for id in genre_ids)    # from previous example, genre_string = "1,2,10". str(id) converts each id number to a string while looping through them. ",".join puts a comma between each id value
    genre_search_url = f"https://api.jikan.moe/v4/anime?genres={genre_string}"      # build url using string of genre_string
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



