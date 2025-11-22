export interface User {
    id: string;
    email: string;
    name: string;
    createdAt: Date;
}
export declare enum DocumentType {
    CV = "cv",
    Transcript = "transcript",
    Certificate = "certificate",
    MotivationLetter = "motivation_letter",
    RecommendationLetter = "recommendation_letter"
}
export interface UserDocument {
    id: string;
    userId: string;
    type: DocumentType;
    fileName: string;
    fileSize: number;
    uploadedAt: Date;
    fileData?: string;
}
export interface UniversityProgram {
    id: string;
    universityName: string;
    programName: string;
    degree: 'Bachelor' | 'Master' | 'PhD';
    country: string;
    tuitionFee: number;
    currency: string;
    duration: string;
    requirements: {
        minGPA: number;
        languageTest?: string;
        requiredDocuments: DocumentType[];
    };
    description: string;
    deadline: Date;
}
export declare enum ApplicationStatus {
    Draft = "draft",
    Submitted = "submitted",
    UnderReview = "under_review",
    Accepted = "accepted",
    Rejected = "rejected",
    Waitlisted = "waitlisted"
}
export interface Application {
    id: string;
    userId: string;
    programId: string;
    status: ApplicationStatus;
    submittedAt?: Date;
    lastUpdated: Date;
    documents: string[];
    notes?: string;
}
export interface Recommendation {
    program: UniversityProgram;
    matchScore: number;
    reasons: string[];
}
//# sourceMappingURL=index.d.ts.map