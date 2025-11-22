import { UserDocument, DocumentType, User } from './types/index.js';
import { StorageService } from './services/storageService.js';
import { generateId, formatFileSize, formatDate, readFileAsBase64 } from './utils/helpers.js';

// Check authentication
const currentUser = StorageService.getCurrentUser();
if (!currentUser) {
    alert('Please sign in first');
    window.location.href = 'index.html';
}

// DOM Elements
const documentTypeSelect = document.getElementById('documentType') as HTMLSelectElement;
const fileInput = document.getElementById('fileInput') as HTMLInputElement;
const fileName = document.getElementById('fileName') as HTMLElement;
const uploadBtn = document.getElementById('uploadBtn') as HTMLButtonElement;
const documentsList = document.getElementById('documentsList') as HTMLElement;
const logoutBtn = document.getElementById('logoutBtn') as HTMLElement;

// State
let selectedFile: File | null = null;

// Load existing documents
function loadDocuments() {
    if (!currentUser) return;
    
    const documents = StorageService.getDocuments(currentUser.id);
    
    if (documents.length === 0) {
        documentsList.innerHTML = '<p class="no-documents">No documents uploaded yet</p>';
        return;
    }
    
    documentsList.innerHTML = documents.map(doc => `
        <div class="document-item" data-doc-id="${doc.id}">
            <div class="document-info">
                <div class="document-type">${formatDocumentType(doc.type)}</div>
                <div class="document-name">${doc.fileName}</div>
                <div class="document-meta">
                    ${formatFileSize(doc.fileSize)} • Uploaded on ${formatDate(doc.uploadedAt)}
                </div>
            </div>
            <div class="document-actions">
                <button class="btn btn-sm btn-secondary download-btn" data-doc-id="${doc.id}">
                    Download
                </button>
                <button class="btn btn-sm btn-danger delete-btn" data-doc-id="${doc.id}">
                    Delete
                </button>
            </div>
        </div>
    `).join('');
    
    // Add event listeners to action buttons
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', handleDeleteDocument);
    });
    
    document.querySelectorAll('.download-btn').forEach(btn => {
        btn.addEventListener('click', handleDownloadDocument);
    });
}

function formatDocumentType(type: DocumentType): string {
    const typeMap: { [key in DocumentType]: string } = {
        [DocumentType.CV]: 'CV / Resume',
        [DocumentType.Transcript]: 'Academic Transcript',
        [DocumentType.Certificate]: 'Certificate',
        [DocumentType.MotivationLetter]: 'Motivation Letter',
        [DocumentType.RecommendationLetter]: 'Recommendation Letter'
    };
    return typeMap[type] || type;
}

function handleFileSelect(e: Event) {
    const target = e.target as HTMLInputElement;
    const file = target.files?.[0];
    
    if (file) {
        selectedFile = file;
        fileName.textContent = file.name;
        uploadBtn.disabled = false;
    } else {
        selectedFile = null;
        fileName.textContent = 'No file chosen';
        uploadBtn.disabled = true;
    }
}

async function handleUpload() {
    if (!selectedFile || !currentUser) return;
    
    // Validate file size (max 10MB)
    const maxSize = 10 * 1024 * 1024;
    if (selectedFile.size > maxSize) {
        alert('File size must be less than 10MB');
        return;
    }
    
    uploadBtn.disabled = true;
    uploadBtn.textContent = 'Uploading...';
    
    try {
        // Read file as base64
        const fileData = await readFileAsBase64(selectedFile);
        
        // Create document object
        const userDocument: UserDocument = {
            id: generateId(),
            userId: currentUser.id,
            type: documentTypeSelect.value as DocumentType,
            fileName: selectedFile.name,
            fileSize: selectedFile.size,
            uploadedAt: new Date(),
            fileData
        };
        
        // Save to storage
        StorageService.saveDocument(userDocument);
        
        // Reset form
        fileInput.value = '';
        fileName.textContent = 'No file chosen';
        selectedFile = null;
        uploadBtn.disabled = true;
        uploadBtn.textContent = 'Upload Document';
        
        // Reload documents list
        loadDocuments();
        
        alert('Document uploaded successfully!');
    } catch (error) {
        console.error('Upload error:', error);
        alert('Failed to upload document. Please try again.');
        uploadBtn.disabled = false;
        uploadBtn.textContent = 'Upload Document';
    }
}

function handleDeleteDocument(e: Event) {
    const target = e.target as HTMLElement;
    const docId = target.dataset.docId;
    
    if (!docId) return;
    
    if (confirm('Are you sure you want to delete this document?')) {
        StorageService.deleteDocument(docId);
        loadDocuments();
        alert('Document deleted successfully!');
    }
}

function handleDownloadDocument(e: Event) {
    const target = e.target as HTMLElement;
    const docId = target.dataset.docId;
    
    if (!docId || !currentUser) return;
    
    const documents = StorageService.getDocuments(currentUser.id);
    const userDoc = documents.find(doc => doc.id === docId);
    
    if (!userDoc || !userDoc.fileData) {
        alert('Document data not found');
        return;
    }
    
    // Create download link
    const link = document.createElement('a');
    link.href = `data:application/octet-stream;base64,${userDoc.fileData}`;
    link.download = userDoc.fileName;
    link.click();
}

function handleLogout() {
    if (confirm('Are you sure you want to log out?')) {
        StorageService.clearCurrentUser();
        window.location.href = 'index.html';
    }
}

// Event listeners
fileInput.addEventListener('change', handleFileSelect);
uploadBtn.addEventListener('click', handleUpload);
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
loadDocuments();
