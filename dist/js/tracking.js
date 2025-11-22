import { ApplicationStatus } from './types/index.js';
import { StorageService } from './services/storageService.js';
import { mockUniversityPrograms } from './services/mockData.js';
import { formatDate } from './utils/helpers.js';
// Check authentication
const currentUser = StorageService.getCurrentUser();
if (!currentUser) {
    alert('Please sign in first');
    window.location.href = 'index.html';
}
// DOM Elements
const totalAppsEl = document.getElementById('totalApps');
const submittedAppsEl = document.getElementById('submittedApps');
const reviewAppsEl = document.getElementById('reviewApps');
const acceptedAppsEl = document.getElementById('acceptedApps');
const applicationsList = document.getElementById('applicationsList');
const logoutBtn = document.getElementById('logoutBtn');
// State
let currentFilter = 'all';
let allApplications = [];
// Load applications
function loadApplications() {
    if (!currentUser)
        return;
    allApplications = StorageService.getApplications(currentUser.id);
    // Update stats
    updateStats();
    // Display applications
    displayApplications();
}
function updateStats() {
    totalAppsEl.textContent = allApplications.length.toString();
    const submitted = allApplications.filter(app => app.status === ApplicationStatus.Submitted).length;
    submittedAppsEl.textContent = submitted.toString();
    const underReview = allApplications.filter(app => app.status === ApplicationStatus.UnderReview).length;
    reviewAppsEl.textContent = underReview.toString();
    const accepted = allApplications.filter(app => app.status === ApplicationStatus.Accepted).length;
    acceptedAppsEl.textContent = accepted.toString();
}
function displayApplications() {
    // Filter applications based on current filter
    let filteredApps = allApplications;
    if (currentFilter !== 'all') {
        filteredApps = allApplications.filter(app => app.status === currentFilter);
    }
    if (filteredApps.length === 0) {
        applicationsList.innerHTML = '<p class="no-applications">No applications yet. Visit the <a href="recommendations.html">recommendations page</a> to start applying!</p>';
        return;
    }
    applicationsList.innerHTML = filteredApps.map(app => {
        const program = mockUniversityPrograms.find(p => p.id === app.programId);
        if (!program)
            return '';
        return `
            <div class="application-card">
                <div class="application-header">
                    <div class="application-title">
                        <h3>${program.programName} (${program.degree})</h3>
                        <p class="application-university">${program.universityName}, ${program.country}</p>
                    </div>
                    <span class="status-badge status-${app.status}">
                        ${formatStatus(app.status)}
                    </span>
                </div>
                
                <div class="application-details">
                    <p><strong>Application ID:</strong> ${app.id}</p>
                    <p><strong>Last Updated:</strong> ${formatDate(app.lastUpdated)}</p>
                    ${app.submittedAt ? `<p><strong>Submitted:</strong> ${formatDate(app.submittedAt)}</p>` : ''}
                    <p><strong>Documents:</strong> ${app.documents.length} attached</p>
                    ${app.notes ? `<p><strong>Notes:</strong> ${app.notes}</p>` : ''}
                </div>
                
                <div class="application-actions">
                    ${app.status === ApplicationStatus.Draft
            ? `<button class="btn btn-primary submit-btn" data-app-id="${app.id}">Submit Application</button>`
            : ''}
                    ${app.status === ApplicationStatus.Draft
            ? `<button class="btn btn-secondary edit-btn" data-app-id="${app.id}">Add Notes</button>`
            : ''}
                    ${app.status === ApplicationStatus.Submitted || app.status === ApplicationStatus.UnderReview
            ? `<button class="btn btn-secondary status-btn" data-app-id="${app.id}">Update Status (Demo)</button>`
            : ''}
                    <button class="btn btn-secondary view-program-btn" data-program-id="${program.id}">View Program</button>
                    ${app.status === ApplicationStatus.Draft
            ? `<button class="btn btn-danger delete-btn" data-app-id="${app.id}">Delete</button>`
            : ''}
                </div>
            </div>
        `;
    }).join('');
    // Add event listeners
    document.querySelectorAll('.submit-btn').forEach(btn => {
        btn.addEventListener('click', handleSubmitApplication);
    });
    document.querySelectorAll('.edit-btn').forEach(btn => {
        btn.addEventListener('click', handleEditNotes);
    });
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', handleDeleteApplication);
    });
    document.querySelectorAll('.status-btn').forEach(btn => {
        btn.addEventListener('click', handleUpdateStatus);
    });
    document.querySelectorAll('.view-program-btn').forEach(btn => {
        btn.addEventListener('click', handleViewProgram);
    });
}
function formatStatus(status) {
    return status.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}
function handleSubmitApplication(e) {
    if (!currentUser)
        return;
    const target = e.target;
    const appId = target.dataset.appId;
    if (!appId)
        return;
    if (confirm('Are you sure you want to submit this application? You cannot edit it after submission.')) {
        const app = allApplications.find(a => a.id === appId);
        if (app) {
            app.status = ApplicationStatus.Submitted;
            app.submittedAt = new Date();
            app.lastUpdated = new Date();
            StorageService.saveApplication(app);
            alert('Application submitted successfully!');
            loadApplications();
        }
    }
}
function handleEditNotes(e) {
    if (!currentUser)
        return;
    const target = e.target;
    const appId = target.dataset.appId;
    if (!appId)
        return;
    const app = allApplications.find(a => a.id === appId);
    if (!app)
        return;
    const notes = prompt('Add notes to your application:', app.notes || '');
    if (notes !== null) {
        app.notes = notes;
        app.lastUpdated = new Date();
        StorageService.saveApplication(app);
        loadApplications();
    }
}
function handleDeleteApplication(e) {
    const target = e.target;
    const appId = target.dataset.appId;
    if (!appId)
        return;
    if (confirm('Are you sure you want to delete this application?')) {
        StorageService.deleteApplication(appId);
        alert('Application deleted successfully!');
        loadApplications();
    }
}
function handleUpdateStatus(e) {
    if (!currentUser)
        return;
    const target = e.target;
    const appId = target.dataset.appId;
    if (!appId)
        return;
    const app = allApplications.find(a => a.id === appId);
    if (!app)
        return;
    // Simulate status progression
    const statusProgression = {
        [ApplicationStatus.Submitted]: ApplicationStatus.UnderReview,
        [ApplicationStatus.UnderReview]: ApplicationStatus.Accepted
    };
    const newStatus = statusProgression[app.status];
    if (newStatus) {
        app.status = newStatus;
        app.lastUpdated = new Date();
        StorageService.saveApplication(app);
        alert(`Application status updated to: ${formatStatus(newStatus)}`);
        loadApplications();
    }
}
function handleViewProgram(e) {
    const target = e.target;
    const programId = target.dataset.programId;
    if (!programId)
        return;
    // Navigate to recommendations page
    window.location.href = 'recommendations.html';
}
function handleFilterChange(e) {
    const target = e.target;
    const status = target.dataset.status;
    if (!status)
        return;
    // Update active tab
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    target.classList.add('active');
    // Update filter
    currentFilter = status;
    displayApplications();
}
function handleLogout() {
    if (confirm('Are you sure you want to log out?')) {
        StorageService.clearCurrentUser();
        window.location.href = 'index.html';
    }
}
// Event listeners
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', handleFilterChange);
});
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
loadApplications();
//# sourceMappingURL=tracking.js.map