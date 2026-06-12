import { useState } from 'react'    // this imports useState, which lets Reach remember changing values. Here, it remembers the button count
//next 3 imports import image files so the component can display them later with <img src={...} />
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
//this imports the CSS styling for this component
import './App.css'

//to start frontend in terminal, get to frontend folder if needed (cd frontend). Then type "npm run dev"

//this file is the main React component. this file controls what you actually see on the page, the actual app UI
/* Browser opens index.html
        ↓
index.html loads /src/main.jsx
        ↓
main.jsx imports App.jsx
        ↓
main.jsx places <App /> inside <div id="root">
        ↓
App.jsx decides what appears on screen */

// will edit this file constantly

/* Big picture:

App.jsx imports images/CSS
↓
creates App component
↓
uses state for count
↓
returns JSX
↓
main.jsx renders App onto the page

The key parts to understand before editing are:

function App()
const [count, setCount] = useState(0)
return (...)
onClick={() => setCount(...)}
export default App */

function App() {    // this line creates a React component named App. 
  /*The App() function is basically saying:

When React asks what should appear on the page,
return this JSX.

Returns this:

Anime Recommendation App
Input box
Button
Recommendations

The important mental model is:

App.jsx
     ↓
returns JSX
     ↓
React renders JSX
     ↓
User sees webpage*/

// JavaScript section: fetch data, save data, change state

  //Component is a reuasable UI function. It returns what should appear on the page
  const [anime, setAnime] = useState("")
  //this creates state. Original - count = current value, setCount = function used to change the value, 0 = starting value
  //now, anime is current value for anime. setAnime is the value anime will be updated to. "" is the starting value for anime. same logic for line below
  const [recommendations, setRecommendations] = useState([])
  const [currentView, setCurrentView] = useState("")    // this decides what will be shown on the page. current view is "recommendations", it'll show what's click when you click Get Recommendations.
  // if current view is "watchlist", it'll show what's clicked when you click View Saved Watchlist. It will only show EITHER recommendations or watchlist, not both. That is the point of currentView, to differentiate
  // what we say on the page
  const [watchlist, setWatchlist] = useState([])  // need a watchlist component, like we have one for recommendations
  const [similarAnimeById, setSimilarAnimeById] = useState({})    // when this is empty, that means no anime has loaded similar anime yet. Each anime we click it add, it adds to the list (keeps what was in it before)
  // for example, this is what's inside similarAnimeById after we click View Similar Anime for both Bleach and Naruto
  // {
  // 20: ["Bleach", "One Piece", "Black Clover"],
  // 269: ["Naruto", "Yu Yu Hakusho", "D.Gray-man"]
  // } 

  async function handleGetRecommendations()
  //async means this function will wait for something that takes time. This is because fetch with the url takes time.
  {
    setSimilarAnimeById({})     // clears the state. Basically a refresh in that you have to click View Similar Anime for that specific anime again
    const animeName = encodeURIComponent(anime) //Changes "One Piece" to "One%20Piece" in actual url, since url does not like spaces
    const url = "http://localhost:8000/recommendations/" + animeName
    const response = await fetch(url)   // await means pause this function until results come back, literally wait for results. 
    // here FastAPI is listening on port 8000, so it receives the request. App.jsx does not access backend files directly. 
    // App.jsx sends an HTTP request to the backend server. When React uses fetch, React is asking FastAPI for data automatically.
    const data = await response.json()    //parse json data into python data, store that in "data"
    setRecommendations(data)      // change recommendations to value in data variable
    setCurrentView("recommendations") // change currentView to "recommendations"
    // console.log(recommendations)   // this is to print in console tab in F12 to test. will comment out / remove later
  }

  // this request is a POST request. 
  async function handleSaveToWatchlist(anime)   // the parameter is the specific anime from the .map() loop. Here we are saving that specific anime to the watchlist
  {
    const animeToSave = {   // before, anime would only have the fields title, genres, synopsis, images. But we need to have an object that's shaped like our Pydantic model to send to backend. So we create it. Now shape of the button 
                            // matches what FastAPI expects. this is a Pydantic model for the specific anime passed. Each loop iteration, we'll have a new one 
      anime_id: anime.anime_id,
      title: anime.title,
      image_url: anime.images,
      synopsis: anime.synopsis,
      genres: anime.genres,
      similar_anime: anime.similar_anime
    }

    console.log("Saving anime:", animeToSave)
    const url = "http://localhost:8000/watchlist"   // we do not add parameter anime to url since this is a POST request. The anime data travels in the request body. because of the method: POST, it knows to do
    // the POST HTTP method, not the GET one
    // Without this line of (url, method: "POST"), fetch() defaults to method: "GET", which would not match my FastAPI endpoint of @app.post("/watchlist") 
    const response = await fetch(url, 
      {
        method: "POST",     
        headers:
        {
          "Content-Type": "application/json"  // this means that the data I'm sending is JSON. This helps FastAPI know how to interpret the request body
        },
        body: JSON.stringify(animeToSave)       //take the JavaScript object called animeToSave and convert it into JSON text so it can travel across the network. the body is the Naruto object
        //  for example, if
        //    animeToSave = {
        //       anime_id: 20,
        //       title: "Naruto"}
            
        //     then it becomes
        //     {
        //       "anime_id": 20,
        //       "title": "Naruto"} 
      })
    const data = await response.json()  // extract the JSON from the python information in response, store in data variable which is in python
    console.log(data)   // to check in console
  }

  // this is a DELETE request
  async function handleRemoveFromWatchlist(anime_id)
  {
    const url = "http://localhost:8000/watchlist/" + anime_id
    const response = await fetch(url,
      {
        method: "DELETE"  // here we only need anime_id, so no headers or body like in handleSaveToWatchlist function
      }
    )
    const data = await response.json() // extract the JSON from the python information in response, store in data variable which is in python
    console.log(data)   // to check in console
    handleViewWatchlist() // "refreshes" my page (refetches the view saved watchlist function, now after the delete is done)
  }

  // this is for a GET request
  async function handleViewWatchlist()
  {
    setSimilarAnimeById({})   // clears the state. Basically a refresh in that you have to click View Similar Anime for that specific anime again
    const url = "http://localhost:8000/watchlist" // same url is fine
    const response = await fetch(url)   // default HTTP method is a get method, so it'll do that. 
    const data = await response.json()    // extract the JSON from the python information in response, store in data variable
    setWatchlist(data)  // store watchlist (which is in the data variable) as the new "watchlist" state value
    setCurrentView("watchlist")
  }

  async function handleViewSimilarAnime(anime)
  {
    const genre_ids = anime.genres.map(genre => genre.mal_id)  // here, genres is a list with dictionaies that have mal_id and name (1, Action as values). Loop through that list. For each dictionary in the list
    //, here called "genre" get the mal_id value for that dictionary. So it would get "1" in this example and do the rest for the other dictionaries. It would make one list with the values, like [1,2,10]
    const genre_String = genre_ids.join(",")   // this combines the values in the list into one string with commas - it becomes "1,2,10". This is what our similar_Anime_endpoint function expects as a parameter
    const url = "http://localhost:8000/similar-anime/" + genre_String 
    const response = await fetch(url)   // call the similar_anime_endpoint function with that url
    const data = await response.json()    // parse the JSON data into python data, store in "data" variable
    setSimilarAnimeById(
      {
        ...similarAnimeById,    // create a new object. ...similarAnimeById means create a new object for similarAnimeById and copy all the old key-values pairs into the new one. This allows us to add new key-value pairs (different similar anime for different anime ids) without
        // completely replacing what was previously there. Want view similar anime for Naruto to show even after I click view similar anime for bleach
        [anime.anime_id]: data   // this adds the anime id as a key value and a list of the similar anime as a value represented by the variable "data"
      }
    )     // data now has a python list of all the similar anime. We put that list as the new value of similarAnimeById
    console.log(data)   // to check in console
  }

  async function handleRemoveSimilarAnime(anime_id)
  {
    // This is taking what's on the right side of the equals side, here similarAnimeById, and destructuring it. JSX is saying take the value at the index anime_id, store that value in the variable "removed". Everything else, store in the variable remainingSimilarAnime.
    // so we're creating 2 new constant variables. State has not yet been changed. 
    const {
      [anime_id]: removed,
      ...remainingSimilarAnime
    } = similarAnimeById
    setSimilarAnimeById(remainingSimilarAnime)  // this sets similarAnimeById by to what's left
    console.log(data)   // to check in console
  }

//   JSX section: display data, hide data, show buttons, show images

  return (   // return sends the JSX back to the browser
            // inside the return use, {/* */} for comments, it's safer. outside of return, use //
    <>    {/*This is a React Fragment. It lets you return multiple elements without wrapping everything in an extra <div></div>*/}
      <section id="center">   {/* This creates a page section. The id="center" connects to CSS styling */}
        <div className="hero">  {/* in React, we use className instead of HTML’s class. This connects the div to CSS styles named .hero*/}
          {/* these 3 lines display the imported images. The {heroImg} syntax means: “use the JavaScript variable named heroImg*/}
          <img src={heroImg} className="base" width="170" height="179" alt="" />
          <img src={reactLogo} className="framework" alt="React logo" />
          <img src={viteLogo} className="vite" alt="Vite logo" />
        </div>
        <div>
          <h1>Anime Recommendation App</h1>  {/*this displays the big title; <h1> = used for largest most important heading on the page*/}
          <p>
            What is your favorite anime?   {/*This displays the starter instruction text. <code> just styles text like code.*/}
          </p>
          {/*<input> lets the user type or enter data*/}
          <input    
            value={anime}
            onChange={(event) => setAnime(event.target.value)}
          /*onChange changes the value of anime for each keystroke as it's entered, not when the button Get Recommendations is clicked. 
          Anime variable is already changed to new value by then*/
          />

          {/*Anime is {anime} - this shows the state update if needed*/}

        </div>
        {/* <button> lets the user click something*/}

        {/*when the user clicks Get Recommendations, it calls this function. Since there's no argument, it can 
          safely be called only when clicked, since we're giving React the function itself. If it was instead onClick={handleGetRecommendations()},
          it would run without being click on*/}
        <button   
          /*this should get recommendations*/
          type="button"
          onClick={handleGetRecommendations}  
        >
          Get Recommendations
        </button>

        <button   
          /*this should get recommendations*/
          type="button"
          onClick={handleViewWatchlist}  
        >
          View Saved Watchlist
        </button>

          {/* now this block of code will only run if currentView === "recommendations". The 3 = signs is a conditional equals. The && means if the statement on the left is correct,
          execute what's on the right, here the code chunk in the parentheses. Also needed to put everything inside <> and </> since React needs only 1 single parent element. without that fragment, I have multiple */}
        {currentView === "recommendations" && 
        (
          <>
          
            {/*this recommendations.slice(1).map((anime) => is saying at index of 1 of recommendations onwards, loop through it (using map). (anime) represents the anime at that specific index each loop iteration}
            recommendations.slice(1).map((anime) => {
              console.log(anime.title)
              
            is the same as:

            for anime in recommendations[1:]:
              print(anime["title"])

            in Python*/}
            
            {recommendations.map((anime) => (  
              <div> {/*this <div> is a container for the anime information. It groups the elements below it together. It itself does not contain anything.*/}
                <p>Title: {anime?.title}</p>   {/*anime.title represents the anime at the specific index - for example, recommendations[1], then recommendations[2], etc*/}

                {/*since we are passing an argument, we need the () =>, otherwise the function would run
                    automatically. We only want the function to run when clicked. So () => creates a function that has the function handleSaveToWatchlist(anime)
                    , which is only called when button is click. "Create a function, but do not run it yet".
                    function() {
                    handleSaveToWatchlist(anime)
                    }*/}
                <button
                  type = "button"
                  onClick = {() => handleSaveToWatchlist(anime)}  
                >
                  Save to Watchlist
                </button>  

                {similarAnimeById[anime.anime_id] 
                 ? (
                    <>
                      <button
                        type = "button"
                        onClick = {() => handleRemoveSimilarAnime(anime.anime_id)}  
                      >
                        View Less
                      </button> 
                    </>
                  )

                 : (
                    <>
                      <button
                        type = "button"
                        onClick = {() => handleViewSimilarAnime(anime)}  // happens only when button is clicked - since we have a parameter, we use () => here
                      >
                      View Similar Anime
                      </button> 
                    </>
                  )
                }

                {/* now this block of code will only run if similarAnimeById[anime.anime_id] exists (does the key exist in there, checks by seeing if the value stored at that key exists). The && means if the statement on the left is correct,
          execute what's on the right, here the code chunk in the parentheses. Also needed to put everything inside <> and </> since React needs only 1 single parent element. without that fragment, I have multiple */}
                {similarAnimeById[anime.anime_id] &&
                (
                  <>
                    <p>Similar Anime: </p>    {/* this is JSX, so it goes directly in the return */}
                    {similarAnimeById[anime.anime_id].map(similarAnime => (<li>{similarAnime}</li>))}   {/* this line is JavaScript, so it must be wrapped inside {} in this return. Loop through all values in the list and display them in a list format
                    For example, if it's ["Bleach", "Naruto"], then display them with bullets on separate lines */}
                  </>
                )
                }

                

                <p>Genres: </p> {/* <p> = Paragraph, used for normal text*/}
                <ul>    {/* <ul> = Unordered List, creates a bulleted list container*/}
                  {anime?.genres?.map((genre) => (<li>{genre.name}</li>))}   {/* <li> = list item, each bullet inside a <ul> */}
                </ul>

                <p>Synopsis: </p>
                <p>
                  {anime?.synopsis}
                </p>

                <p>Images: </p>

                {/* alt is what shows if the src does not work */}
                <img
                  src = {anime?.images}
                  alt = {anime?.title}  
                />
                
                {/* ? is used for optional chaining. Only continue if the thing on the left exists. they are needed as when the page first loads, const [recommendations, setRecommendations] = useState([])
                so initially recommendations = [], so recommendations[0] and recommendations[1] are undefined. so recommendations[1].title becomes 
                undefined.title, and React crashes. So in recommendations[1]?.title, first get recommendations[1]. IF IT EXISTS, get .title. Else, return undefined*/}
                {/*<ul>    {/* <ul> = Unordered List, creates a bulleted list container*/}
                 
              </div>
            ))}
          </>
        )
        }

        {currentView === "watchlist" && 
        (
          <>
            {watchlist.map((anime) => 
              (  
                <div> {/*this <div> is a container for the anime information. It groups the elements below it together. It itself does not contain anything.*/}
                  <p>Title: {anime?.title}</p>   {/*anime.title represents the anime at the specific index - for example, recommendations[1], then recommendations[2], etc*/}

                  {/*since we are passing an argument, we need the () =>, otherwise the function would run
                      automatically. We only want the function to run when clicked. So () => creates a function that has the function removeFromWatchlist(anime)
                      , which is only called when button is click. "Create a function, but do not run it yet".
                      function() {
                      removeFromWatchlist(anime)
                      }*/}
                  {/* add a "Remove from Watchlist" button later
                    <button   
                    type = "button"
                    onClick = {() => removeFromWatchlist(anime)}  
                  >
                    Remove from Watchlist
                  </button> */} 

                  <button   
                  /*this should remove from watchlist*/
                  type="button"
                  onClick={() => handleRemoveFromWatchlist(anime?.anime_id)}  // passing a parameter, so we need to do () => first
                  >
                  Remove From Saved Watchlist
                  </button>

                  {similarAnimeById[anime.anime_id] 
                    ? (
                        <>
                          <button
                            type = "button"
                            onClick = {() => handleRemoveSimilarAnime(anime.anime_id)}  
                          >
                            View Less
                          </button> 
                        </>
                      )

                    : (
                        <>
                          <button
                            type = "button"
                            onClick = {() => handleViewSimilarAnime(anime)}  // happens only when button is clicked - since we have a parameter, we use () => here
                          >
                          View Similar Anime
                          </button> 
                        </>
                      )
                  }

                  {/* now this block of code will only run if similarAnimeById[anime.anime_id] exists (does the key exist in there, checks by seeing if the value stored at that key exists). The && means if the statement on the left is correct,
                  execute what's on the right, here the code chunk in the parentheses. Also needed to put everything inside <> and </> since React needs only 1 single parent element. without that fragment, I have multiple */}
                  {similarAnimeById[anime.anime_id] &&
                  (
                    <>
                      <p>Similar Anime: </p>    {/* this is JSX, so it goes directly in the return */}
                      {similarAnimeById[anime.anime_id].map(similarAnime => (<li>{similarAnime}</li>))}   {/* this line is JavaScript, so it must be wrapped inside {} in this return. Loop through all values in the list and display them in a list format
                      For example, if it's ["Bleach", "Naruto"], then display them with bullets on separate lines */}
                    </>
                  )
                  }

                  <p>Genres: </p> {/* <p> = Paragraph, used for normal text*/}
                  <ul>    {/* <ul> = Unordered List, creates a bulleted list container*/}
                    {anime?.genres?.map((genre) => (<li>{genre.name}</li>))}   {/* <li> = list item, each bullet inside a <ul> */}
                  </ul>

                  <p>Synopsis: </p>
                  <p>
                    {anime?.synopsis}
                  </p>

                  <p>Images: </p>

                  {/* alt is what shows if the src does not work */}
                  <img
                    src = {anime?.images}
                    alt = {anime?.title}  
                  />
                </div>
              ))
            }
          </>
        )
        } 
      

        
          
          
      

      </section>  {/* this marks the end of the section that starts with section id="center". This is the section that will be edited.*/}
          {/*everything below is just Vite starter content: links, icons, and layout. most of it will be deleted later*/}
          <div className="ticks"></div>

          <section id="next-steps">
            <div id="docs">
              <svg className="icon" role="presentation" aria-hidden="true">
                <use href="/icons.svg#documentation-icon"></use>
              </svg>
              <h2>Documentation</h2>
              <p>Your questions, answered</p>
              <ul>
                <li>
                  <a href="https://vite.dev/" target="_blank">
                    <img className="logo" src={viteLogo} alt="" />
                    Explore Vite
                  </a>
                </li>
                <li>
                  <a href="https://react.dev/" target="_blank">
                    <img className="button-icon" src={reactLogo} alt="" />
                    Learn more
                  </a>
                </li>
              </ul>
            </div>
            <div id="social">
              <svg className="icon" role="presentation" aria-hidden="true">
                <use href="/icons.svg#social-icon"></use>
              </svg>
              <h2>Connect with us</h2>
              <p>Join the Vite community</p>
              <ul>
                <li>
                  <a href="https://github.com/vitejs/vite" target="_blank">
                    <svg
                      className="button-icon"
                      role="presentation"
                      aria-hidden="true"
                    >
                      <use href="/icons.svg#github-icon"></use>
                    </svg>
                    GitHub
                  </a>
                </li>
                <li>
                  <a href="https://chat.vite.dev/" target="_blank">
                    <svg
                      className="button-icon"
                      role="presentation"
                      aria-hidden="true"
                    >
                      <use href="/icons.svg#discord-icon"></use>
                    </svg>
                    Discord
                  </a>
                </li>
                <li>
                  <a href="https://x.com/vite_js" target="_blank">
                    <svg
                      className="button-icon"
                      role="presentation"
                      aria-hidden="true"
                    >
                      <use href="/icons.svg#x-icon"></use>
                    </svg>
                    X.com
                  </a>
                </li>
                <li>
                  <a href="https://bsky.app/profile/vite.dev" target="_blank">
                    <svg
                      className="button-icon"
                      role="presentation"
                      aria-hidden="true"
                    >
                      <use href="/icons.svg#bluesky-icon"></use>
                    </svg>
                    Bluesky
                  </a>
                </li>
              </ul>
            </div>
          </section>

          <div className="ticks"></div>
          <section id="spacer"></section>
        </>
        );
}

        // this line allows main.jsx to import this component when it does import App from './App.jsx' in main.jsx
        export default App
