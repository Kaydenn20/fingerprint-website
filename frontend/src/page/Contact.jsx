import React, { useState } from 'react';
import '../css/Contact.css';

function Contact() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: ''
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Here you would typically send the form data to your backend
    console.log('Form submitted:', formData);
    alert('Thank you for your message! We will get back to you soon.');
    setFormData({ name: '', email: '', subject: '', message: '' });
  };

  return (
    <div className="app">
      <div className="contact-container">
        <div className="contact-hero">
          <h1 className="contact-hero-title">Contact Us</h1>
          <p className="contact-hero-subtitle">
            Get in touch with our team for questions, feedback, or collaboration opportunities
          </p>
        </div>

        <div className="contact-content">
          <div className="contact-info-section">
            <h2 className="contact-section-title">Project Information</h2>
            
            <div className="student-info">
              <h3>👨‍🎓 Student Developer</h3>
              <div className="info-card">
                <div className="info-item">
                  <strong>Name:</strong> Your Name Here
                </div>
                <div className="info-item">
                  <strong>Student ID:</strong> 
                </div>
                <div className="info-item">
                  <strong>Email:</strong> 
                  <a href="mailto:your.email@university.edu">your.email@university.edu</a>
                </div>
                <div className="info-item">
                  <strong>Program:</strong> Bachelor of Computer Science
                </div>
                <div className="info-item">
                  <strong>Year:</strong> Final Year Project
                </div>
              </div>
            </div>

            <div className="supervisor-info">
              <h3>👨‍🏫 Academic Supervisor</h3>
              <div className="info-card">
                <div className="info-item">
                  <strong>Name:</strong> Supervisor Name Here
                </div>
                <div className="info-item">
                  <strong>Title:</strong> Professor/Dr./Mr./Ms.
                </div>
                <div className="info-item">
                  <strong>Department:</strong> Department Name
                </div>
                <div className="info-item">
                  <strong>Email:</strong> 
                  <a href="mailto:supervisor@university.edu">supervisor@university.edu</a>
                </div>
                <div className="info-item">
                  <strong>Office:</strong> Office Location
                </div>
              </div>
            </div>

            <div className="project-details">
              <h3>📋 Project Details</h3>
              <div className="info-card">
                <div className="info-item">
                  <strong>Project Title:</strong> Advanced Medical Fingerprint Recognition System
                </div>
                <div className="info-item">
                  <strong>Project Type:</strong> Final Year Project (FYP)
                </div>
                <div className="info-item">
                  <strong>Duration:</strong> Start Date - End Date
                </div>
                <div className="info-item">
                  <strong>Technology:</strong> AI/ML, Web Development, Healthcare Technology
                </div>
                <div className="info-item">
                  <strong>Status:</strong> In Development
                </div>
              </div>
            </div>
          </div>

          <div className="contact-form-section">
            <h2 className="contact-section-title">Send us a Message</h2>
            <form onSubmit={handleSubmit} className="contact-form">
              <div className="form-group">
                <label htmlFor="name">Name *</label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  required
                  placeholder="Your full name"
                />
              </div>

              <div className="form-group">
                <label htmlFor="email">Email *</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  required
                  placeholder="your.email@example.com"
                />
              </div>

              <div className="form-group">
                <label htmlFor="subject">Subject *</label>
                <input
                  type="text"
                  id="subject"
                  name="subject"
                  value={formData.subject}
                  onChange={handleInputChange}
                  required
                  placeholder="What is this about?"
                />
              </div>

              <div className="form-group">
                <label htmlFor="message">Message *</label>
                <textarea
                  id="message"
                  name="message"
                  value={formData.message}
                  onChange={handleInputChange}
                  required
                  rows="6"
                  placeholder="Please describe your inquiry or feedback..."
                ></textarea>
              </div>

              <button type="submit" className="submit-button">
                <span className="button-icon">📧</span>
                Send Message
              </button>
            </form>
          </div>
        </div>

        <div className="additional-contact">
          <h2 className="contact-section-title">Other Ways to Connect</h2>
          <div className="contact-methods">
            <div className="contact-method">
              <span className="method-icon">📧</span>
              <h3>Email</h3>
              <p>For technical questions and project inquiries</p>
              <a href="mailto:your.email@university.edu">your.email@university.edu</a>
            </div>
            
            <div className="contact-method">
              <span className="method-icon">🏢</span>
              <h3>Office Hours</h3>
              <p>Meet with the supervisor during scheduled hours</p>
              <p><strong>Days:</strong> Monday - Friday</p>
              <p><strong>Time:</strong> 9:00 AM - 5:00 PM</p>
            </div>
            
            <div className="contact-method">
              <span className="method-icon">📱</span>
              <h3>Emergency Contact</h3>
              <p>For urgent matters related to the project</p>
              <p><strong>Phone:</strong> +[Country Code] [Phone Number]</p>
            </div>
          </div>
        </div>

        <div className="faq-section">
          <h2 className="contact-section-title">Frequently Asked Questions</h2>
          <div className="faq-list">
            <div className="faq-item">
              <h3>How accurate is the blood group classification?</h3>
              <p>Our system achieves over 99% accuracy in blood group classification using advanced AI algorithms and extensive training data.</p>
            </div>
            
            <div className="faq-item">
              <h3>Is the system HIPAA compliant?</h3>
              <p>Yes, our system is designed with HIPAA compliance in mind, ensuring patient data privacy and security throughout the process.</p>
            </div>
            
            <div className="faq-item">
              <h3>Can I integrate this system with existing healthcare software?</h3>
              <p>Absolutely! Our system is designed with modular architecture and provides APIs for seamless integration with existing healthcare systems.</p>
            </div>
            
            <div className="faq-item">
              <h3>What are the system requirements?</h3>
              <p>The system works on any modern web browser and can be accessed from desktop computers, tablets, and mobile devices.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Contact; 