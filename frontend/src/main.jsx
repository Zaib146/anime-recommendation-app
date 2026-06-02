import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'   // bring in the app component from App.jsx

// this file finds the div in index.html and turns React on
// rarely touch this file
/*document.getElementById('root')) - this finds the <div id="root"></div> from index.html*/
/*render(<App />) - this puts the App component onto the page, after React is now running*/
// for main.jsx, put comments here above the render call, more professional

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
  
)
