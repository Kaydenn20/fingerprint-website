import React from 'react';
import './About.css';

function About() {
  return (
    <div className="about-container">
      <h1>About Our Fingerprint System</h1>
      
      <div className="about-section">
        <h2>Our Mission</h2>
        <p>
          We are dedicated to providing state-of-the-art fingerprint recognition technology
          that ensures security, accuracy, and convenience for all users.
        </p>
      </div>

      <div className="about-section">
        <h2>Technology</h2>
        <div className="tech-grid">
          <div className="tech-card">
            <h3>Advanced Recognition</h3>
            <p>Utilizing cutting-edge algorithms for precise fingerprint matching</p>
          </div>
          <div className="tech-card">
            <h3>Secure Storage</h3>
            <p>Your data is protected with industry-standard encryption</p>
          </div>
          <div className="tech-card">
            <h3>Fast Processing</h3>
            <p>Quick and efficient fingerprint analysis and verification</p>
          </div>
          <div className="tech-card">
            <h3>User-Friendly</h3>
            <p>Simple and intuitive interface for all users</p>
          </div>
        </div>
      </div>

      <div className="about-section">
        <h2>Our Team</h2>
        <div className="team-grid">
          <div className="team-member">
            <div className="member-avatar">JD</div>
            <h3>John Doe</h3>
            <p>Lead Developer</p>
          </div>
          <div className="team-member">
            <div className="member-avatar">AS</div>
            <h3>Alice Smith</h3>
            <p>Security Expert</p>
          </div>
          <div className="team-member">
            <div className="member-avatar">RJ</div>
            <h3>Robert Johnson</h3>
            <p>UI/UX Designer</p>
          </div>
        </div>
      </div>

      <div className="about-section">
        <h2>Contact Us</h2>
        <div className="contact-info">
          <p>Email: info@fingerprintsystem.com</p>
          <p>Phone: +1 (555) 123-4567</p>
          <p>Address: 123 Tech Street, Innovation City</p>
        </div>
      </div>
    </div>
  );
}

export default About; 