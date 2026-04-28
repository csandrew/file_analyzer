import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState(null);

  const onDrop = useCallback((acceptedFiles) => {
    setFile(acceptedFiles[0]);
    setError(null);
    setAnalysisResult(null);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    maxSize: 10485760,
    multiple: false
  });

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setUploading(true);
    setError(null);

    try {
      const response = await axios.post('http://localhost:8000/api/documents/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      setAnalysisResult(response.data);
      console.log('Upload successful:', response.data);
    } catch (err) {
      console.error('Upload error:', err);
      setError(err.response?.data?.error || err.message || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>📁 File Analyzer</h1>
        <p>Upload any document for instant analysis</p>
      </header>

      <div className="container">
        <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`}>
          <input {...getInputProps()} />
          {isDragActive ? (
            <p>Drop your file here...</p>
          ) : (
            <div className="dropzone-content">
              <p>📤 Drag & drop a file here</p>
              <p className="small">or click to browse</p>
              <p className="small">Max size: 10MB</p>
              <p className="small">Supported: PDF, Images, Word, Excel, Text, CSV</p>
            </div>
          )}
        </div>

        {file && (
          <div className="file-info">
            <h3>Selected File:</h3>
            <p>📄 {file.name}</p>
            <p>📏 {(file.size / 1024).toFixed(2)} KB</p>
            <button 
              onClick={handleUpload} 
              disabled={uploading}
              className="upload-button"
            >
              {uploading ? 'Analyzing...' : 'Analyze File'}
            </button>
          </div>
        )}

        {error && (
          <div className="error">
            <h3>❌ Error</h3>
            <p>{error}</p>
          </div>
        )}

        {analysisResult && (
          <div className="results">
            <h2>📊 Analysis Results</h2>
            
            <div className="result-section">
              <h3>Basic Information</h3>
              <p><strong>File Name:</strong> {analysisResult.original_name}</p>
              <p><strong>File Size:</strong> {(analysisResult.file_size / 1024).toFixed(2)} KB</p>
              <p><strong>File Type:</strong> {analysisResult.file_type}</p>
              <p><strong>MIME Type:</strong> {analysisResult.mime_type}</p>
              <p><strong>Status:</strong> {analysisResult.status}</p>
            </div>

            {analysisResult.analysis && (
              <div className="result-section">
                <h3>Detailed Analysis</h3>
                <pre className="analysis-details">
                  {JSON.stringify(analysisResult.analysis, null, 2)}
                </pre>
              </div>
            )}

            {analysisResult.id && (
              <p className="file-id">Document ID: {analysisResult.id}</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
