import React, { useState } from 'react'
import API_BASE from '../api.js'

export default function Upload() {
  const [file, setFile] = useState(null)
  const [message, setMessage] = useState('')

  const handleUpload = async () => {
    if (!file) return
    const formData = new FormData()
    formData.append('file', file)
    const response = await fetch(`${API_BASE}/ingest`, {
      method: 'POST',
      body: formData
    })
    const data = await response.json()
    setMessage(data.message)
  }

  return (
    <div className="mb-6">
      <h2 className="text-xl font-semibold mb-4">Upload File for Ingestion</h2>
      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
        className="mb-4"
      />
      <button onClick={handleUpload} className="bg-green-500 text-white px-4 py-2">Upload</button>
      <p className="mt-2">{message}</p>
    </div>
  )
}
