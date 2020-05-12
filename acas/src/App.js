import React from 'react';
// import logo from './assets/logo.svg';

import { Switch, Route, Redirect } from "react-router-dom";
import { BrowserRouter as Router } from "react-router-dom";

import Home from "./pages/Home.js";

import './App.css';

function App() {
  return (
    <div className="App">
      <Router>
        <Switch>
					<Route path="/home" component={Home} />
					<Redirect exact from="/" to="/home" />
        </Switch>
			</Router>
      {/* <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
      </header> */}
    </div>  
  );
}

export default App;
