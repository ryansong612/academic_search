import React from 'react';
import './App.css';
import Register from "./components/Register"
import RegisterSuccess from "./components/RegisterSuccess"
import Login from "./components/Login";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import LoginSuccess from "./components/LoginSuccess";
import Chat from "./components/Chat";
import Welcome from "./components/Welcome"
import PrivateRoute from "./components/PrivateRoute"

function App() {
  return (
    <div className="App" style={{display: 'flex', justifyContent: 'center'}}>
        <Router>
            <Routes>
                <Route path="/" element={<Welcome />}></Route>
                <Route path="/register" element={<Register />}></Route>
                <Route path="/register-success" element={<RegisterSuccess />}></Route>
                <Route path="/login-success" element={<LoginSuccess />}></Route>
                <Route path="/login" element={<Login />}></Route>
                <Route element={<PrivateRoute />}>
                    <Route path="/chat" element={<Chat />}></Route>
                </Route>
            </Routes>
        </Router>
    </div>


  );
}

export default App;
