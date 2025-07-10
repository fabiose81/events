import React from 'react';
import { BrowserRouter, Route, Routes, Navigate } from 'react-router-dom'
import Login from './pages/Login';
import SignUp from './pages/SignUp';
import Event from './pages/Event';
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <React.Fragment>
        <Routes>
          <Route path="/" element={<Navigate replace to="/login" />} exact />
          <Route path="/login" element={<Login />} />
          <Route path="/event" element={<Event />} />
          <Route path="/sign-up" element={<SignUp />} />
        </Routes>
      </React.Fragment>
    </BrowserRouter>
  );
}

export default App;