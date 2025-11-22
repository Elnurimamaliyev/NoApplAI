import { User, UserDocument, Application } from '../types/index.js';

const STORAGE_KEYS = {
  CURRENT_USER: 'noapplai_current_user',
  DOCUMENTS: 'noapplai_documents',
  APPLICATIONS: 'noapplai_applications',
  USERS: 'noapplai_users'
};

export class StorageService {
  // User management
  static getCurrentUser(): User | null {
    const userStr = localStorage.getItem(STORAGE_KEYS.CURRENT_USER);
    if (!userStr) return null;
    const user = JSON.parse(userStr);
    user.createdAt = new Date(user.createdAt);
    return user;
  }

  static setCurrentUser(user: User): void {
    localStorage.setItem(STORAGE_KEYS.CURRENT_USER, JSON.stringify(user));
  }

  static clearCurrentUser(): void {
    localStorage.removeItem(STORAGE_KEYS.CURRENT_USER);
  }

  static getAllUsers(): User[] {
    const usersStr = localStorage.getItem(STORAGE_KEYS.USERS);
    if (!usersStr) return [];
    const users = JSON.parse(usersStr);
    return users.map((u: any) => ({
      ...u,
      createdAt: new Date(u.createdAt)
    }));
  }

  static saveUser(user: User): void {
    const users = this.getAllUsers();
    const index = users.findIndex(u => u.id === user.id);
    if (index >= 0) {
      users[index] = user;
    } else {
      users.push(user);
    }
    localStorage.setItem(STORAGE_KEYS.USERS, JSON.stringify(users));
  }

  // Document management
  static getDocuments(userId: string): UserDocument[] {
    const docsStr = localStorage.getItem(STORAGE_KEYS.DOCUMENTS);
    if (!docsStr) return [];
    const allDocs = JSON.parse(docsStr);
    return allDocs
      .filter((doc: any) => doc.userId === userId)
      .map((doc: any) => ({
        ...doc,
        uploadedAt: new Date(doc.uploadedAt)
      }));
  }

  static saveDocument(document: UserDocument): void {
    const docsStr = localStorage.getItem(STORAGE_KEYS.DOCUMENTS);
    const allDocs = docsStr ? JSON.parse(docsStr) : [];
    allDocs.push(document);
    localStorage.setItem(STORAGE_KEYS.DOCUMENTS, JSON.stringify(allDocs));
  }

  static deleteDocument(documentId: string): void {
    const docsStr = localStorage.getItem(STORAGE_KEYS.DOCUMENTS);
    if (!docsStr) return;
    const allDocs = JSON.parse(docsStr);
    const filtered = allDocs.filter((doc: any) => doc.id !== documentId);
    localStorage.setItem(STORAGE_KEYS.DOCUMENTS, JSON.stringify(filtered));
  }

  // Application management
  static getApplications(userId: string): Application[] {
    const appsStr = localStorage.getItem(STORAGE_KEYS.APPLICATIONS);
    if (!appsStr) return [];
    const allApps = JSON.parse(appsStr);
    return allApps
      .filter((app: any) => app.userId === userId)
      .map((app: any) => ({
        ...app,
        submittedAt: app.submittedAt ? new Date(app.submittedAt) : undefined,
        lastUpdated: new Date(app.lastUpdated)
      }));
  }

  static saveApplication(application: Application): void {
    const appsStr = localStorage.getItem(STORAGE_KEYS.APPLICATIONS);
    const allApps = appsStr ? JSON.parse(appsStr) : [];
    const index = allApps.findIndex((app: any) => app.id === application.id);
    
    if (index >= 0) {
      allApps[index] = application;
    } else {
      allApps.push(application);
    }
    localStorage.setItem(STORAGE_KEYS.APPLICATIONS, JSON.stringify(allApps));
  }

  static deleteApplication(applicationId: string): void {
    const appsStr = localStorage.getItem(STORAGE_KEYS.APPLICATIONS);
    if (!appsStr) return;
    const allApps = JSON.parse(appsStr);
    const filtered = allApps.filter((app: any) => app.id !== applicationId);
    localStorage.setItem(STORAGE_KEYS.APPLICATIONS, JSON.stringify(filtered));
  }

  static clearAllData(): void {
    Object.values(STORAGE_KEYS).forEach(key => {
      localStorage.removeItem(key);
    });
  }
}
