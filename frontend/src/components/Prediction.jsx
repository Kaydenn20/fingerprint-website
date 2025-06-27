import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import '../css/Prediction.css';

function Prediction() {
    const location = useLocation();
    const navigate = useNavigate();
    const [activeTab, setActiveTab] = useState('overlay'); // 'overlay' or 'heatmap'
    
    // Access imageUrl and prediction from location.state
    // Use optional chaining (?.) and nullish coalescing (??) for safer access
    const { imageUrl, prediction } = location.state || {};

    // Check if prediction data is NOT available
    // This happens if the image wasn't uploaded/processed on the previous page
    if (!prediction) {
        return (
            <div className="prediction-container">
                <div className="exit-button-container">
                    <button onClick={() => navigate('/home')} className="exit-button">⏪ Exit</button>
                </div>
                <div className="prediction-header">
                    {/* Updated Error Message Header */}
                    <h2>Error: Prediction Not Available</h2>
                </div>
                <div className="prediction-content" style={{ textAlign: 'center' }}>
                    {/* Updated Error Message Body */}
                    <p>We couldn't retrieve prediction results. This might be because:</p>
                    <ul>
                        <li>No image was uploaded.</li>
                        <li>There was an issue processing the image.</li>
                        <li>The prediction service encountered an error.</li>
                    </ul>
                     {/* You could add a check for imageUrl here if you specifically want to mention it */}
                     {/* For example: {!imageUrl && <p>Please ensure you upload a fingerprint image.</p>} */}
                     {/* But checking for !prediction is usually sufficient as no prediction means no successful image processing */}

                    <div className="action-buttons">
                        <button onClick={() => navigate('/home')} className="back-button">
                            Go Back and Try Again
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    // If prediction IS available, display the results as before
    const { blood_group, confidence, overlay, heatmap, xai_available } = prediction;

    return (
        <div className="prediction-container">
            <div className="exit-button-container">
                <button onClick={() => navigate('/home')} className="exit-button">⏪ Exit</button>
            </div>
            <div className="prediction-header">
                <h2>🧬 Blood Group Prediction with AI Explanation</h2>
                <p className="header-subtitle">Advanced AI-powered analysis with explainable results</p>
            </div>

            <div className="prediction-content">
                <div className="result-section">
                    <h3>🎯 Analysis Results</h3>
                    <div className="result-card improved-result-card" style={{display: 'flex', flexDirection: 'row', justifyContent: 'space-between', alignItems: 'stretch', gap: '1.5em'}}>
                        <div className="result-item improved-result-item" style={{flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', borderRight: '1.5px solid #b6e0fe', padding: '0.5em 0.7em'}}>
                            <span className="result-label">Predicted Blood Group:</span>
                            <span className="result-value blood-group">
                                <span className="result-icon" role="img" aria-label="Blood">🩸</span> {blood_group}
                            </span>
                        </div>
                        <div className="result-item improved-result-item" style={{flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', borderRight: '1.5px solid #b6e0fe', padding: '0.5em 0.7em'}}>
                            <span className="result-label">Confidence Level:</span>
                            <span className="result-value confidence">
                                <span className="result-icon" role="img" aria-label="Confidence">📈</span> {(confidence * 100).toFixed(2)}%
                            </span>
                        </div>
                        <div className="result-item improved-result-item" style={{flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', borderRight: 'none', padding: '0.5em 0.7em'}}>
                            <span className="result-label">AI Explanation:</span>
                            <span className="result-value xai-status">
                                {xai_available ? <span className="result-icon" role="img" aria-label="Available">✅</span> : <span className="result-icon" role="img" aria-label="Not Available">❌</span>}
                                {xai_available ? ' Available' : ' Not Available'}
                            </span>
                        </div>
                    </div>
                </div>

                <div className="visualization-section">
                    <h3>🔍 Explainable AI Visualization</h3>
                    <p className="xai-description">
                        This heatmap shows which regions of the fingerprint most influenced the AI's blood group prediction. 
                        Red areas indicate high importance, while blue areas show lower influence.
                    </p>
                    
                    {xai_available ? (
                        <div className="xai-container">
                            <div className="xai-tabs">
                                <button 
                                    className={`xai-tab ${activeTab === 'overlay' ? 'active' : ''}`}
                                    onClick={() => setActiveTab('overlay')}
                                >
                                    🔍 Overlay View
                                </button>
                                <button 
                                    className={`xai-tab ${activeTab === 'heatmap' ? 'active' : ''}`}
                                    onClick={() => setActiveTab('heatmap')}
                                >
                                    🎨 Heatmap Only
                        </button>
                            </div>
                            
                            <div className="xai-image-container">
                                {activeTab === 'overlay' && overlay && (
                                    <div className="xai-image-wrapper">
                                        <img 
                                            src={overlay} 
                                            alt="Grad-CAM overlay" 
                                            className="xai-image" 
                                        />
                                        <div className="xai-caption">
                                            <strong>Overlay View:</strong> AI attention heatmap superimposed on the original fingerprint
                                        </div>
                                    </div>
                                )}
                                
                                {activeTab === 'heatmap' && heatmap && (
                                    <div className="xai-image-wrapper">
                                        <img 
                                            src={heatmap} 
                                            alt="Grad-CAM heatmap" 
                                            className="xai-image" 
                                        />
                                        <div className="xai-caption">
                                            <strong>Heatmap View:</strong> Pure attention heatmap showing AI focus areas
                                        </div>
                                    </div>
                                )}
                            </div>
                            
                            <div className="xai-legend">
                                <h4>🎨 Color Legend</h4>
                                <div className="legend-items">
                                    <div className="legend-item">
                                        <span className="legend-color red"></span>
                                        <span>High Importance (Red)</span>
                                    </div>
                                    <div className="legend-item">
                                        <span className="legend-color yellow"></span>
                                        <span>Medium Importance (Yellow)</span>
                                    </div>
                                    <div className="legend-item">
                                        <span className="legend-color blue"></span>
                                        <span>Low Importance (Blue)</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ) : (
                        <div className="xai-unavailable">
                            <div className="xai-placeholder">
                                <span className="placeholder-icon">🔬</span>
                                <p>AI Explanation not available for this prediction</p>
                                <p className="placeholder-subtext">
                                    This might be due to model architecture or processing limitations
                                </p>
                            </div>
                        </div>
                    )}
                </div>

                <div className="original-image-section">
                    <h3>📷 Original Fingerprint</h3>
                    <div className="image-wrapper">
                        {imageUrl ? (
                            <img src={imageUrl} alt="Uploaded fingerprint" className="prediction-image" />
                        ) : (
                            <p>Image preview not available.</p>
                        )}
                    </div>
                </div>

                <div className="action-buttons">
                    <button onClick={() => navigate('/home')} className="back-button">
                        🔄 Analyze Another Fingerprint
                    </button>
                </div>
            </div>
        </div>
    );
}

export default Prediction;