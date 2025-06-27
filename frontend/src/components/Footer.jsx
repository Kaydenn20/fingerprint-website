import React from 'react';
import { Link } from 'react-router-dom';
import '../css/Footer.css';

const Footer = () => {
  return (
    <footer className="footer-medical">
      <div className="footer-content-medical">
        <div className="footer-section-medical">
          <h3>Quick Links</h3>
          <ul>
            <li><Link to="/">Home</Link></li>
          </ul>
        </div>

        <div className="footer-section-medical">
          <h3>Contact Info</h3>
          <ul>
            <li>Email: info@fingerprintsystem.com</li>
            <li>Phone: +1 (555) 123-4567</li>
            <li>Address: 123 Medical Center Drive</li>
            <li>City, State 12345</li>
          </ul>
          <div className="social-links-medical">
           
          </div>
        </div>

        <div className="footer-section-medical">
          <h3>Newsletter</h3>
          <p>Stay updated with our latest medical technology advances.</p>
          <form className="newsletter-form-medical">
            <input type="email" placeholder="Enter your email" />
            <button type="submit">Subscribe</button>
          </form>
        </div>
      </div>
      
      <div className="footer-bottom-medical">
        <p>&copy; {new Date().getFullYear()} Medical Fingerprint System. All rights reserved.</p>
      </div>
    </footer>
  );
};

export default Footer; 