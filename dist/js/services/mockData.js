import { DocumentType } from '../types/index.js';
export const mockUniversityPrograms = [
    {
        id: 'prog-1',
        universityName: 'Massachusetts Institute of Technology',
        programName: 'Computer Science',
        degree: 'Master',
        country: 'USA',
        tuitionFee: 53790,
        currency: 'USD',
        duration: '2 years',
        requirements: {
            minGPA: 3.5,
            languageTest: 'TOEFL 100+',
            requiredDocuments: [DocumentType.CV, DocumentType.Transcript, DocumentType.MotivationLetter]
        },
        description: 'World-class computer science program focusing on AI, machine learning, and software engineering.',
        deadline: new Date('2024-12-15')
    },
    {
        id: 'prog-2',
        universityName: 'Stanford University',
        programName: 'Artificial Intelligence',
        degree: 'Master',
        country: 'USA',
        tuitionFee: 58416,
        currency: 'USD',
        duration: '2 years',
        requirements: {
            minGPA: 3.7,
            languageTest: 'TOEFL 105+',
            requiredDocuments: [DocumentType.CV, DocumentType.Transcript, DocumentType.MotivationLetter, DocumentType.RecommendationLetter]
        },
        description: 'Leading AI program with research opportunities in neural networks, robotics, and NLP.',
        deadline: new Date('2024-11-30')
    },
    {
        id: 'prog-3',
        universityName: 'University of Cambridge',
        programName: 'Data Science',
        degree: 'Master',
        country: 'UK',
        tuitionFee: 35000,
        currency: 'GBP',
        duration: '1 year',
        requirements: {
            minGPA: 3.4,
            languageTest: 'IELTS 7.0+',
            requiredDocuments: [DocumentType.CV, DocumentType.Transcript, DocumentType.MotivationLetter]
        },
        description: 'Intensive data science program covering statistics, machine learning, and big data analytics.',
        deadline: new Date('2024-12-31')
    },
    {
        id: 'prog-4',
        universityName: 'ETH Zurich',
        programName: 'Computer Science',
        degree: 'Master',
        country: 'Switzerland',
        tuitionFee: 1500,
        currency: 'CHF',
        duration: '2 years',
        requirements: {
            minGPA: 3.3,
            languageTest: 'TOEFL 95+',
            requiredDocuments: [DocumentType.CV, DocumentType.Transcript, DocumentType.Certificate]
        },
        description: 'Excellence in computer science with low tuition fees and high quality education.',
        deadline: new Date('2024-12-15')
    },
    {
        id: 'prog-5',
        universityName: 'Technical University of Munich',
        programName: 'Informatics',
        degree: 'Master',
        country: 'Germany',
        tuitionFee: 0,
        currency: 'EUR',
        duration: '2 years',
        requirements: {
            minGPA: 3.0,
            languageTest: 'TOEFL 88+',
            requiredDocuments: [DocumentType.CV, DocumentType.Transcript]
        },
        description: 'Tuition-free computer science education with strong industry connections.',
        deadline: new Date('2025-01-15')
    },
    {
        id: 'prog-6',
        universityName: 'University of Toronto',
        programName: 'Computer Science',
        degree: 'Master',
        country: 'Canada',
        tuitionFee: 25000,
        currency: 'CAD',
        duration: '2 years',
        requirements: {
            minGPA: 3.3,
            languageTest: 'TOEFL 93+',
            requiredDocuments: [DocumentType.CV, DocumentType.Transcript, DocumentType.MotivationLetter]
        },
        description: 'Innovative CS program in one of North America\'s most diverse cities.',
        deadline: new Date('2025-01-05')
    },
    {
        id: 'prog-7',
        universityName: 'National University of Singapore',
        programName: 'Computer Science',
        degree: 'Master',
        country: 'Singapore',
        tuitionFee: 30000,
        currency: 'SGD',
        duration: '2 years',
        requirements: {
            minGPA: 3.2,
            languageTest: 'TOEFL 90+',
            requiredDocuments: [DocumentType.CV, DocumentType.Transcript, DocumentType.MotivationLetter]
        },
        description: 'Top-ranked Asian university with focus on technology and innovation.',
        deadline: new Date('2024-12-01')
    },
    {
        id: 'prog-8',
        universityName: 'Carnegie Mellon University',
        programName: 'Machine Learning',
        degree: 'Master',
        country: 'USA',
        tuitionFee: 51196,
        currency: 'USD',
        duration: '2 years',
        requirements: {
            minGPA: 3.6,
            languageTest: 'TOEFL 100+',
            requiredDocuments: [DocumentType.CV, DocumentType.Transcript, DocumentType.MotivationLetter, DocumentType.RecommendationLetter]
        },
        description: 'Premier machine learning program with world-renowned faculty.',
        deadline: new Date('2024-12-10')
    }
];
//# sourceMappingURL=mockData.js.map