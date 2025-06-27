import React from 'react';
import { Link } from 'react-router-dom';
import '../css/About.css';

function About() {
  return (
    <div className="app">
      <div className="about-container">
        <div className="about-hero">
          <h1 className="about-hero-title">About Our System</h1>
          <p className="about-hero-subtitle">
            Revolutionizing healthcare with AI-powered fingerprint-based blood group classification
          </p>
        </div>

        <div className="about-content">
          <section className="about-section">
            <h2>System Overview</h2>
            <p>
              Our Advanced Medical Fingerprint Recognition System is a cutting-edge healthcare technology 
              that combines artificial intelligence with medical diagnostics to provide non-invasive blood 
              group classification through fingerprint analysis. This innovative approach eliminates the 
              need for traditional blood sampling while maintaining high accuracy and reliability.
            </p>
          </section>

          <section className="about-section">
            <h2>Objectives</h2>
            <div className="objectives-grid">
              <div className="objective-card">
                <span className="objective-icon">🩸</span>
                <h3>Non-Invasive Testing</h3>
                <p>Eliminate the need for blood draws by using fingerprint analysis for blood group determination</p>
              </div>
              <div className="objective-card">
                <span className="objective-icon">⚡</span>
                <h3>Rapid Results</h3>
                <p>Provide instant blood group classification results within seconds of fingerprint upload</p>
              </div>
              <div className="objective-card">
                <span className="objective-icon">🎯</span>
                <h3>High Accuracy</h3>
                <p>Achieve 99%+ accuracy in blood group classification using advanced AI algorithms</p>
              </div>
              <div className="objective-card">
                <span className="objective-icon">🏥</span>
                <h3>Healthcare Integration</h3>
                <p>Seamlessly integrate with existing healthcare systems for improved patient care</p>
              </div>
              <div className="objective-card">
                <span className="objective-icon">🔒</span>
                <h3>Data Security</h3>
                <p>Ensure HIPAA compliance and maintain patient privacy throughout the process</p>
              </div>
              <div className="objective-card">
                <span className="objective-icon">📱</span>
                <h3>Accessibility</h3>
                <p>Make blood group testing accessible in remote areas and emergency situations</p>
              </div>
            </div>
          </section>

          <section className="about-section">
            <h2>Technology Stack</h2>
            <div className="tech-grid">
              <div className="tech-category">
                <h3>🤖 Artificial Intelligence</h3>
                <ul>
                  <li><strong>Deep Learning:</strong> ResNet50 architecture for image classification</li>
                  <li><strong>Computer Vision:</strong> OpenCV for fingerprint preprocessing and validation</li>
                  <li><strong>Neural Networks:</strong> Custom-trained models for blood group classification</li>
                  <li><strong>Image Processing:</strong> Advanced algorithms for fingerprint pattern recognition</li>
                </ul>
              </div>
              
              <div className="tech-category">
                <h3>🌐 Web Development</h3>
                <ul>
                  <li><strong>Frontend:</strong> React.js with modern UI/UX design</li>
                  <li><strong>Backend:</strong> Flask (Python) REST API</li>
                  <li><strong>Styling:</strong> CSS3 with responsive design principles</li>
                  <li><strong>Routing:</strong> React Router for seamless navigation</li>
                </ul>
              </div>
              
              <div className="tech-category">
                <h3>🔧 Development Tools</h3>
                <ul>
                  <li><strong>Framework:</strong> TensorFlow/Keras for model development</li>
                  <li><strong>Data Processing:</strong> NumPy and PIL for image manipulation</li>
                  <li><strong>API:</strong> Flask-CORS for cross-origin requests</li>
                  <li><strong>Deployment:</strong> Network-accessible Flask server</li>
                </ul>
              </div>
              
              <div className="tech-category">
                <h3>📊 Data & Security</h3>
                <ul>
                  <li><strong>Validation:</strong> Multi-stage fingerprint verification</li>
                  <li><strong>Security:</strong> HIPAA-compliant data handling</li>
                  <li><strong>Performance:</strong> Optimized for real-time processing</li>
                  <li><strong>Scalability:</strong> Modular architecture for easy expansion</li>
                </ul>
              </div>
            </div>
          </section>

          <section className="about-section">
            <h2>How It Works</h2>
            <div className="process-steps">
              <div className="step">
                <div className="step-number">1</div>
                <div className="step-content">
                  <h3>Fingerprint Upload</h3>
                  <p>Users upload a clear fingerprint image through our secure web interface</p>
                </div>
              </div>
              <div className="step">
                <div className="step-number">2</div>
                <div className="step-content">
                  <h3>Image Validation</h3>
                  <p>Advanced algorithms verify the image quality and confirm it's a valid fingerprint</p>
                </div>
              </div>
              <div className="step">
                <div className="step-number">3</div>
                <div className="step-content">
                  <h3>AI Analysis</h3>
                  <p>ResNet50 neural network analyzes fingerprint patterns to determine blood group</p>
                </div>
              </div>
              <div className="step">
                <div className="step-number">4</div>
                <div className="step-content">
                  <h3>Results Delivery</h3>
                  <p>Instant results with confidence scores and detailed analysis are provided</p>
                </div>
              </div>
            </div>
          </section>

          <section className="about-section">
            <h2>Future Enhancements</h2>
            <div className="enhancements">
              <p>
                Our system is designed for continuous improvement and expansion. Future versions will include:
              </p>
              <ul>
                <li>Integration with electronic health records (EHR) systems</li>
                <li>Mobile application for on-the-go testing</li>
                <li>Additional biometric data analysis capabilities</li>
                <li>Real-time collaboration features for healthcare teams</li>
                <li>Multi-language support for global accessibility</li>
              </ul>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}

export default About; 