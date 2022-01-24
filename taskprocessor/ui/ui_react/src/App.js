//Imports
import React, { Component } from "react";
import Canvas from "./components/Canvas";
import Entities from "./components/Entities";
import Properties from "./components/Properties";

// Styles
import './styles/PageStyles.css'

// Main function
// Returns all of the React Components
class App extends Component{
  render() {
    return (
      <>
      <div className='grid-container'>
          <div className='EntitiesPanel'>
            <Entities />
          </div>
          <div className='NodeCanvas'> 
            <Canvas />
          </div>
          <div className='NodeProperties'>
            <Properties />
          </div>
        </div>
      </>
    )
  }
}
export default App;
