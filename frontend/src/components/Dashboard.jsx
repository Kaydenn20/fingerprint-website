import React, { useEffect, useState } from 'react';
import { Pie, Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
} from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement);

const COLORS = [
  '#005f73', '#0a9396', '#94d2bd', '#ee9b00', '#ca6702', '#bb3e03', '#ae2012', '#3a86ff'
];

// --- Blood group color map ---
const BLOOD_COLORS = {
  'A+': '#E7D27C',
  'A-': '#FFF8D5',
  'B+': '#DDA0DD',
  'B-': '#E6AAD2',
  'AB+': '#F1BEB5',
  'AB-': '#D3B8A1',
  'O+': '#9DD6AD',
  'O-': '#A5E3E0',
};

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let interval;
    const fetchStats = async () => {
      try {
        setLoading(true);
        setError('');
        const res = await fetch('http://localhost:5000/stats');
        if (!res.ok) throw new Error('Failed to fetch stats');
        const data = await res.json();
        setStats(data);
      } catch (err) {
        setError('Could not load stats.');
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
    interval = setInterval(fetchStats, 3000);
    return () => clearInterval(interval);
  }, []);

  // Prepare chart data
  const bloodGroups = stats ? Object.keys(stats.blood_groups) : [];
  const bloodCounts = stats ? Object.values(stats.blood_groups) : [];
  const confidences = stats ? stats.confidences : [];

  // Confidence histogram bins
  const bins = [0,0,0,0,0,0,0,0,0,0];
  confidences.forEach(c => {
    const idx = Math.min(9, Math.floor(c * 10));
    bins[idx]++;
  });

  // --- Timeline colors by blood group ---
  const groupColors = {
    'A+': '#005f73', 'A-': '#0a9396', 'AB+': '#94d2bd', 'AB-': '#ee9b00',
    'B+': '#ca6702', 'B-': '#bb3e03', 'O+': '#ae2012', 'O-': '#3a86ff'
  };
  const recent = stats ? stats.recent_predictions : [];

  // --- Timeline auto-scroll ref ---
  const timelineRef = React.useRef(null);
  useEffect(() => {
    if (timelineRef.current) {
      timelineRef.current.scrollLeft = timelineRef.current.scrollWidth;
    }
  }, [recent.length]);

  // Calculate average confidence per blood group
  const groupAvgConfidence = bloodGroups.map(bg => {
    const groupPreds = recent.filter(p => p.blood_group === bg);
    if (groupPreds.length === 0) return 0;
    const avg = groupPreds.reduce((sum, p) => sum + (p.confidence || 0), 0) / groupPreds.length;
    return +(avg * 100).toFixed(1); // as percentage
  });

  // Chart options for responsiveness
  const pieOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          padding: 20,
          usePointStyle: true,
          font: {
            size: window.innerWidth < 768 ? 12 : 14
          }
        }
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: '#fff',
        bodyColor: '#fff',
        borderColor: '#005f73',
        borderWidth: 1
      }
    }
  };

  const barOptions = {
    responsive: true,
    maintainAspectRatio: false,
    scales: { 
      y: { 
        beginAtZero: true, 
        max: 100,
        ticks: {
          font: {
            size: window.innerWidth < 768 ? 10 : 12
          }
        }
      },
      x: {
        ticks: {
          font: {
            size: window.innerWidth < 768 ? 10 : 12
          }
        }
      }
    },
    plugins: { 
      legend: { 
        display: false 
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: '#fff',
        bodyColor: '#fff',
        borderColor: '#005f73',
        borderWidth: 1
      }
    }
  };

  return (
    <div className="dashboard-container">
      <h2 className="dashboard-title">📈 Real-Time Prediction Dashboard</h2>
      {loading && <p className="loading-text">Loading stats...</p>}
      {error && <p className="error-text">{error}</p>}
      {stats && (
        <>
          <div className="stats-summary">
            <b>Total Predictions:</b> {stats.total}
          </div>
          
          <div className="charts-container">
            <div className="chart-wrapper">
              <h3>Blood Group Distribution</h3>
              <div className="chart-container">
              <Pie
                data={{
                  labels: bloodGroups,
                  datasets: [{
                    data: bloodCounts,
                    backgroundColor: bloodGroups.map(bg => BLOOD_COLORS[bg] || '#ccc'),
                      borderWidth: 2,
                      borderColor: '#fff'
                  }],
                }}
                  options={pieOptions}
              />
              </div>
            </div>
            
            <div className="chart-wrapper">
              <h3>Confidence Histogram</h3>
              <div className="chart-container">
              <Bar
                data={{
                  labels: bloodGroups,
                  datasets: [{
                    label: 'Avg Confidence (%)',
                    data: groupAvgConfidence,
                    backgroundColor: bloodGroups.map(bg => BLOOD_COLORS[bg] || '#ccc'),
                      borderWidth: 1,
                      borderColor: '#fff'
                  }],
                }}
                  options={barOptions}
              />
              </div>
            </div>
          </div>
          
          <div className="timeline-section">
            <h3>Recent Predictions Timeline</h3>
            <div
              ref={timelineRef}
              className="timeline-container"
            >
              {recent.length === 0 && <span className="no-predictions">No predictions yet.</span>}
              {recent.map((p, i) => (
                <div
                  key={i}
                  title={`Blood Group: ${p.blood_group}\nConfidence: ${(p.confidence*100).toFixed(1)}%`}
                  className="timeline-item"
                  style={{
                    background: BLOOD_COLORS[p.blood_group] || '#ccc',
                    width: `${Math.max(40, 40 + 60 * p.confidence)}px`,
                    height: `${Math.max(30, 30 + 30 * p.confidence)}px`,
                  }}
                >
                  <span className="blood-group-text">{p.blood_group}</span>
                  <span className="confidence-text">
                    {Math.round(p.confidence*100)}%
                  </span>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default Dashboard; 