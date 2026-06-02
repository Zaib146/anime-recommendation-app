import { useState } from 'react'    // this imports useState, which lets Reach remember changing values. Here, it remembers the button count
//next 3 imports import image files so the component can display them later with <img src={...} />
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
//this imports the CSS styling for this component
import './App.css'

//to start frontend in terminal, get to frontend folder if need (cd frontend). Then type "npm run dev"

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

function App() {    // this line creats a React component named App
  //Component is a reuasable UI function. It returns what should appear on the page
  const [count, setCount] = useState(0)   //this creates state. count = current value, setCount = function used to change the value, 0 = starting value

  return (    // return sends the JSX back to the browser
    <>    {/*This is a React Fragment. It lets you return multiple elements without wrapping everything in an extra <div></div>*/}
      <section id="center">   {/* This creates a page section. The id="center" connects to CSS styling */}
        <div className="hero">  {/* n React, we use className instead of HTML’s class. This connects the div to CSS styles named .hero*/}
          {/* these 3 lines display the imported images. The {heroImg} syntax means: “use the JavaScript variable named heroImg*/}
          <img src={heroImg} className="base" width="170" height="179" alt="" />
          <img src={reactLogo} className="framework" alt="React logo" />
          <img src={viteLogo} className="vite" alt="Vite logo" />
        </div>
        <div>
          <h1>Get started</h1>  {/* this displays the big title*/}
          <p>
            Edit <code>src/App.jsx</code> and save to test <code>HMR</code>   {/*This displays the starter instruction text. 
            <code> just styles text like code.*/}
          </p>
        </div>
        <button
          type="button"
          className="counter"
          onClick={() => setCount((count) => count + 1)}
        >
          Count is {count}
          {/* this creates a button. which clicked, setCount((count) => count + 1), then React increases count by 1. 
          Then Count is {count} updates automatically*/}
        </button>
      </section>
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
