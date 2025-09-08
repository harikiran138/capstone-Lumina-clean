import React, { useState } from 'react'
import API_BASE from '../api.js'

export default function Chat() {
  const [query, setQuery] = useState('')
  const [answer, setAnswer] = useState('')
  const [sources, setSources] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [queryHistory, setQueryHistory] = useState([])

  const handleQuery = async () => {
    if (!query.trim()) return

    setLoading(true)
    setError('')
    try {
      const response = await fetch(`${API_BASE}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      setAnswer(data.answer)
      setSources(data.sources || [])

      // Add to history
      setQueryHistory(prev => [...prev, {
        query,
        answer: data.answer,
        sources: data.sources || [],
        timestamp: new Date().toLocaleString()
      }])

    } catch (err) {
      setError('Failed to get response. Please try again.')
      console.error('Query error:', err)
    } finally {
      setLoading(false)
    }
  }

  const clearHistory = () => {
    setQueryHistory([])
    setAnswer('')
    setSources([])
    setQuery('')
  }

  return (
    <div className="mt-6">
      <h2 className="text-xl font-semibold mb-4">AI Document Assistant</h2>

      {/* Query Input */}
      <div className="mb-4">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask a question about your documents..."
          className="border p-3 w-full rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          onKeyPress={(e) => e.key === 'Enter' && handleQuery()}
        />
        <div className="flex gap-2 mt-2">
          <button
            onClick={handleQuery}
            disabled={loading || !query.trim()}
            className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {loading ? 'Searching...' : 'Ask Question'}
          </button>
          <button
            onClick={clearHistory}
            className="bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600"
          >
            Clear History
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {/* Current Answer */}
      {answer && (
        <div className="bg-white p-6 rounded-lg shadow-md mb-6">
          <h3 className="text-lg font-semibold mb-3 text-gray-800">Answer</h3>
          <div className="text-gray-700 leading-relaxed whitespace-pre-wrap">
            {answer}
          </div>
        </div>
      )}

      {/* Sources */}
      {sources.length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow-md mb-6">
          <h3 className="text-lg font-semibold mb-3 text-gray-800">
            Sources ({sources.length} found)
          </h3>
          <div className="space-y-2">
            {sources.map((source, index) => (
              <div key={index} className="bg-gray-50 p-3 rounded border-l-4 border-blue-500">
                <div className="text-sm text-gray-600">
                  Source {index + 1}
                </div>
                <div className="text-gray-800 mt-1">
                  {source}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Query History */}
      {queryHistory.length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold mb-3 text-gray-800">
            Query History ({queryHistory.length})
          </h3>
          <div className="space-y-4">
            {queryHistory.slice().reverse().map((item, index) => (
              <div key={index} className="border rounded-lg p-4 bg-gray-50">
                <div className="text-sm text-gray-500 mb-2">
                  {item.timestamp}
                </div>
                <div className="font-medium text-gray-800 mb-2">
                  Q: {item.query}
                </div>
                <div className="text-gray-700 mb-2">
                  A: {item.answer}
                </div>
                {item.sources.length > 0 && (
                  <div className="text-sm text-gray-600">
                    Sources: {item.sources.length} found
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
