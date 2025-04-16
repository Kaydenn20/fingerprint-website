import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import About from './About'
import './App.css'

function App() {
  const [selectedImage, setSelectedImage] = useState(null)
  const [previewUrl, setPreviewUrl] = useState('')

  const handleImageChange = (event) => {
    const file = event.target.files[0]
    if (file) {
      setSelectedImage(file)
      const reader = new FileReader()
      reader.onloadend = () => {
        setPreviewUrl(reader.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleSubmit = (event) => {
    event.preventDefault()
    if (selectedImage) {
      console.log('Submitting fingerprint image:', selectedImage)
    }
  }

  const handleReset = () => {
    setSelectedImage(null)
    setPreviewUrl('')
  }

  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <div className="nav-brand">
            <span className="brand-icon">🏥</span>
            <span>Medical Fingerprint System</span>
          </div>
          <ul className="nav-links">
            <li><Link to="/" className="active">Home</Link></li>
            <li><Link to="/about">About</Link></li>
            <li><Link to="/support">Support</Link></li>
          </ul>
        </nav>
        
        <Routes>
          <Route path="/" element={
            <div className="app-container">
              <div className="hero-section">
                <h1>Advanced Medical Fingerprint Recognition</h1>
                <p className="hero-subtitle">Secure and accurate patient identification for healthcare professionals</p>
              </div>
              
              <div className="upload-container">
                <div className="upload-header">
                  <h2>Upload Fingerprint</h2>
                  <p className="upload-instructions">Please upload a clear fingerprint image for analysis</p>
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
                    <button type="submit" className="submit-button" disabled={!selectedImage}>
                      <span className="button-icon">🔍</span>
                      Analyze Fingerprint
                    </button>
                    <button type="button" onClick={handleReset} className="reset-button">
                      <span className="button-icon">🔄</span>
                      Reset
                    </button>
                  </div>
                </form>
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
          } />
          <Route path="/about" element={<About />} />
        </Routes>

        <footer className="footer">
          <div className="footer-content">
            <div className="footer-section">
              <h3>Quick Links</h3>
              <ul>
                <li><Link to="/">Home</Link></li>
                <li><Link to="/about">About</Link></li>
                <li><Link to="/support">Support</Link></li>
                <li><a href="#">Privacy Policy</a></li>
              </ul>
            </div>
            
            <div className="footer-section">
              <h3>Contact Us</h3>
              <p>Email: support@medicalfingerprint.com</p>
              <p>Phone: +1 (555) 123-4567</p>
              <div className="social-links">
                <a href="#" className="social-icon">Facebook</a>
                <a href="#" className="social-icon">Twitter</a>
                <a href="#" className="social-icon">LinkedIn</a>
              </div>
            </div>
            
            <div className="footer-section">
              <h3>Newsletter</h3>
              <p>Subscribe to our newsletter for updates</p>
              <div className="newsletter-form">
                <input type="email" placeholder="Enter your email" />
                <button type="submit">Subscribe</button>
              </div>
            </div>
          </div>
          <div className="footer-bottom">
            <p>&copy; 2024 Medical Fingerprint System. All rights reserved.</p>
          </div>
        </footer>
      </div>
    </Router>
  )
}

export default App
