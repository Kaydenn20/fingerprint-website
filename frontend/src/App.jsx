import { Routes, Route, Link, useLocation, Navigate } from 'react-router-dom'
import { useState } from 'react'
import About from './page/About'
import Prediction from './components/Prediction'
import Home from './components/Home'
import Contact from './page/Contact'
import Dashboard from './components/Dashboard'
import Landing from './page/Landing'
import './App.css'

function App() {
  const location = useLocation();
  const isLanding = location.pathname === '/';
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const toggleMobileMenu = () => {
    setMobileMenuOpen(!mobileMenuOpen);
  };

  const closeMobileMenu = () => {
    setMobileMenuOpen(false);
  };

  return (
    <div className="app">
      {!isLanding && location.pathname !== '/prediction' && (
        <nav className="navbar">
          <div className="nav-brand">
            <span className="brand-icon">🏥</span>
            <span>Medical Fingerprint System</span>
          </div>
          
          {/* Mobile menu button */}
          <button 
            className="mobile-menu-toggle"
            onClick={toggleMobileMenu}
            aria-label="Toggle mobile menu"
          >
            <span className={`hamburger ${mobileMenuOpen ? 'open' : ''}`}></span>
          </button>

          <ul className={`nav-links ${mobileMenuOpen ? 'mobile-open' : ''}`}>
            <li><Link to="/home" onClick={closeMobileMenu}>Home</Link></li>
            <li><Link to="/about" onClick={closeMobileMenu}>About</Link></li>
            <li><Link to="/contact" onClick={closeMobileMenu}>Contact</Link></li>
            <li><Link to="/dashboard" onClick={closeMobileMenu}>Dashboard</Link></li>
          </ul>
        </nav>
      )}
      
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/home" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/prediction" element={<Prediction />} />
      </Routes>

      {!isLanding && (
        <footer className="footer">
          <div className="footer-content">
            <div className="footer-section">
              <h3>Quick Links</h3>
              <ul>
                <li><Link to="/home">Home</Link></li>
                <li><Link to="/about">About</Link></li>
                <li><Link to="/contact">Contact</Link></li>
                <li><Link to="/dashboard">Dashboard</Link></li>
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
      )}
    </div>
  )
}

export default App
