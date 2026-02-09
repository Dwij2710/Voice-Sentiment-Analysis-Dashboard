let selectedFile = null;
let emotionPieChart = null;
let emotionTimelineChart = null;

const emotionColors = {
    'Very Happy': '#2e7d32',
    'Happy': '#4caf50',
    'Positive': '#8bc34a',
    'Negative': '#ff9800',
    'Sad': '#f44336',
    'Very Sad': '#c62828'
};

// File selection handler
document.getElementById('audioFile').addEventListener('change', function(e) {
    selectedFile = e.target.files[0];
    if (selectedFile) {
        document.querySelector('.upload-label span').textContent = selectedFile.name;
        document.getElementById('analyzeBtn').disabled = false;
    }
});

// Analyze button handler
document.getElementById('analyzeBtn').addEventListener('click', async function() {
    if (!selectedFile) return;
    
    // Hide previous results and errors
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'none';
    document.getElementById('loadingSection').style.display = 'block';
    
    const formData = new FormData();
    formData.append('audio', selectedFile);
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        document.getElementById('loadingSection').style.display = 'none';
        
        if (data.success) {
            displayResults(data);
        } else {
            showError(data.error || 'Analysis failed. Please try again.');
        }
    } catch (error) {
        document.getElementById('loadingSection').style.display = 'none';
        showError('Network error. Please check your connection and try again.');
        console.error('Error:', error);
    }
});

function displayResults(data) {
    document.getElementById('resultsSection').style.display = 'block';
    
    // Display stats
    document.getElementById('duration').textContent = formatDuration(data.duration);
    document.getElementById('segments').textContent = data.total_segments;
    
    // Find dominant emotion
    const summary = data.emotion_summary;
    let dominantEmotion = 'N/A';
    let maxCount = 0;
    
    for (const [emotion, stats] of Object.entries(summary)) {
        if (stats.count > maxCount) {
            maxCount = stats.count;
            dominantEmotion = emotion;
        }
    }
    
    document.getElementById('dominantEmotion').textContent = dominantEmotion;
    
    // Create charts
    createEmotionPieChart(data.emotion_summary);
    createEmotionTimelineChart(data.results);
    
    // Display timeline
    displayTimeline(data.results);
    
    // Display emotion summary
    displayEmotionSummary(data.emotion_summary);
}

function createEmotionPieChart(emotionSummary) {
    const ctx = document.getElementById('emotionPieChart').getContext('2d');
    
    // Destroy previous chart if exists
    if (emotionPieChart) {
        emotionPieChart.destroy();
    }
    
    const labels = Object.keys(emotionSummary);
    const data = labels.map(emotion => emotionSummary[emotion].count);
    const colors = labels.map(emotion => emotionColors[emotion] || '#999');
    
    emotionPieChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors,
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const percentage = emotionSummary[label].percentage;
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

function createEmotionTimelineChart(results) {
    const ctx = document.getElementById('emotionTimelineChart').getContext('2d');
    
    // Destroy previous chart if exists
    if (emotionTimelineChart) {
        emotionTimelineChart.destroy();
    }
    
    // Prepare data
    const timestamps = results.map(r => r.timestamp);
    const emotions = results.map(r => r.emotion);
    
    // Create emotion to numeric mapping
    const emotionToNumber = {
        'Very Sad': 1,
        'Sad': 2,
        'Negative': 3,
        'Positive': 4,
        'Happy': 5,
        'Very Happy': 6
    };
    
    const dataPoints = results.map(r => ({
        x: r.start_seconds,
        y: emotionToNumber[r.emotion] || 3,
        emotion: r.emotion,
        text: r.text
    }));
    
    emotionTimelineChart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'Emotion Over Time',
                data: dataPoints,
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                pointBackgroundColor: dataPoints.map(p => emotionColors[p.emotion] || '#999'),
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 6,
                pointHoverRadius: 8,
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                x: {
                    type: 'linear',
                    title: {
                        display: true,
                        text: 'Time (seconds)',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    ticks: {
                        callback: function(value) {
                            return Math.floor(value) + 's';
                        }
                    }
                },
                y: {
                    min: 0,
                    max: 7,
                    title: {
                        display: true,
                        text: 'Emotion',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    ticks: {
                        callback: function(value) {
                            const reverseMapping = {
                                1: 'Very Sad',
                                2: 'Sad',
                                3: 'Negative',
                                4: 'Positive',
                                5: 'Happy',
                                6: 'Very Happy'
                            };
                            return reverseMapping[value] || '';
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        title: function(context) {
                            const point = context[0].raw;
                            return `Time: ${formatSeconds(point.x)}`;
                        },
                        label: function(context) {
                            const point = context.raw;
                            return [
                                `Emotion: ${point.emotion}`,
                                `Text: "${point.text}"`
                            ];
                        }
                    }
                }
            }
        }
    });
}

function displayTimeline(results) {
    const timeline = document.getElementById('timeline');
    timeline.innerHTML = '';
    
    results.forEach(result => {
        const item = document.createElement('div');
        item.className = `timeline-item ${result.emotion.replace(/\s+/g, '.')}`;
        
        item.innerHTML = `
            <div class="timeline-header">
                <span class="timestamp">${result.timestamp}</span>
                <span class="emotion-badge ${result.emotion.replace(/\s+/g, '.')}">${result.emotion}</span>
            </div>
            <div class="timeline-content">
                <p>"${result.text}"</p>
                <p class="confidence">Confidence: ${result.confidence}%</p>
            </div>
        `;
        
        timeline.appendChild(item);
    });
}

function displayEmotionSummary(emotionSummary) {
    const summaryGrid = document.getElementById('emotionSummary');
    summaryGrid.innerHTML = '';
    
    for (const [emotion, stats] of Object.entries(emotionSummary)) {
        const card = document.createElement('div');
        card.className = 'summary-card';
        card.style.borderColor = emotionColors[emotion] || '#999';
        
        card.innerHTML = `
            <h4>${emotion}</h4>
            <div class="summary-stat">
                <span>Occurrences:</span>
                <strong>${stats.count}</strong>
            </div>
            <div class="summary-stat">
                <span>Percentage:</span>
                <strong>${stats.percentage}%</strong>
            </div>
            <div class="summary-stat">
                <span>Avg Confidence:</span>
                <strong>${stats.avg_confidence}%</strong>
            </div>
        `;
        
        summaryGrid.appendChild(card);
    }
}

function formatDuration(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
}

function formatSeconds(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
}

function showError(message) {
    document.getElementById('errorSection').style.display = 'block';
    document.getElementById('errorMessage').textContent = message;
}
