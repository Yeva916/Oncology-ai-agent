import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Nav from './components/Nav'
import Home from './pages/Home'
import Analyze from './pages/Analyze'
import Demo from './pages/Demo'
import Health from './pages/Health'

export default function App(){
  return (
    <div className="app">
      <Nav />
      <main>
        <Routes>
          <Route path="/" element={<Home/>} />
          <Route path="/analyze" element={<Analyze/>} />
          <Route path="/demo" element={<Demo/>} />
          <Route path="/health" element={<Health/>} />
        </Routes>
      </main>
    </div>
  )
}
