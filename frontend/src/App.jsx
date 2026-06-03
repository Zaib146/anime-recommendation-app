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

Right now it returns:

Get Started
Count is 0
Documentation

Later it will return:

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

  //Component is a reuasable UI function. It returns what should appear on the page
  const [anime, setAnime] = useState("")   
  //this creates state. Original - count = current value, setCount = function used to change the value, 0 = starting value
  //now, anime is current value for anime. setAnime is the value anime will be updated to. "" is the starting value for anime. same logic for line below
  const [recommendations, setRecommendations] = useState([])

  async function handleGetRecommendations() 
  //async means this function will wait for something that takes time. This is because fetch with the url takes time.
  {
    const animeName = encodeURIComponent(anime) //Changes "One Piece" to "One%20Piece" in actual url, since url does not like spaces
    const url = "http://localhost:8000/recommendations/" + animeName
    const response = await fetch(url)   // await means pause this function until results come back, literally wait for results. 
    // here FastAPI is listening on port 8000, so it receives the request. App.jsx does not access backend files directly. 
    // App.jsx sends an HTTP request to the backend server. When React uses fetch, React is asking FastAPI for data automatically.
    const data = await response.json()    //parse json data into python data, store that in "data"
    setRecommendations(data)      // change recommendations to value in data variable
    console.log(data)   // this is to print in console tab in F12 to test. will remove later

  }

  return (    // return sends the JSX back to the browser
    <>    {/*This is a React Fragment. It lets you return multiple elements without wrapping everything in an extra <div></div>*/}
      <section id="center">   {/* This creates a page section. The id="center" connects to CSS styling */}
        <div className="hero">  {/* in React, we use className instead of HTML’s class. This connects the div to CSS styles named .hero*/}
          {/* these 3 lines display the imported images. The {heroImg} syntax means: “use the JavaScript variable named heroImg*/}
          <img src={heroImg} className="base" width="170" height="179" alt="" />
          <img src={reactLogo} className="framework" alt="React logo" />
          <img src={viteLogo} className="vite" alt="Vite logo" />
        </div>
        <div>
          <h1>Anime Recommendation App</h1>  {/* this displays the big title*/}
          <p>
            What is your favorite anime?   {/*This displays the starter instruction text. <code> just styles text like code.*/}
          </p>
        <input 
          value = {anime}
          onChange = {(event) => setAnime(event.target.value)}
          /*onChange changes the value of anime for each keystroke as it's entered, not when the button Get Recommendations is clicked. 
          Anime variable is already change to new value by then*/
        />

        {/*Anime is {anime} - this shows the state update if needed*/}

        </div>
        <button
        /*this should get recommendations*/
          type="button"
          onClick = {handleGetRecommendations}  //when the user clicks Get Recommendations, it calls this function
        >
          Get Recommendations
        </button>

        <p>Title: {recommendations[1]?.title}</p>   {/*experimenting with this line to see if React can render the information onto the page.
        Right now, information shows in console tab of F12, which is good.*/}

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
  )
}

// this line allows main.jsx to import this component when it does import App from './App.jsx' in main.jsx
export default App
