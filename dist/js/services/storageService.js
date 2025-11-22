const STORAGE_KEYS = {
    CURRENT_USER: 'noapplai_current_user',
    DOCUMENTS: 'noapplai_documents',
    APPLICATIONS: 'noapplai_applications',
    USERS: 'noapplai_users'
};
export class StorageService {
    // User management
    static getCurrentUser() {
        const userStr = localStorage.getItem(STORAGE_KEYS.CURRENT_USER);
        if (!userStr)
            return null;
        const user = JSON.parse(userStr);
        user.createdAt = new Date(user.createdAt);
        return user;
    }
    static setCurrentUser(user) {
        localStorage.setItem(STORAGE_KEYS.CURRENT_USER, JSON.stringify(user));
    }
    static clearCurrentUser() {
        localStorage.removeItem(STORAGE_KEYS.CURRENT_USER);
    }
    static getAllUsers() {
        const usersStr = localStorage.getItem(STORAGE_KEYS.USERS);
        if (!usersStr)
            return [];
        const users = JSON.parse(usersStr);
        return users.map((u) => ({
            ...u,
            createdAt: new Date(u.createdAt)
        }));
    }
    static saveUser(user) {
        const users = this.getAllUsers();
        const index = users.findIndex(u => u.id === user.id);
        if (index >= 0) {
            users[index] = user;
        }
        else {
            users.push(user);
        }
        localStorage.setItem(STORAGE_KEYS.USERS, JSON.stringify(users));
    }
    // Document management
    static getDocuments(userId) {
        const docsStr = localStorage.getItem(STORAGE_KEYS.DOCUMENTS);
        if (!docsStr)
            return [];
        const allDocs = JSON.parse(docsStr);
        return allDocs
            .filter((doc) => doc.userId === userId)
            .map((doc) => ({
            ...doc,
            uploadedAt: new Date(doc.uploadedAt)
        }));
    }
    static saveDocument(document) {
        const docsStr = localStorage.getItem(STORAGE_KEYS.DOCUMENTS);
        const allDocs = docsStr ? JSON.parse(docsStr) : [];
        allDocs.push(document);
        localStorage.setItem(STORAGE_KEYS.DOCUMENTS, JSON.stringify(allDocs));
    }
    static deleteDocument(documentId) {
        const docsStr = localStorage.getItem(STORAGE_KEYS.DOCUMENTS);
        if (!docsStr)
            return;
        const allDocs = JSON.parse(docsStr);
        const filtered = allDocs.filter((doc) => doc.id !== documentId);
        localStorage.setItem(STORAGE_KEYS.DOCUMENTS, JSON.stringify(filtered));
    }
    // Application management
    static getApplications(userId) {
        const appsStr = localStorage.getItem(STORAGE_KEYS.APPLICATIONS);
        if (!appsStr)
            return [];
        const allApps = JSON.parse(appsStr);
        return allApps
            .filter((app) => app.userId === userId)
            .map((app) => ({
            ...app,
            submittedAt: app.submittedAt ? new Date(app.submittedAt) : undefined,
            lastUpdated: new Date(app.lastUpdated)
        }));
    }
    static saveApplication(application) {
        const appsStr = localStorage.getItem(STORAGE_KEYS.APPLICATIONS);
        const allApps = appsStr ? JSON.parse(appsStr) : [];
        const index = allApps.findIndex((app) => app.id === application.id);
        if (index >= 0) {
            allApps[index] = application;
        }
        else {
            allApps.push(application);
        }
        localStorage.setItem(STORAGE_KEYS.APPLICATIONS, JSON.stringify(allApps));
    }
    static deleteApplication(applicationId) {
        const appsStr = localStorage.getItem(STORAGE_KEYS.APPLICATIONS);
        if (!appsStr)
            return;
        const allApps = JSON.parse(appsStr);
        const filtered = allApps.filter((app) => app.id !== applicationId);
        localStorage.setItem(STORAGE_KEYS.APPLICATIONS, JSON.stringify(filtered));
    }
    static clearAllData() {
        Object.values(STORAGE_KEYS).forEach(key => {
            localStorage.removeItem(key);
        });
    }
}
//# sourceMappingURL=storageService.js.map