import { User, UserDocument, Application } from '../types/index.js';
export declare class StorageService {
    static getCurrentUser(): User | null;
    static setCurrentUser(user: User): void;
    static clearCurrentUser(): void;
    static getAllUsers(): User[];
    static saveUser(user: User): void;
    static getDocuments(userId: string): UserDocument[];
    static saveDocument(document: UserDocument): void;
    static deleteDocument(documentId: string): void;
    static getApplications(userId: string): Application[];
    static saveApplication(application: Application): void;
    static deleteApplication(applicationId: string): void;
    static clearAllData(): void;
}
//# sourceMappingURL=storageService.d.ts.map