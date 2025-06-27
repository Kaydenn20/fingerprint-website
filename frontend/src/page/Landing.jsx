import React from 'react';
import { useNavigate } from 'react-router-dom';

const Landing = () => {
  const navigate = useNavigate();
  return (
    <div className="landing-container">
      <div className="landing-card">
        <div className="landing-icon">
          <svg width="3.5em" height="3.5em" viewBox="0 0 48 48" fill="none">
            {/* <circle cx="24" cy="24" r="24" fill="#b6e0fe"/> */}
            <path d="M24 12v24M12 24h24" stroke="#005f73" strokeWidth="0.18em" strokeLinecap="round"/>
          </svg>
        </div>
        <h1 className="landing-title">
          Welcome to Medical Fingerprint System
        </h1>
        <p className="landing-description">
          Fast, secure, and modern patient identification for healthcare professionals.
        </p>
        <button
          className="landing-button"
          onClick={() => navigate('/home')}
          aria-label="Get started with the application"
        >
          Get Started
        </button>
      </div>
    </div>
  );
};

export default Landing; 