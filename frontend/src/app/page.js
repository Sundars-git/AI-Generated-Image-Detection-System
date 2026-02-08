"use client";

import { useState, useRef } from 'react';
import Head from 'next/head';
import Image from 'next/image';

export default function Home() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [showHeatmap, setShowHeatmap] = useState(false);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      processFile(file);
    }
  };

  const processFile = (file) => {
    setError(null);
    setResult(null);
    if (!file.type.startsWith('image/')) {
      setError('Please upload a valid image file.');
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      setError('Image size too large (max 10MB).');
      return;
    }

    setSelectedFile(file);
    const reader = new FileReader();
    reader.onloadend = () => {
      setImagePreview(reader.result);
    };
    reader.readAsDataURL(file);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      processFile(e.dataTransfer.files[0]);
    }
  };

  const handleDetect = async () => {
    if (!selectedFile) return;

    setIsLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
      const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.statusText}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || 'Failed to analyze image.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <Head>
        <title>AI Image Detector</title>
        <meta name="description" content="Detect AI-generated images vs Real photos" />
      </Head>

      <main className="main">
        <header className="header">
          <h1>AI vs Real Image Detector</h1>
          <p>Upload an image to analyze its authenticity with AI-powered transparency.</p>
        </header>

        <section 
          className="upload-section"
          onDragOver={handleDragOver}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
        >
          <input 
            type="file" 
            ref={fileInputRef} 
            onChange={handleFileChange} 
            accept="image/*" 
            style={{ display: 'none' }} 
          />
          
          {!imagePreview ? (
            <div className="upload-placeholder">
              <span className="icon">📁</span>
              <p>Drag & Drop or Click to Upload Image</p>
              <span className="subtext">Supported formats: JPG, PNG, WebP (Max 10MB)</span>
            </div>
          ) : (
            <div className="preview-container">
              <img 
                src={showHeatmap && result?.heatmap_image ? `data:image/jpeg;base64,${result.heatmap_image}` : imagePreview} 
                alt="Uploaded Preview" 
                className="image-preview" 
              />
              {result?.heatmap_image && (
                  <button 
                    className="heatmap-toggle" 
                    onClick={(e) => { e.stopPropagation(); setShowHeatmap(!showHeatmap); }}
                  >
                    {showHeatmap ? 'Hide Heatmap' : 'Show Heatmap'}
                  </button>
              )}
            </div>
          )}
        </section>

        {error && <div className="error-message">{error}</div>}

        <button 
          className="detect-button" 
          onClick={handleDetect} 
          disabled={!selectedFile || isLoading}
        >
          {isLoading ? 'Analyzing...' : 'Detect Image'}
        </button>

        {result && (
          <section className="results-section">
            <div className="result-card">
              <h2>Analysis Result</h2>
              
              <div className="probability-container">
                <div className="prob-item">
                  <span className="label">AI Generated</span>
                  <div className="progress-bar-bg">
                    <div 
                      className="progress-bar-fill ai" 
                      style={{ width: `${(result.ai_probability * 100).toFixed(1)}%` }}
                    ></div>
                  </div>
                  <span className="value">{(result.ai_probability * 100).toFixed(1)}%</span>
                </div>

                <div className="prob-item">
                  <span className="label">Real Photo</span>
                  <div className="progress-bar-bg">
                    <div 
                      className="progress-bar-fill real" 
                      style={{ width: `${(result.real_probability * 100).toFixed(1)}%` }}
                    ></div>
                  </div>
                  <span className="value">{(result.real_probability * 100).toFixed(1)}%</span>
                </div>
              </div>

              <div className="verdict">
                Verdict: 
                <span className={result.ai_probability > 0.5 ? 'verdict-ai' : 'verdict-real'}>
                  {result.ai_probability > 0.5 ? ' Likely AI-Generated' : ' Likely Real'}
                </span>
                <span className="confidence">
                 (Confidence: {(Math.max(result.ai_probability, result.real_probability) * 100).toFixed(1)}%)
                </span>
              </div>
              
              <div className="disclaimer">
                <p>⚠️ AI detection is probabilistic and not 100% accurate. Heatmap visualizes regions that influenced the decision.</p>
              </div>
            </div>
          </section>
        )}
      </main>
      
      <footer className="footer">
        <p>Built with Next.js, FastAPI, and PyTorch (CLIP)</p>
      </footer>
    </div>
  );
}
