import React, { useState } from 'react'
import axios from 'axios'
import TrialResult from '../components/TrialResult'

const API_BASE = import.meta.env.VITE_API_BASE_URL || ''

export default function Demo(){
  const [loading, setLoading] = useState(false)
  const [resp, setResp] = useState(null)
  const [error, setError] = useState(null)

  async function runDemo(){
    setLoading(true)
    setResp(null)
    setError(null)
    try{
      const r = await axios.get(`${API_BASE}/demo`)
      setResp(r.data?.response || r.data)
    }catch(err){
      setError(err.message)
    }finally{setLoading(false)}
  }

  return (
    <section className="container">
      <h2>Demo</h2>
      <p>Run a demo generation using the backend demo endpoint with sample clinical data.</p>
      <div className="actions">
        <button onClick={runDemo} disabled={loading}>{loading? 'Running...':'Run Demo'}</button>
      </div>

      {error && (
        <div className="card error-box">
          <h3>Error</h3>
          <p>{error}</p>
        </div>
      )}

      {resp && typeof resp === 'string' ? (
        <TrialResult result={resp} />
      ) : resp ? (
        <div className="card result">
          <h3>Demo Result</h3>
          <pre>{JSON.stringify(resp, null, 2)}</pre>
        </div>
      ) : null}
    </section>
  )
}
