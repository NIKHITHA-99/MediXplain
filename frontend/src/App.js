import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import ReactMarkdown from 'react-markdown';
import axios from 'axios';
import './App.css';
import jsPDF from 'jspdf';

function App() {
  const [file, setFile] = useState(null);
  const [explanation, setExplanation] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: { 'application/pdf': ['.pdf'], 'image/*': ['.png', '.jpg', '.jpeg'] },
    maxFiles: 1,
    onDrop: (acceptedFiles) => {
      setFile(acceptedFiles[0]);
      setExplanation('');
      setError('');
    }
  });

  const analyzeReport = async () => {
    if (!file) return;
    setLoading(true);
    setError('');
    try {
      const formData = new FormData();
      formData.append('file', file);
      const response = await axios.post('/analyze', formData);
      if (response.data.error) {
        setError(response.data.error);
      } else {
        setExplanation(response.data.explanation);
      }
   } catch (err) {
  console.error('Full error:', err);
  if (err.response) {
    setError(`Status ${err.response.status}: ${JSON.stringify(err.response.data)}`);
  } else if (err.request) {
    setError(`No response from backend: ${err.message}`);
  } else {
    setError(`Error: ${err.message}`);
  }
}
    setLoading(false);
  };

  return (
    <div className="app">
      <header className="header">
        <div className="logo">🏥 MediXplain</div>
        <p className="tagline">Your Medical Reports, Simply Explained</p>
      </header>

      <main className="main">
        <div className="upload-section">
          <h2>Upload Your Medical Report</h2>
          <p className="subtitle">PDF or Image (blood test, MRI, X-ray, lab report)</p>

          <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''} ${file ? 'has-file' : ''}`}>
            <input {...getInputProps()} />
            {file ? (
              <div className="file-info">
                <span className="file-icon">📄</span>
                <span className="file-name">{file.name}</span>
                <span className="file-size">{(file.size / 1024).toFixed(1)} KB</span>
              </div>
            ) : (
              <div className="drop-text">
                <span className="drop-icon">⬆️</span>
                <p>Drag & drop your report here</p>
                <p className="or">or click to browse</p>
              </div>
            )}
          </div>

          {file && (
            <button className="analyze-btn" onClick={analyzeReport} disabled={loading}>
              {loading ? '🔍 Analyzing...' : '🔍 Explain My Report'}
            </button>
          )}
        </div>

        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>AI is reading your report...</p>
          </div>
        )}

        {error && (
          <div className="error">❌ {error}</div>
        )}

        {explanation && (
          <div className="result">
            <div className="result-header">
              <h2>📋 Your Report Explained</h2>
              <div style={{display:'flex', gap:'10px'}}>
  <button className="copy-btn" onClick={() => navigator.clipboard.writeText(explanation)}>
    📋 Copy
  </button>
  <button className="copy-btn" onClick={() => {
    const doc = new jsPDF();
    const lines = doc.splitTextToSize(explanation, 180);
    let y = 20;
    doc.setFontSize(16);
    doc.setFont('helvetica', 'bold');
    doc.text('MediXplain - Medical Report Explanation', 15, y);
    y += 10;
    doc.setFontSize(10);
    doc.setFont('helvetica', 'normal');
    doc.text(`Generated: ${new Date().toLocaleDateString()}`, 15, y);
    y += 10;
    doc.setFontSize(11);
    lines.forEach(line => {
      if (y > 280) {
        doc.addPage();
        y = 20;
      }
      doc.text(line, 15, y);
      y += 7;
    });
    doc.save('medical_report_explanation.pdf');
  }}>
    ⬇️ Download PDF
  </button>
</div>
              
                          </div>
            <div className="explanation">
              <ReactMarkdown>{explanation}</ReactMarkdown>
            </div>
          </div>
        )}
      </main>

      <footer className="footer">
        <p>⚠️ MediXplain is for educational purposes only. Always consult your doctor.</p>
      </footer>
    </div>
  );
}

export default App;