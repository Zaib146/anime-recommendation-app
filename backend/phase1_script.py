import requests # needed to fetch json data from Jikan API   

#  enter anime name. from requests library, use get method to get json data from Jikan API. Returns raw JSON data into variable "response"
#  use the .json() method on response to parse the json data and return it as python dictionaries and lists. Store that into variable data.

# this helper function normalizes the anime genre results into one body. So the React does not care which API the genres came from, because all will be in the same structure anyway
# this is conversion logic for Jikan function

# Original jikan_genres structure:
#
# [
#     {
#         "mal_id": 1,
#         "type": "anime",
#         "name": "Action",
#         "url": "https://myanimelist.net/anime/genre/1/Action"
#     },
#     {
#         "mal_id": 2,
#         "type": "anime",
#         "name": "Adventure",
#         "url": "https://myanimelist.net/anime/genre/2/Adventure"
#     }
# ]
#
# Converted into:
#
# [
#     {
#         "name": "Action",
#         "jikan_id": 1
#     },
#     {
#         "name": "Adventure",
#         "jikan_id": 2
#     }
# ]

def normalize_jikan_genres(jikan_genres):
    normalized_genres = []
    
    # here genre is a dictionary, or a genre object, so we access genre['name'] and genre['mal_id']
    for genre in jikan_genres:
        normalized_genres.append({
            "name": genre["name"],
            "jikan_id": genre["mal_id"]
        })
    return normalized_genres

# same idea as normalize_jikan_genres function

# Original AniList genre structure:
#
# [
#     "Action",
#     "Adventure",
#     "Comedy"
# ]
#
# Converted into:
#
# [
#     {
#         "name": "Action",
#         "jikan_id": None
#     },
#     {
#         "name": "Adventure",
#         "jikan_id": None
#     },
#     {
#         "name": "Comedy",
#         "jikan_id": None
#     }
# ]

def normalize_anilist_genres(anilist_genres):
    normalized_genres = []
    
    # here there's no dictionary like in jikan, so we just use genre_name, a genre string
    for genre_name in anilist_genres:
        normalized_genres.append({
            "name": genre_name,
            "jikan_id": None
        })
    return normalized_genres

# this function handles the actual recommendation logic, the fetch logic
def get_jikan_recommendation(anime_name):
    anime_search_url = f"https://api.jikan.moe/v4/anime?q={anime_name}"
    response = requests.get(anime_search_url)
    data = response.json()          # convert the JSON results back into Python dictionaries and lists so we can work with the data
    
    print("STATUS CODE: ", response.status_code)
    print("JIKAN RESPONSE: ", data)
    
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

        normalized_genres = normalize_jikan_genres(anime['genres'])
        item = {"anime_id": anime["mal_id"], "title": anime['title'], "genres": normalized_genres, "synopsis": anime['synopsis'] or "No synposis available.", "image_url": anime['images']['jpg']['image_url']}
        
        results.append(item)
          
    # removed calling similar anime list for each anime in the list. Load time for the page was too long. Now will only be called with a button. Therefore, deleted the logic that extracted the genre ids from anime in anime list.
    # since the genre-id extraction will happen in React when the user clicks the button, because React already has access to anime.genres as a part of Anime pydantic model. Don't need that here, since not calling similar anime 
    # each time automatically now    
    # results is a list that contains dictionaries
    return results

