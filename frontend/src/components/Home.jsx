import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api';
import '../App.css';

function Home() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl, setPreviewUrl] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleImageChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreviewUrl(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    setResult(null);
    if (selectedImage) {
      setLoading(true);
      try {
        const formData = new FormData();
        formData.append('image', selectedImage);
        const response = await api.post('/predict', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });
        navigate('/prediction', { state: { imageUrl: previewUrl, prediction: response.data } });
      } catch (err) {
        setError(
          err.response?.data?.error || 'Failed to analyze fingerprint. Please try again.'
        );
      } finally {
        setLoading(false);
      }
    }
  };

  const handleReset = () => {
    setSelectedImage(null);
    setPreviewUrl('');
  };

  return (
    <div className="app-container">
      <div className="hero-section">
        <h1>Advanced Medical Fingerprint Recognition</h1>
        <p className="hero-subtitle">Secure and accurate patient identification for healthcare professionals</p>
      </div>
      <div className="upload-container">
        <div className="upload-header">
          <h2>Fingerprint Analysis</h2>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="upload-button-container">
            <label className="upload-button">
              <span className="upload-icon">📷</span>
              Choose Fingerprint Image
              <input
                type="file"
                accept="image/*"
                onChange={handleImageChange}
                className="file-input"
              />
            </label>
          </div>
          <div className="image-preview">
            {previewUrl ? (
              <img src={previewUrl} alt="Fingerprint preview" className="preview-image" />
            ) : (
              <div className="placeholder">
                <span className="placeholder-icon">👆</span>
                <p>No fingerprint image selected</p>
                <p className="placeholder-subtext">Please upload a clear fingerprint image</p>
              </div>
            )}
          </div>
          <div className="button-group">
            <button type="submit" className="submit-button" disabled={!selectedImage || loading}>
              <span className="button-icon">🔍</span>
              {loading ? 'Analyzing...' : 'Analyze Fingerprint'}
            </button>
            <button type="button" onClick={handleReset} className="reset-button" disabled={loading}>
              <span className="button-icon">🔄</span>
              Reset
            </button>
          </div>
        </form>
        {error && <div className="error-message">{error}</div>}
      </div>
      <div className="features-section">
        <h2>Key Features</h2>
        <div className="features-grid">
          <div className="feature-card">
            <span className="feature-icon">🔒</span>
            <h3>Secure</h3>
            <p>HIPAA-compliant data protection</p>
          </div>
          <div className="feature-card">
            <span className="feature-icon">⚡</span>
            <h3>Fast</h3>
            <p>Quick and accurate identification</p>
          </div>
          <div className="feature-card">
            <span className="feature-icon">🎯</span>
            <h3>Accurate</h3>
            <p>99.9% matching accuracy</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home; 