import React, { useState } from 'react'
import axios from 'axios'
import TrialResult from '../components/TrialResult'

const API_BASE = import.meta.env.VITE_API_BASE_URL || ''

export default function Analyze(){
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  async function submit(e){
    e.preventDefault()
    setLoading(true)
    setResult(null)
    setError(null)
    try{
      const resp = await axios.post(`${API_BASE}/analyze`, { query })
      setResult(resp.data?.response || resp.data)
    }catch(err){
      setError(err.message)
    }finally{
      setLoading(false)
    }
  }

  return (
    <section className="container">
      <h2>Analyze Clinical Query</h2>
      <form onSubmit={submit} className="card">
        <label>Enter clinical query for patient eligibility analysis:</label>
        <textarea 
          value={query} 
          onChange={e=>setQuery(e.target.value)} 
          rows={6}
          placeholder="E.g., Patient with advanced non-small cell lung cancer, age 65, ECOG performance status 1..."
        />
        <div className="actions">
          <button type="submit" disabled={loading || !query.trim()}>
            {loading? 'Analyzing...':'Run Analysis'}
          </button>
        </div>
      </form>

      {error && (
        <div className="card error-box">
          <h3>Error</h3>
          <p>{error}</p>
        </div>
      )}

      {result && typeof result === 'string' ? (
        <TrialResult result={result} />
      ) : result ? (
        <div className="card result">
          <h3>Result</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      ) : null}
    </section>
  )
}
