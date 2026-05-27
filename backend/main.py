from fastapi import FastAPI
from phase1_script import get_recommendation

# create app object
app = FastAPI()

@app.get("/recommendations/{anime_name}")
def recommendations_endpoint(anime_name):
    return get_recommendation(anime_name)