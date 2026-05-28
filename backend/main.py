from fastapi import FastAPI     # needed for backend setup
from phase1_script import get_recommendation

# create app object
# this creates my backend server, we're creating an application object here. This "app" becomes my server, my API, my backend. Everything attaches to this object
app = FastAPI()

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

# notes for git commands
# 1. git status - see status if files, if they're modified, staged, see if changes are staged for commmit 
# 2. git add . - take all modified files in this folder and prepare them for the next commit. This is called "staging". Nothing is saved yet. We've only selected the files that will be included in the save point 

# before "git add ."
# Working Directory
# ├── main.py (modified)
# └── phase1_script.py (modified)

# Staging Area
# (empty)

#after "git add ."
# Working Directory
# ├── main.py
# └── phase1_script.py

# Staging Area
# ├── main.py
# └── phase1_script.py

# 3. git commit -m "message" - Git takes everything in the staging area and creates a permanent snapshot. This is the actual "save" or "checkpoint". 
# "message" is the note attached to this save point. Can view these notes in my commit history
# after git commit -m "message", Git now remembers:  
# Commit A
# ├── main.py
# └── phase1_script.py
# these changes are saved in my local Git repository (on PC, NOT on Github yet) - commit exists only on PC

# 4. git push - uploads your local commits to Github

# before git push:
# Your PC
# └── Commit A

# GitHub
# └── Older version

# after git push: 
# Your PC
# └── Commit A

# GitHub
# └── Commit A

# git log --oneline: shows commit history (newest at top)
# this is older, probably don't use: git checkout <commit-id> example is git checkout 45d9e03: temporarily inspect old code
# git switch main - return to latest version, branch switching
# git switch --detach <commit_id>: detached commit viewing. Move you to that commit in a detached HEAD state. git checkout <commit-id> does the same thing
# both actually change the VS code files to become the versions at the entered <commit_id>. can change them back though
# git restore <filename> - example is git restore main.py: this is file restoring. same as git checkout <filename>
# git switch -c feature-watchlist: creates a new branch attached at main (main stays where it is). now the experimental work happens at the branch feature-watchlist. same as git checkout -b feature-watchlist
# so workflow could be this: git switch -c feature-react-frontend, then git commit -m "Added anime card component", then git switch main. Now that we are in main (in the branch that will receive changes if we merge), if happy with the experiment, we can merge.
# merge by git merge feature-watchlist

# example:
# git switch -c feature-watchlist

# # make changes

# git add .
# git commit -m "Added SQLite watchlist"

# git switch main
# git merge feature-watchlist
# git push

# AVOID THIS FOR NOW - git reset --hard <commit-id>: truly moves the branch backwards. changes vs code files and removes later commits from the branch. 
# git revert <commit_id>: common practice to undo a previous commit is not to move the branch backwards. Instead, create a new commit that undoes a previous one.

