import React, { useState } from 'react'

export default function UploadDocs() {
  const [file, setFile] = useState(null)
  const [message, setMessage] = useState('')

  const handleFileChange = (e) => {
    setFile(e.target.files[0])
  }

  const handleUpload = async () => {
    if (!file) return
    const formData = new FormData()
    formData.append('file', file)
    try {
    const response = await fetch(`${API_BASE}/upload`, {
        method: 'POST',
        body: formData
      })
      const data = await response.json()
      setMessage(data.message)
    } catch (error) {
      setMessage('Upload failed')
    }
  }

  return (
    <div className="p-4">
      <h2 className="text-2xl mb-4">Upload Documents</h2>
      <input type="file" onChange={handleFileChange} className="mb-4" />
      <button onClick={handleUpload} className="bg-blue-500 text-white px-4 py-2">Upload</button>
      {message && <p className="mt-4">{message}</p>}
    </div>
  )
}
