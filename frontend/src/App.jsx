import React from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import Chat from './components/Chat.jsx'
import Upload from './components/Upload.jsx'
import UploadDocs from './components/UploadDocs.jsx'

export default function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100 p-4">
        <h1 className="text-3xl font-bold mb-6">Lumina AI RAG</h1>
        <nav className="mb-6">
          <Link to="/" className="mr-4 text-blue-600 hover:text-blue-800">Home</Link>
          <Link to="/upload" className="mr-4 text-blue-600 hover:text-blue-800">Upload Docs</Link>
          <Link to="/chat" className="mr-4 text-blue-600 hover:text-blue-800">Chat</Link>
        </nav>
        <Routes>
          <Route path="/" element={<><Upload /><Chat /></>} />
          <Route path="/upload" element={<UploadDocs />} />
          <Route path="/chat" element={<Chat />} />
        </Routes>
      </div>
    </Router>
  )
}
