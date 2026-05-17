import React from 'react'

export default function TrialResult({ result }) {
  if (!result) return null

  const normalizeText = (text) => {
    if (!text) return ''

    return String(text)
      .replace(/\\n/g, '\n')
      .replace(/\\r/g, '\r')
      .replace(/\r/g, '')
      .replace(/^"|"$/g, '')
      .trim()
  }

  const extractSection = (block, startLabel, endLabels = []) => {
    const startIndex = block.indexOf(startLabel)
    if (startIndex < 0) return ''

    const remainder = block.slice(startIndex + startLabel.length)
    const endIndex = endLabels
      .map(label => remainder.indexOf(label))
      .filter(index => index >= 0)
      .sort((left, right) => left - right)[0]

    return (endIndex !== undefined ? remainder.slice(0, endIndex) : remainder).trim()
  }

  const parseResponse = (text) => {
    const normalized = normalizeText(text)
    const finalSummaryMatch = normalized.match(/\*\*FINAL SUMMARY:\*\*([\s\S]*)$/i) || normalized.match(/FINAL SUMMARY:\s*([\s\S]*)$/i)
    const finalSummary = finalSummaryMatch ? finalSummaryMatch[1].trim() : ''
    const trialsSection = finalSummaryMatch ? normalized.slice(0, finalSummaryMatch.index).trim() : normalized

    const trialBlocks = trialsSection
      .split(/\n---\n/)
      .map(block => block.trim())
      .filter(Boolean)

    const trials = trialBlocks.map(block => {
      const trialIdMatch = block.match(/^Trial ID:\s*(.+)$/m)
      const relevanceMatch = block.match(/^Relevance:\s*(.+)$/m)

      return {
        trialId: trialIdMatch ? trialIdMatch[1].trim() : 'Unknown',
        relevance: relevanceMatch ? relevanceMatch[1].trim() : 'Unknown',
        summary: extractSection(block, 'Clinical Summary:', ['Eligibility Assessment:', 'Final Judgment:']),
        eligibilityAssessment: extractSection(block, 'Eligibility Assessment:', ['Final Judgment:']),
        judgment: extractSection(block, 'Final Judgment:', []),
      }
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

  const renderParagraphs = (text) => {
    if (!text) return <p className="empty-text">Not specified</p>

    return text.split(/\n\n+/).map((paragraph, idx) => {
      const lines = paragraph.split('\n')

      return (
        <p key={idx} className="summary-paragraph">
          {lines.map((line, lineIdx) => (
            <React.Fragment key={lineIdx}>
              {line.replace(/\*\*/g, '')}
              {lineIdx < lines.length - 1 ? <br /> : null}
            </React.Fragment>
          ))}
        </p>
      )
    })
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
              {renderParagraphs(trial.summary)}
            </div>

            <div className="trial-section">
              <h4>Eligibility Assessment</h4>
              <div className="eligibility-box">
                <span className="eligibility-icon">{getEligibilityIcon(trial.judgment)}</span>
                <div className="eligibility-copy">
                  {renderParagraphs(trial.eligibilityAssessment || trial.judgment)}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {finalSummary && (
        <div className="final-summary-box">
          <h3>Summary & Recommendation</h3>
          <div className="summary-content">
            {renderParagraphs(finalSummary)}
          </div>
        </div>
      )}
    </div>
  )
}
