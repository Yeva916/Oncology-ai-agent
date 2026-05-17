import React from 'react'
import { NavLink } from 'react-router-dom'

export default function Nav(){
  return (
    <nav className="nav">
      <div className="brand">Onco Agent</div>
      <div className="links">
        <NavLink to="/">Home</NavLink>
        <NavLink to="/analyze">Analyze</NavLink>
        <NavLink to="/demo">Demo</NavLink>
        <NavLink to="/health">Health</NavLink>
      </div>
    </nav>
  )
}