def get_anilist_recommendation(anime_name):
    # query is a python string that contains GraphQL code, like how I have SQL code inside a python string in main.py
    query = """     
    query ($search: String) {   # this says that my GraphQL query expects one variable named search. The $ sign tells GraphQL this is a variable, not a literal value
        # adding this Page as a wrapper now returns a list of the first 25 anime that have the search word of the anime title, like "Naruto" in it. For example, it'll return "Naruto,
        # Naruto Shippuden, Boruto: Naruto Next Generations", etc. Without the Page wrapper, it was only returning "Naruto". We chose 25 per page since that's around the number Jikan would return too.
        # If we want to return more, we would do Page(page: 2, perPage: 25) etc
        Page(page: 1, perPage: 25) {
    
            # here $search is like ? in SQL. it's a placeholder that will be replaced with the anime name, like "Naruto", that's defined in the "variables" dictionary
            # search anilist's media database with the value in search, only returning type anime (not manga)
            
            media(search: $search, type: ANIME) {
                # everything below is what we're requesting from AniList API. Unlike REST API's, GraphQL never sends extra information.
                # with GET request with REST API, server decides what I get; with POST request with GraphQL, I decide exactly what I get - so app only downloads fields it actually uses
                
                id      # AniList's own ID. We are requesting for the anime ID here
                idMal   # corresponding MyAnimeList ID. current project revolves around this
                
                title {     # Anime titles: AniList can also return the title in native japanese, but we only care for english and romaji. here title is an object
                    english
                    romaji
                }
                
                coverImage {        # Cover Image: same idea as title. we could get extraLarge, medium, color, etc, we only want large here
                    large
                }
                
                description         # Synopsis: this is the same as anime["synopsis"] in REST API
                
                genres              # Genres: this is the same as anime["genres"] in REST API
                                                        
                } 
            
        }                                           
    } 
    """
    # create a "variables" dictionary we'll send with query in our POST request. we call the key here "search" because it needs to match with the $search variable in GraphQL, so it can 
    # replace $search with anime_name - remember, $search is like ? in SQL, anime_name replaces it
    variables = {
        "search": anime_name
    }
    
    url = "https://graphql.anilist.co"      # unlike Jikan, the AniList URL never changes. The anime name does not go in the URL, it goes in the request body
    
    # with POST, we say "Here's my URL and here's the GraphQL query I want you to execute." In Jikan with requests.get(), we say "Here's my URL."
    response = requests.post(
        url,
        json = {        # json = is saying convert this dictionary into JSON and send it in the HTTP request body. This is the same thing React does in the app when it sends a POST request to FastAPI
            "query": query,         # the left side, "query", is the name the GraphQL server expects. The right side, query, is the Python variable
            "variables": variables  # same here like with query above
        }
    )
    
    # when combined, this is the JSON, what the HTTP request body looks like
    # {
    # "query": "query ($search: String) { Media(search: $search, type: ANIME) { ... } }",

    # "variables": {
    #     "search": "Naruto"
    # }
    
    # AniList returns the information as JSON (response is in JSON)
    
    data = response.json()      # convert the JSON results back into Python dictionaries and lists so we can work with the data
    
    # can see if request worked in backend terminal, and the results there too
    print("STATUS CODE: ", response.status_code)
    print("ANILIST RESPONSE: ", data)
    
    anime_list = data["data"]["Page"]["media"]
    
    results = []
    
    for anime in anime_list:
        
        normalized_genres = normalize_anilist_genres(anime['genres'])
        
        # some anime do not have an english title, so include the romaji title
        item = {"anime_id": anime["idMal"], "title": anime['title']['english'] or anime['title']['romaji'],
                "genres": normalized_genres, "synopsis": anime['description'] or "No synposis available.",
                "image_url": anime['coverImage']['large']}
        results.append(item)
    return results

def get_recommendation(anime_name):
    results = get_anilist_recommendation(anime_name)   # second call in case 
    
    if results:     # if the Jikan API returns actual anime results, we're done. 2 scenarios where it doesn't: the API request succeeded, but Jikan API has no information about the anime, so empty.
        # scenario 2 is where the API request fails, so results is empty. results is true when both the API request is a success, and we actually get back anime information from the API
        return results

# frontend now sends my standardized genres, no longer a list of genre_ids
# jikan extracts genre_ids
def get_jikan_genre_recommendations(genres):
    
    # first thing is the function extracts the genre_ids from genres (we create a list called genres_ids and append to it)
    
    genre_ids = []
    
    for genre in genres:
        if genre["jikan_id"] is not None:
            genre_ids.append(genre["jikan_id"])
            
    # now function continues as before
    genre_string = ",".join(str(id) for id in genre_ids)    # from previous example, genre_string = "1,2,10" (parameter was ["1", "2", "10"]). 
    # str(id) converts each id number to a string while looping through ids in the original list. ",".join puts a comma between each id value
    genre_search_url = f"https://api.jikan.moe/v4/anime?genres={genre_string}"      # build url using string of genre_string
    response = requests.get(genre_search_url)       # gets json data of the genres
    data = response.json()      # parse through the json data and return it as a list of genres
    
    # print(data)       # to see what data holds
    
    genre_list = data["data"]   # data is a dictionary variable. genre_list is a list that contains dictionaries
    anime_list = []             # empty list to hold titles of other anime with same genres
    
    for anime in genre_list:        # loop through each anime that has the same genres
        anime_list.append(anime['title'])       # add the title of each of those animes to anime_list
    
    # print(anime_list[:5])     # to see what's being returned
    return anime_list       # this returns a list of other animes that have the same genres as the original anime


