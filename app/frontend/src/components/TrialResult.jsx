import React from 'react'

export default function TrialResult({ result }) {
  if (!result) return null

  // Parse result text into trials and summary
  const parseResponse = (text) => {
    const trials = []
    const finalSummaryMatch = text.match(/\*\*FINAL SUMMARY:\*\*(.+)$/s)
    const finalSummary = finalSummaryMatch ? finalSummaryMatch[1].trim() : ''
    
    // Split by --- to get trial blocks
    const trialBlocks = text.split(/---/).filter(block => block.trim() && !block.includes('FINAL SUMMARY'))
    
    trialBlocks.forEach(block => {
      const lines = block.trim().split('\n')
      
      // Extract Trial ID
      const idLine = lines.find(l => l.startsWith('Trial ID:'))
      const trialId = idLine ? idLine.replace('Trial ID:', '').trim() : 'Unknown'
      
      // Extract Relevance
      const relLine = lines.find(l => l.startsWith('Relevance:'))
      const relevance = relLine ? relLine.replace('Relevance:', '').trim() : 'Unknown'
      
      // Extract Clinical Summary
      const summaryIdx = lines.findIndex(l => l.startsWith('Clinical Summary:'))
      let summary = ''
      if (summaryIdx >= 0) {
        summary = lines[summaryIdx].replace('Clinical Summary:', '').trim()
      }
      
      // Extract Final Judgment
      const judgmentIdx = lines.findIndex(l => l.startsWith('Final Judgment:'))
      let judgment = ''
      if (judgmentIdx >= 0) {
        judgment = lines.slice(judgmentIdx).join('\n').replace('Final Judgment:', '').trim()
        // Stop at next section
        const nextSection = judgment.indexOf('\n\n')
        if (nextSection > 0) judgment = judgment.substring(0, nextSection)
      }
      
      trials.push({ trialId, relevance, summary, judgment })
    })
    
    return { trials, finalSummary }
  }

  const { trials, finalSummary } = parseResponse(result)
  
  const getRelevanceBadge = (relevance) => {
    const colors = {
      'Low': '#ef4444',
      'Medium': '#f59e0b',
      'High': '#10b981'
    }
    return colors[relevance] || '#6b7280'
  }

  const getEligibilityIcon = (judgment) => {
    const lower = judgment.toLowerCase()
    if (lower.includes('ineligible')) return '❌'
    if (lower.includes('treatment-naïve') || lower.includes('clear mismatch')) return '❌'
    if (lower.includes('strong candidate') || lower.includes('meets')) return '✅'
    if (lower.includes('medium') || lower.includes('uncertain') || lower.includes('primary uncertainty')) return '⚠️'
    return '✅'
  }

  return (
    <div className="trial-results">
      <div className="results-header">
        <h3>Clinical Trial Analysis</h3>
        <p>{trials.length} trial(s) analyzed</p>
      </div>

      <div className="trials-grid">
        {trials.map((trial, idx) => (
          <div key={idx} className="trial-card">
            <div className="trial-header">
              <div className="trial-id">{trial.trialId}</div>
              <div 
                className="relevance-badge"
                style={{ backgroundColor: getRelevanceBadge(trial.relevance) }}
              >
                {trial.relevance}
              </div>
            </div>

            <div className="trial-section">
              <h4>Summary</h4>
              <p>{trial.summary}</p>
            </div>

            <div className="trial-section">
              <h4>Eligibility Assessment</h4>
              <div className="eligibility-box">
                <span className="eligibility-icon">{getEligibilityIcon(trial.judgment)}</span>
                <p>{trial.judgment}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {finalSummary && (
        <div className="final-summary-box">
          <h3>Summary & Recommendation</h3>
          <div className="summary-content">
            {finalSummary.split('\n\n').map((para, idx) => (
              <p key={idx} className="summary-paragraph">
                {para.replace(/\*\*/g, '').split('\n').map((line, i) => (
                  <React.Fragment key={i}>
                    {line}
                    <br />
                  </React.Fragment>
                ))}
              </p>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
