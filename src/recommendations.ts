import { Application, ApplicationStatus } from './types/index.js';
import { StorageService } from './services/storageService.js';
import { RecommendationService } from './services/recommendationService.js';
import { generateId, formatDate } from './utils/helpers.js';

// Check authentication
const currentUser = StorageService.getCurrentUser();
if (!currentUser) {
    alert('Please sign in first');
    window.location.href = 'index.html';
}

// DOM Elements
const gpaInput = document.getElementById('gpaInput') as HTMLInputElement;
const countryFilter = document.getElementById('countryFilter') as HTMLSelectElement;
const applyFiltersBtn = document.getElementById('applyFilters') as HTMLButtonElement;
const resetFiltersBtn = document.getElementById('resetFilters') as HTMLButtonElement;
const recommendationsList = document.getElementById('recommendationsList') as HTMLElement;
const logoutBtn = document.getElementById('logoutBtn') as HTMLElement;

// Load recommendations
function loadRecommendations() {
    if (!currentUser) return;
    
    const gpa = parseFloat(gpaInput.value) || 3.5;
    const selectedCountries = Array.from(countryFilter.selectedOptions).map(opt => opt.value);
    
    const documents = StorageService.getDocuments(currentUser.id);
    const recommendations = RecommendationService.getRecommendations(
        documents,
        gpa,
        selectedCountries
    );
    
    if (recommendations.length === 0) {
        recommendationsList.innerHTML = '<p class="loading">No recommendations available</p>';
        return;
    }
    
    recommendationsList.innerHTML = recommendations.map(rec => {
        const program = rec.program;
        const isApplied = checkIfApplied(program.id);
        
        return `
            <div class="recommendation-card">
                <div class="recommendation-header">
                    <div class="program-info">
                        <h3>${program.programName} (${program.degree})</h3>
                        <p class="program-university">${program.universityName}, ${program.country}</p>
                    </div>
                    <div class="match-score">
                        <div class="score-circle">${rec.matchScore}%</div>
                        <div class="score-label">Match Score</div>
                    </div>
                </div>
                
                <div class="program-details">
                    <div class="detail-item">
                        <span class="detail-label">Tuition Fee</span>
                        <span class="detail-value">
                            ${program.tuitionFee === 0 ? 'Free' : `${program.tuitionFee.toLocaleString()} ${program.currency}`}
                        </span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Duration</span>
                        <span class="detail-value">${program.duration}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Min GPA</span>
                        <span class="detail-value">${program.requirements.minGPA.toFixed(1)}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Language Test</span>
                        <span class="detail-value">${program.requirements.languageTest || 'Not specified'}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Application Deadline</span>
                        <span class="detail-value">${formatDate(program.deadline)}</span>
                    </div>
                </div>
                
                <p class="program-description">${program.description}</p>
                
                <div class="match-reasons">
                    <h4>Why This Program Matches You:</h4>
                    <ul>
                        ${rec.reasons.map(reason => `<li>${reason}</li>`).join('')}
                    </ul>
                </div>
                
                <div class="recommendation-actions">
                    ${isApplied 
                        ? '<button class="btn btn-secondary" disabled>Already Applied</button>'
                        : `<button class="btn btn-primary apply-btn" data-program-id="${program.id}">Apply Now</button>`
                    }
                    <button class="btn btn-secondary view-details-btn" data-program-id="${program.id}">View Details</button>
                </div>
            </div>
        `;
    }).join('');
    
    // Add event listeners
    document.querySelectorAll('.apply-btn').forEach(btn => {
        btn.addEventListener('click', handleApply);
    });
    
    document.querySelectorAll('.view-details-btn').forEach(btn => {
        btn.addEventListener('click', handleViewDetails);
    });
}

function checkIfApplied(programId: string): boolean {
    if (!currentUser) return false;
    const applications = StorageService.getApplications(currentUser.id);
    return applications.some(app => app.programId === programId);
}

function handleApply(e: Event) {
    if (!currentUser) return;
    
    const target = e.target as HTMLElement;
    const programId = target.dataset.programId;
    
    if (!programId) return;
    
    // Check if already applied
    if (checkIfApplied(programId)) {
        alert('You have already applied to this program');
        return;
    }
    
    // Get user documents
    const documents = StorageService.getDocuments(currentUser.id);
    
    if (documents.length === 0) {
        if (confirm('You need to upload documents first. Go to upload page?')) {
            window.location.href = 'upload.html';
        }
        return;
    }
    
    // Create application
    const application: Application = {
        id: generateId(),
        userId: currentUser.id,
        programId: programId,
        status: ApplicationStatus.Draft,
        lastUpdated: new Date(),
        documents: documents.map(doc => doc.id)
    };
    
    StorageService.saveApplication(application);
    
    alert('Application created successfully! You can track it on the tracking page.');
    
    // Reload to update button states
    loadRecommendations();
}

function handleViewDetails(e: Event) {
    const target = e.target as HTMLElement;
    const programId = target.dataset.programId;
    
    if (!programId) return;
    
    // In a real app, this would navigate to a detailed page
    alert('Program details page would open here. For this demo, all details are shown in the card.');
}

function handleApplyFilters() {
    loadRecommendations();
}

function handleResetFilters() {
    gpaInput.value = '3.5';
    countryFilter.selectedIndex = -1;
    loadRecommendations();
}

function handleLogout() {
    if (confirm('Are you sure you want to log out?')) {
        StorageService.clearCurrentUser();
        window.location.href = 'index.html';
    }
}

// Event listeners
applyFiltersBtn.addEventListener('click', handleApplyFilters);
resetFiltersBtn.addEventListener('click', handleResetFilters);
logoutBtn.addEventListener('click', (e) => {
    e.preventDefault();
    handleLogout();
});

// Mobile navigation toggle
const navToggle = document.getElementById('navToggle');
if (navToggle) {
    navToggle.addEventListener('click', () => {
        const navMenu = document.querySelector('.nav-menu');
        navMenu?.classList.toggle('active');
    });
}

// Initialize
loadRecommendations();