# anilist has its own recommendations for each anime based on what other users recommended. so i'm going to get those (exists within media), and give the top 10 recommendations that way.
# I will NOT give similar anime based on same genres like I did with Jikan, because of this difference
# will not use genres parameter for now, still have it here to be consistent with get_jikan_genre_recommendations. for future apis, can include extra info in parameters like that for consistency,
# do not have to actually use. as of right now, this function will only actually be called with the parameter anime_id, not genres
def get_anilist_similar_anime(anime_id, genres):
    # similar struction as in get_anilist_recommendation function with the post request
    query = """
    query ($idMal: Int) {       # this declares a GraphQL variable named idMal
    $idMal is the variable whose value will be replaced later, like $search earlier

        # Find the AniList anime whose MyAnimeList ID matches the ID passed from your app
        media(idMal: $idMal, type: ANIME) {     # here recommendations also exists inside media (think of media as a huge object
        GraphQL only sends info from media we request)
        
            # asks AniList for up to ten highly rated recommendations connected to that anime.
            recommendations(page: 1, perPage: 10, sort: RATING_DESC) {
                
                # each node has rating, user, date, and recommended anime info. we only care about recommended anime,
                which is called mediaRecommendation inside of nodes
                nodes {
                    
                    # from the recommended anime info, we only want the anime id (MAL Ids, since current
                    # project revolves around this) and its name
                    mediaRecommendation {
                        idMal
                        title {
                            english
                            romaji
                        }
                    }
                }
            }
        }
    }
    """
    
    variables = {
        "idMal": anime_id
    }
    
    # fixed url
    url = "https://graphql.anilist.co"
    
    # AniList,Here's the query I want you to execute. Here are the variables to plug into it.
    # with POST, we say "Here's my URL and here's the GraphQL query I want you to execute." In Jikan with requests.get(), we say "Here's my URL."
    
    # the left side, "query", is the name the GraphQL server expects. The right side, query, is the Python variable
    # for variables, same here like with query above
    
    response = requests.post(
        url, 
        json = {     #json = is saying convert this dictionary into JSON and send it in the HTTP request body. 
                        # This is the same thing React does in the app when it sends a POST request to FastAPI
            "query": query,
            "variables": variables
        }
    )
        
    data = response.json()   # convert the JSON results back into Python dictionaries and lists so we can work with the data
    
    # can see if request worked in backend terminal, and the results there too
    
    print("ANILIST SIMILAR STATUS: ", response.status_code)
    print("ANILIST SIMILAR RESPONSE: ", data)
    
    # conceptually, this is what the JSON response, in python form, looks like
    # {
    # "data":
    # {
    #     "media":
    #     {
    #         "recommendations":
    #         {
    #             "nodes":
    #             [
    #                 recommendation 1,
    #                 recommendation 2,
    #                 recommendation 3
    #             ]
    #         }
    #     }
    # }
    # }
    
    recommendation_nodes = data['data']['media']['recommendations']['nodes']
    
    # so recommendation_nodes is just this python list below, like how anime_list was a python list in
    # get_anilist_recommendation() function
    #             [
    #                 recommendation 1,
    #                 recommendation 2,
    #                 recommendation 3
    #             ]
    
    # this will be the list of titles of similar anime
    similar_anime_list = []
    
    
    # for first iteration, recommendation is recommendation 1 in the above python list. 
    # recommendation 1 has a mediaRecommendation, as described earlier.
    for recommendation in recommendation_nodes:
        # recommended_anime has the information inside of the dictionary mediaRecommendation
        recommended_anime = recommendation['mediaRecommendation']

        # if there is content inside the dictionary mediaRecommendation, do this 
        # (anilist could have it blank here, would cause an error without this statement)
        if recommended_anime is not None:
            # within mediaRecommendation, we extract the title
            title = (
                recommended_anime['title']['english'] or recommended_anime['title']['romaji']
            )

        similar_anime_list.append(title)
        
    # now has list of 10 similar anime by title    
    return similar_anime_list