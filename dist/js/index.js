import { StorageService } from './services/storageService.js';
import { mockUniversityPrograms } from './services/mockData.js';
import { generateId, isValidEmail } from './utils/helpers.js';
// State
let isSignUpMode = false;
// DOM Elements
const authSection = document.getElementById('authSection');
const dashboardSection = document.getElementById('dashboardSection');
const authForm = document.getElementById('authForm');
const authTitle = document.getElementById('authTitle');
const authName = document.getElementById('authName');
const authEmail = document.getElementById('authEmail');
const authPassword = document.getElementById('authPassword');
const authSubmitBtn = document.getElementById('authSubmitBtn');
const authToggleText = document.getElementById('authToggleText');
const authToggleLink = document.getElementById('authToggleLink');
const nameLabel = document.getElementById('nameLabel');
const logoutBtn = document.getElementById('logoutBtn');
// Dashboard elements
const userName = document.getElementById('userName');
const docCount = document.getElementById('docCount');
const recoCount = document.getElementById('recoCount');
const appCount = document.getElementById('appCount');
// Check if user is already logged in
function checkAuth() {
    const user = StorageService.getCurrentUser();
    if (user) {
        showDashboard(user);
    }
    else {
        showAuth();
    }
}
function showAuth() {
    authSection.style.display = 'block';
    dashboardSection.style.display = 'none';
    logoutBtn.style.display = 'none';
}
function showDashboard(user) {
    authSection.style.display = 'none';
    dashboardSection.style.display = 'block';
    logoutBtn.style.display = 'block';
    // Update dashboard
    userName.textContent = user.name;
    // Get user documents
    const documents = StorageService.getDocuments(user.id);
    docCount.textContent = documents.length.toString();
    // Get recommendations count
    recoCount.textContent = mockUniversityPrograms.length.toString();
    // Get applications
    const applications = StorageService.getApplications(user.id);
    appCount.textContent = applications.length.toString();
}
function toggleAuthMode() {
    isSignUpMode = !isSignUpMode;
    if (isSignUpMode) {
        authTitle.textContent = 'Create Your Account';
        authName.style.display = 'block';
        nameLabel.style.display = 'block';
        authSubmitBtn.textContent = 'Sign Up';
        authToggleText.textContent = 'Already have an account?';
        authToggleLink.textContent = 'Sign In';
    }
    else {
        authTitle.textContent = 'Welcome to NoApplAI';
        authName.style.display = 'none';
        nameLabel.style.display = 'none';
        authSubmitBtn.textContent = 'Sign In';
        authToggleText.textContent = "Don't have an account?";
        authToggleLink.textContent = 'Sign Up';
    }
}
function handleAuth(e) {
    e.preventDefault();
    const email = authEmail.value.trim();
    const password = authPassword.value.trim();
    const name = authName.value.trim();
    // Validation
    if (!isValidEmail(email)) {
        alert('Please enter a valid email address');
        return;
    }
    if (password.length < 6) {
        alert('Password must be at least 6 characters');
        return;
    }
    if (isSignUpMode) {
        if (!name) {
            alert('Please enter your name');
            return;
        }
        // Check if user already exists
        const existingUsers = StorageService.getAllUsers();
        if (existingUsers.some(u => u.email === email)) {
            alert('An account with this email already exists. Please sign in.');
            return;
        }
        // Create new user
        const user = {
            id: generateId(),
            email,
            name,
            createdAt: new Date()
        };
        StorageService.saveUser(user);
        StorageService.setCurrentUser(user);
        alert('Account created successfully!');
        showDashboard(user);
    }
    else {
        // Sign in
        const existingUsers = StorageService.getAllUsers();
        const user = existingUsers.find(u => u.email === email);
        if (!user) {
            alert('No account found with this email. Please sign up.');
            return;
        }
        StorageService.setCurrentUser(user);
        showDashboard(user);
    }
    // Reset form
    authForm.reset();
}
function handleLogout() {
    if (confirm('Are you sure you want to log out?')) {
        StorageService.clearCurrentUser();
        location.reload();
    }
}
// Event listeners
authForm.addEventListener('submit', handleAuth);
authToggleLink.addEventListener('click', (e) => {
    e.preventDefault();
    toggleAuthMode();
});
logoutBtn.addEventListener('click', (e) => {
    e.preventDefault();
    handleLogout();
});
// Mobile navigation toggle
const navToggle = document.getElementById('navToggle');
const navMenu = document.getElementById('navMenu');
if (navToggle && navMenu) {
    navToggle.addEventListener('click', () => {
        navMenu.classList.toggle('active');
    });
}
// Initialize
checkAuth();
//# sourceMappingURL=index.js.map