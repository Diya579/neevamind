// NeevaMind Frontend JavaScript

class NeevaMindApp {
    constructor() {
        this.currentPage = 'homepage';
        this.currentUser = null;
        this.apiBaseUrl = 'http://localhost:5000/api';
        this.init();
    }

    init() {
        this.bindEvents();
        this.checkAuthStatus();
    }

    bindEvents() {
        // Navigation events
        document.getElementById('loginBtn').addEventListener('click', () => this.showModal('loginModal'));
        document.getElementById('signupBtn').addEventListener('click', () => this.showModal('signupModal'));
        document.getElementById('getStartedBtn').addEventListener('click', () => this.showModal('signupModal'));
        
        // Modal close events
        document.querySelectorAll('.close').forEach(closeBtn => {
            closeBtn.addEventListener('click', (e) => this.hideModal(e.target.closest('.modal')));
        });
        
        // Form submission events
        document.getElementById('loginForm').addEventListener('submit', (e) => this.handleLogin(e));
        document.getElementById('signupForm').addEventListener('submit', (e) => this.handleSignup(e));
        document.getElementById('diaryForm').addEventListener('submit', (e) => this.handleDiarySubmit(e));
        
        // Navigation events
        document.getElementById('logoutBtn').addEventListener('click', () => this.handleLogout());
        document.getElementById('backToDashboard').addEventListener('click', () => this.showPage('dashboard'));
        document.getElementById('backToDashboardFromInsights').addEventListener('click', () => this.showPage('dashboard'));
        document.getElementById('backToDashboardFromReport').addEventListener('click', () => this.showPage('dashboard'));
        
        // CTA button event
        document.getElementById('ctaStartBtn').addEventListener('click', () => this.showModal('signupModal'));
        
        // Dashboard card events
        document.getElementById('writeDiaryCard').addEventListener('click', () => this.showPage('diaryPage'));
        document.getElementById('viewInsightsCard').addEventListener('click', () => this.showPage('insightsPage'));
        document.getElementById('viewWeeklyReportCard').addEventListener('click', () => this.showPage('weeklyReportPage'));
        
        // Memory clarity slider
        const memorySlider = document.getElementById('memoryClarity');
        const memoryValue = document.getElementById('memoryClarityValue');
        if (memorySlider && memoryValue) {
            memorySlider.addEventListener('input', (e) => {
                memoryValue.textContent = e.target.value;
            });
        }
        
        // FAQ accordion functionality
        document.querySelectorAll('.faq-question').forEach(question => {
            question.addEventListener('click', (e) => {
                const faqItem = e.target.closest('.faq-item');
                const isActive = faqItem.classList.contains('active');
                
                // Close all FAQ items
                document.querySelectorAll('.faq-item').forEach(item => {
                    item.classList.remove('active');
                });
                
                // Open clicked item if it wasn't active
                if (!isActive) {
                    faqItem.classList.add('active');
                }
            });
        });
        
        // Close modal when clicking outside
        window.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                this.hideModal(e.target);
            }
        });
    }

    async checkAuthStatus() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/auth/check`, {
                credentials: 'include'
            });
            
            if (response.ok) {
                const data = await response.json();
                this.currentUser = data.user;
                this.showPage('dashboard');
                this.updateWelcomeMessage();
            }
        } catch (error) {
            console.log('User not authenticated');
        }
    }

    showPage(pageId) {
        // Hide all pages
        document.querySelectorAll('.page').forEach(page => {
            page.classList.remove('active');
        });
        
        // Show selected page
        document.getElementById(pageId).classList.add('active');
        this.currentPage = pageId;
        
        // Load page-specific data
        if (pageId === 'insightsPage') {
            this.loadInsights();
        } else if (pageId === 'weeklyReportPage') {
            this.loadWeeklyReport();
        }
    }

    showModal(modalId) {
        document.getElementById(modalId).style.display = 'block';
    }

    hideModal(modal) {
        modal.style.display = 'none';
    }

    updateWelcomeMessage() {
        const welcomeElement = document.getElementById('welcomeMessage');
        if (welcomeElement && this.currentUser) {
            welcomeElement.textContent = `Welcome back, ${this.currentUser.name}!`;
        }
    }

    async handleLogin(e) {
        e.preventDefault();
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify({ email, password })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.currentUser = data.user;
                this.hideModal(document.getElementById('loginModal'));
                this.showPage('dashboard');
                this.updateWelcomeMessage();
                this.showToast('Login successful!', 'success');
            } else {
                this.showToast(data.message || 'Login failed', 'error');
            }
        } catch (error) {
            this.showToast('Network error. Please try again.', 'error');
        }
    }

    async handleSignup(e) {
        e.preventDefault();
        const name = document.getElementById('signupName').value;
        const email = document.getElementById('signupEmail').value;
        const password = document.getElementById('signupPassword').value;
        const confirmPassword = document.getElementById('signupConfirmPassword').value;
        
        if (password !== confirmPassword) {
            this.showToast('Passwords do not match', 'error');
            return;
        }
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/auth/signup`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify({ name, email, password })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.currentUser = data.user;
                this.hideModal(document.getElementById('signupModal'));
                this.showPage('dashboard');
                this.updateWelcomeMessage();
                this.showToast('Signup successful!', 'success');
            } else {
                this.showToast(data.message || 'Signup failed', 'error');
            }
        } catch (error) {
            this.showToast('Network error. Please try again.', 'error');
        }
    }

    async handleDiarySubmit(e) {
        e.preventDefault();
        const entryText = document.getElementById('diaryText').value;
        const moodTag = document.getElementById('moodTag').value;
        const memoryClarity = parseInt(document.getElementById('memoryClarity').value);
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/diary/entry`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify({ entryText, moodTag, memoryClarity })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.showToast('Diary entry saved successfully!', 'success');
                document.getElementById('diaryForm').reset();
                document.getElementById('memoryClarityValue').textContent = '5';
                
                // Generate AI insights after saving entry
                await this.generateInsights();
            } else {
                this.showToast(data.message || 'Failed to save entry', 'error');
            }
        } catch (error) {
            this.showToast('Network error. Please try again.', 'error');
        }
    }

    async generateInsights() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/insights/generate`, {
                method: 'POST',
                credentials: 'include'
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.showToast('AI insights generated successfully!', 'success');
            } else {
                console.error('Failed to generate insights:', data.message);
            }
        } catch (error) {
            console.error('Error generating insights:', error);
        }
    }

    async loadInsights() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/insights`, {
                credentials: 'include'
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.displayInsights(data.insights);
            } else {
                this.showToast('Failed to load insights', 'error');
            }
        } catch (error) {
            this.showToast('Network error. Please try again.', 'error');
        }
    }

    displayInsights(insights) {
        const container = document.getElementById('insightsContainer');
        container.innerHTML = '';
        
        if (insights.length === 0) {
            container.innerHTML = '<p>No insights available yet. Write some diary entries to get started!</p>';
            return;
        }
        
        insights.forEach(insight => {
            const card = document.createElement('div');
            card.className = 'insight-card';
            card.innerHTML = `
                <h4>${this.getInsightTitle(insight.category)}</h4>
                <p>${insight.insight_text}</p>
                <span class="category">${insight.category}</span>
            `;
            container.appendChild(card);
        });
    }

    getInsightTitle(category) {
        const titles = {
            'mood': 'Mood Analysis',
            'memory': 'Memory Patterns',
            'cognitive': 'Cognitive Health',
            'language': 'Language Usage',
            'behavior': 'Behavioral Insights'
        };
        return titles[category] || 'Insight';
    }

    async loadWeeklyReport() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/insights/weekly-report`, {
                credentials: 'include'
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.displayWeeklyReport(data.report);
            } else {
                this.showToast('Failed to load weekly report', 'error');
            }
        } catch (error) {
            this.showToast('Network error. Please try again.', 'error');
        }
    }

    displayWeeklyReport(reportData) {
        // Calculate overall statistics
        const totalEntries = reportData.reduce((sum, day) => sum + day.entryCount, 0);
        const avgMood = reportData.reduce((sum, day) => sum + day.moodScore, 0) / reportData.length;
        const avgMemory = reportData.reduce((sum, day) => sum + day.memoryScore, 0) / reportData.length;
        
        // Update summary cards
        document.getElementById('overallMood').textContent = avgMood.toFixed(1);
        document.getElementById('overallMemory').textContent = avgMemory.toFixed(1);
        document.getElementById('totalEntries').textContent = totalEntries;
        
        // Display chart
        this.displayWeeklyChart(reportData);
        
        // Display daily breakdown
        this.displayDailyBreakdown(reportData);
    }

    displayWeeklyChart(reportData) {
        const chartContainer = document.getElementById('weeklyChart');
        
        chartContainer.innerHTML = `
            <div class="enhanced-chart">
                <div class="chart-legend">
                    <div class="legend-item">
                        <div class="legend-color mood-color"></div>
                        <span>Mood Score</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color memory-color"></div>
                        <span>Memory Score</span>
                    </div>
                </div>
                <div class="chart-bars">
                    ${reportData.map(day => `
                        <div class="bar-group">
                            <div class="bar-container">
                                <div class="bar mood-bar" style="height: ${day.moodScore * 15}px;" title="Mood: ${day.moodScore}"></div>
                                <div class="bar memory-bar" style="height: ${day.memoryScore * 15}px;" title="Memory: ${day.memoryScore}"></div>
                            </div>
                            <div class="bar-label">${day.day}</div>
                            <div class="bar-entry-count">${day.entryCount} entries</div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    displayDailyBreakdown(reportData) {
        const breakdownContainer = document.getElementById('dailyBreakdown');
        
        breakdownContainer.innerHTML = reportData.map(day => `
            <div class="day-card">
                <h4>${day.day}</h4>
                <p><strong>Mood:</strong> ${day.moodScore.toFixed(1)}/10</p>
                <p><strong>Memory:</strong> ${day.memoryScore.toFixed(1)}/10</p>
                <p><strong>Entries:</strong> ${day.entryCount}</p>
            </div>
        `).join('');
    }

    async handleLogout() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/auth/logout`, {
                method: 'POST',
                credentials: 'include'
            });
            
            if (response.ok) {
                this.currentUser = null;
                this.showPage('homepage');
                this.showToast('Logged out successfully', 'success');
            }
        } catch (error) {
            this.showToast('Error logging out', 'error');
        }
    }

    showToast(message, type = 'info') {
        // Simple toast notification
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            color: white;
            font-weight: 600;
            z-index: 10000;
            animation: slideInRight 0.3s ease;
            background-color: ${type === 'success' ? 'var(--primary-teal)' : 'var(--dark-teal)'};
        `;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new NeevaMindApp();
});

// Add some additional CSS for the toast and simple chart
const additionalStyles = `
    .toast {
        animation: slideInRight 0.3s ease;
    }
    
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .simple-chart {
        text-align: center;
    }
    
    .chart-bars {
        display: flex;
        justify-content: space-around;
        align-items: end;
        height: 200px;
        margin-top: 1rem;
    }
    
    .bar-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 40px;
    }
    
    .bar {
        width: 30px;
        background-color: var(--primary-teal);
        border-radius: 4px 4px 0 0;
        transition: all 0.3s ease;
    }
    
    .bar:hover {
        background-color: var(--dark-teal);
    }
    
    .bar-label {
        margin-top: 0.5rem;
        font-size: 0.8rem;
        color: var(--dark-gray);
    }
`;

const styleSheet = document.createElement('style');
styleSheet.textContent = additionalStyles;
