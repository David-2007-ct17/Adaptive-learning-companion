// Adaptive Learning Companion - Web Application JavaScript

class LearningCompanionApp {
    constructor() {
        this.currentSession = null;
        this.initEventListeners();
    }

    initEventListeners() {
        // Start learning button
        const startBtn = document.getElementById('startLearningBtn');
        if (startBtn) {
            startBtn.addEventListener('click', () => this.startLearningSession());
        }

        // Quick demo buttons
        const demoBtns = document.querySelectorAll('#quickDemoBtn, #dashboardDemo');
        demoBtns.forEach(btn => {
            if (btn) {
                btn.addEventListener('click', () => this.runQuickDemo());
            }
        });

        // Refresh dashboard
        const refreshBtn = document.getElementById('refreshDashboard');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.refreshDashboard());
        }

        // Enter key support for topic input
        const topicInput = document.getElementById('topicInput');
        if (topicInput) {
            topicInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.startLearningSession();
                }
            });
        }

        // Modal functionality
        this.initModal();
    }

    initModal() {
        const modal = document.getElementById('sessionModal');
        const closeBtn = document.getElementById('modalClose');
        const viewButtons = document.querySelectorAll('.view-session-btn');

        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                modal.style.display = 'none';
            });
        }

        // Close modal when clicking outside
        window.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        });

        // View session buttons
        viewButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const sessionData = JSON.parse(btn.getAttribute('data-session'));
                this.showSessionModal(sessionData);
            });
        });
    }

    showSessionModal(sessionData) {
        const modal = document.getElementById('sessionModal');
        const modalTopic = document.getElementById('modalTopic');
        const modalBody = document.getElementById('modalBody');

        modalTopic.textContent = sessionData.user_input;
        
        let modalContent = `
            <div class="session-info">
                <div class="info-item">
                    <strong>Date:</strong> ${sessionData.timestamp.slice(0, 10)}
                </div>
        `;

        if (sessionData.responses.score) {
            modalContent += `
                <div class="info-item">
                    <strong>Quiz Score:</strong> 
                    <span class="score-value ${sessionData.responses.score >= 80 ? 'score-high' : sessionData.responses.score >= 60 ? 'score-medium' : 'score-low'}">
                        ${sessionData.responses.score}%
                    </span>
                </div>
            `;
        }

        if (sessionData.responses.study_plan) {
            modalContent += `
                <div class="content-box">
                    <h3>📝 Study Plan</h3>
                    <div class="content-text">${this.escapeHtml(sessionData.responses.study_plan)}</div>
                </div>
            `;
        }

        if (sessionData.responses.explanation) {
            modalContent += `
                <div class="content-box">
                    <h3>🤖 Explanation</h3>
                    <div class="content-text">${this.escapeHtml(sessionData.responses.explanation)}</div>
                </div>
            `;
        }

        modalBody.innerHTML = modalContent;
        modal.style.display = 'flex';
    }

    async startLearningSession() {
        const topicInput = document.getElementById('topicInput');
        const topic = topicInput ? topicInput.value.trim() : '';
        
        if (!topic) {
            this.showAlert('Please enter a topic to learn about.', 'error');
            return;
        }

        // Get user profile
        const profile = {
            name: document.getElementById('userName') ? document.getElementById('userName').value : '',
            level: document.getElementById('knowledgeLevel') ? document.getElementById('knowledgeLevel').value : 'beginner',
            timeline: document.getElementById('timeline') ? document.getElementById('timeline').value : '1 week',
            style: document.getElementById('learningStyle') ? document.getElementById('learningStyle').value : 'mixed'
        };

        this.showLoading(true);
        this.updateProgress(0, 'Starting learning session...');

        try {
            const response = await fetch('/api/learning-session', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    topic: topic,
                    profile: profile
                })
            });

            const data = await response.json();

            if (data.success) {
                this.updateProgress(100, 'Complete!');
                setTimeout(() => {
                    this.displaySessionResults(data.session_data, data.topic);
                }, 500);
            } else {
                this.showAlert('Error: ' + data.error, 'error');
            }
        } catch (error) {
            this.showAlert('Network error: ' + error.message, 'error');
        } finally {
            this.showLoading(false);
        }
    }

    updateProgress(percent, text) {
        const progressBar = document.getElementById('progressBar');
        const progressText = document.getElementById('progressText');
        const progressSection = document.getElementById('progressSection');
        
        if (progressSection) {
            progressSection.style.display = 'block';
        }
        
        if (progressBar) {
            progressBar.style.width = percent + '%';
        }
        
        if (progressText) {
            progressText.textContent = text;
        }
    }

    async displaySessionResults(sessionData, topic) {
        const resultsSection = document.getElementById('resultsSection');
        if (!resultsSection) return;

        resultsSection.style.display = 'block';
        resultsSection.innerHTML = '';

        let resultsHTML = `
            <div class="session-header card">
                <h2 class="card-title">
                    <span class="card-icon">🎉</span>
                    Learning Session Complete: ${topic}
                </h2>
            </div>
        `;

        // Study Plan
        if (sessionData.study_plan) {
            resultsHTML += this.createContentBox('📝 Study Plan', sessionData.study_plan);
        }

        // Learning Tools
        if (sessionData.subtopics || sessionData.analogy || sessionData.time_estimate) {
            let toolsContent = '';
            
            if (sessionData.subtopics && sessionData.subtopics.length > 0) {
                toolsContent += '<h4>Topic Breakdown:</h4><ul>';
                sessionData.subtopics.forEach(subtopic => {
                    toolsContent += `<li>${this.escapeHtml(subtopic)}</li>`;
                });
                toolsContent += '</ul>';
            }

            if (sessionData.analogy) {
                toolsContent += `<h4>Helpful Analogy:</h4><p>${this.escapeHtml(sessionData.analogy)}</p>`;
            }

            if (sessionData.time_estimate) {
                toolsContent += `<h4>Time Estimate:</h4><p>${this.escapeHtml(sessionData.time_estimate)}</p>`;
            }

            if (toolsContent) {
                resultsHTML += this.createContentBox('🛠️ Learning Tools', toolsContent);
            }
        }

        // Explanation
        if (sessionData.explanation) {
            resultsHTML += this.createContentBox('🤖 Detailed Explanation', sessionData.explanation);
        }

        // Quiz
        if (sessionData.quiz) {
            resultsHTML += this.createContentBox('🎯 Knowledge Check', sessionData.quiz);
        }

        // Results
        if (sessionData.score !== undefined) {
            const scoreClass = sessionData.score >= 80 ? 'score-high' : 
                             sessionData.score >= 60 ? 'score-medium' : 'score-low';
            const scoreMessage = sessionData.score >= 80 ? '🎉 Excellent! You\'ve mastered this topic!' :
                               sessionData.score >= 60 ? '👍 Good progress! Keep practicing!' :
                               '💪 Keep learning! Review the material and try again.';

            resultsHTML += `
                <div class="content-box">
                    <h3>📊 Session Results</h3>
                    <div class="score-display ${scoreClass}">
                        <div class="score-number">${sessionData.score}%</div>
                        <div class="score-message">${scoreMessage}</div>
                    </div>
                </div>
            `;
        }

        resultsSection.innerHTML = resultsHTML;
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    createContentBox(title, content) {
        return `
            <div class="content-box">
                <h3>${title}</h3>
                <div class="content-text">${this.formatContent(content)}</div>
            </div>
        `;
    }

    formatContent(content) {
        // Convert line breaks to HTML and escape any HTML tags
        return this.escapeHtml(content).replace(/\n/g, '<br>');
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    async runQuickDemo() {
        this.showAlert('Starting quick demo...', 'info');
        
        const demoResults = document.getElementById('demoResults');
        if (demoResults) {
            demoResults.innerHTML = '<div class="loading-text">🔄 Preparing demo session...</div>';
        }

        try {
            const response = await fetch('/api/quick-demo');
            const data = await response.json();

            if (data.success) {
                if (demoResults) {
                    demoResults.innerHTML = this.createDemoResults(data.topic, data.session_data);
                    demoResults.scrollIntoView({ behavior: 'smooth' });
                } else {
                    this.displaySessionResults(data.session_data, data.topic + ' (Demo)');
                }
                this.showAlert('Demo completed successfully!', 'success');
            } else {
                this.showAlert('Demo error: ' + data.error, 'error');
            }
        } catch (error) {
            this.showAlert('Network error: ' + error.message, 'error');
        }
    }

    createDemoResults(topic, sessionData) {
        return `
            <div class="card">
                <h2 class="card-title">
                    <span class="card-icon">⚡</span>
                    Quick Demo: ${topic}
                </h2>
                <div class="demo-content">
                    ${sessionData.study_plan ? this.createContentBox('📝 Study Plan', sessionData.study_plan) : ''}
                    ${sessionData.explanation ? this.createContentBox('🤖 Explanation', sessionData.explanation) : ''}
                    <div class="demo-actions">
                        <a href="/learn" class="btn btn-primary">
                            <span class="btn-icon">🚀</span>
                            Start Your Own Session
                        </a>
                    </div>
                </div>
            </div>
        `;
    }

    showLoading(show, text = 'AI agents are working on your learning session...') {
        const loadingSpinner = document.getElementById('loadingSpinner');
        const loadingText = document.getElementById('loadingText');
        
        if (loadingSpinner) {
            loadingSpinner.style.display = show ? 'block' : 'none';
        }
        
        if (loadingText) {
            loadingText.textContent = text;
        }
    }

    showAlert(message, type = 'info') {
        // Create alert element
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.innerHTML = `
            <div class="alert-content">
                <span class="alert-icon">${this.getAlertIcon(type)}</span>
                <span class="alert-message">${message}</span>
                <button class="alert-close" onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
        `;

        // Add styles for alert
        alertDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${this.getAlertColor(type)};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 1000;
            max-width: 400px;
            animation: slideIn 0.3s ease;
        `;

        // Add to page
        document.body.appendChild(alertDiv);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentElement) {
                alertDiv.remove();
            }
        }, 5000);
    }

    getAlertIcon(type) {
        const icons = {
            'info': 'ℹ️',
            'success': '✅',
            'error': '❌',
            'warning': '⚠️'
        };
        return icons[type] || 'ℹ️';
    }

    getAlertColor(type) {
        const colors = {
            'info': '#3498db',
            'success': '#27ae60',
            'error': '#e74c3c',
            'warning': '#f39c12'
        };
        return colors[type] || '#3498db';
    }

    async refreshDashboard() {
        try {
            const response = await fetch('/api/dashboard-data');
            const insights = await response.json();
            
            // For now, just reload the page
            // In a more advanced version, we could update the DOM dynamically
            location.reload();
        } catch (error) {
            this.showAlert('Error refreshing dashboard: ' + error.message, 'error');
        }
    }
}

// Add CSS for alerts
const alertStyles = `
@keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

.alert-content {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.alert-close {
    background: none;
    border: none;
    color: white;
    font-size: 1.2rem;
    cursor: pointer;
    margin-left: auto;
}

.score-display {
    text-align: center;
    padding: 2rem;
    border-radius: 8px;
    margin: 1rem 0;
}

.score-display.score-high { background: #d4edda; color: #155724; }
.score-display.score-medium { background: #fff3cd; color: #856404; }
.score-display.score-low { background: #f8d7da; color: #721c24; }

.score-number {
    font-size: 3rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}

.score-message {
    font-size: 1.2rem;
    font-weight: 500;
}
`;

// Inject alert styles
const styleSheet = document.createElement('style');
styleSheet.textContent = alertStyles;
document.head.appendChild(styleSheet);

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.learningApp = new LearningCompanionApp();
});