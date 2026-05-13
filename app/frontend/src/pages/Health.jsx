import React, { useEffect, useState } from 'react'
import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE_URL || ''

export default function Health(){
  const [status, setStatus] = useState(null)

  useEffect(()=>{
    axios.get(`${API_BASE}/health`).then(r=>setStatus(r.data)).catch(e=>setStatus({error: e.message}))
  },[])

  return (
    <section className="container">
      <h2>Health</h2>
      <div className="card result">
        <pre>{status ? JSON.stringify(status, null, 2) : 'Checking...'}</pre>
      </div>
    </section>
  )
}
