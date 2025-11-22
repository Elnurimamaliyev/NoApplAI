import { mockUniversityPrograms } from './mockData.js';
export class RecommendationService {
    static getRecommendations(userDocuments, userGPA = 3.5, preferredCountries = []) {
        const recommendations = [];
        for (const program of mockUniversityPrograms) {
            const matchScore = this.calculateMatchScore(program, userDocuments, userGPA, preferredCountries);
            const reasons = this.generateReasons(program, userDocuments, userGPA, matchScore);
            recommendations.push({
                program,
                matchScore,
                reasons
            });
        }
        // Sort by match score descending
        return recommendations.sort((a, b) => b.matchScore - a.matchScore);
    }
    static calculateMatchScore(program, userDocuments, userGPA, preferredCountries) {
        let score = 0;
        // GPA match (40 points max)
        if (userGPA >= program.requirements.minGPA) {
            const gpaExcess = userGPA - program.requirements.minGPA;
            score += Math.min(40, 30 + (gpaExcess * 10));
        }
        else {
            const gpaDeficit = program.requirements.minGPA - userGPA;
            score += Math.max(0, 20 - (gpaDeficit * 20));
        }
        // Document completeness (30 points max)
        const userDocTypes = new Set(userDocuments.map(doc => doc.type));
        const requiredDocs = program.requirements.requiredDocuments;
        const completedDocs = requiredDocs.filter(docType => userDocTypes.has(docType)).length;
        score += (completedDocs / requiredDocs.length) * 30;
        // Country preference (20 points max)
        if (preferredCountries.length === 0 || preferredCountries.includes(program.country)) {
            score += 20;
        }
        else {
            score += 5;
        }
        // Tuition affordability bonus (10 points max)
        const tuitionInUSD = this.convertToUSD(program.tuitionFee, program.currency);
        if (tuitionInUSD === 0) {
            score += 10;
        }
        else if (tuitionInUSD < 10000) {
            score += 8;
        }
        else if (tuitionInUSD < 30000) {
            score += 5;
        }
        else {
            score += 2;
        }
        return Math.round(Math.min(100, score));
    }
    static generateReasons(program, userDocuments, userGPA, matchScore) {
        const reasons = [];
        // GPA reasons
        if (userGPA >= program.requirements.minGPA + 0.3) {
            reasons.push(`Your GPA (${userGPA.toFixed(1)}) exceeds the minimum requirement`);
        }
        else if (userGPA >= program.requirements.minGPA) {
            reasons.push(`Your GPA meets the minimum requirement`);
        }
        else {
            reasons.push(`Your GPA is slightly below the requirement (need ${program.requirements.minGPA})`);
        }
        // Document reasons
        const userDocTypes = new Set(userDocuments.map(doc => doc.type));
        const requiredDocs = program.requirements.requiredDocuments;
        const missingDocs = requiredDocs.filter(docType => !userDocTypes.has(docType));
        if (missingDocs.length === 0) {
            reasons.push('All required documents uploaded');
        }
        else {
            reasons.push(`Missing ${missingDocs.length} required document(s)`);
        }
        // Tuition reasons
        const tuitionInUSD = this.convertToUSD(program.tuitionFee, program.currency);
        if (tuitionInUSD === 0) {
            reasons.push('Tuition-free education');
        }
        else if (tuitionInUSD < 10000) {
            reasons.push('Very affordable tuition fees');
        }
        // Program quality
        if (matchScore >= 80) {
            reasons.push('Strong overall match for your profile');
        }
        else if (matchScore >= 60) {
            reasons.push('Good match for your profile');
        }
        return reasons;
    }
    static convertToUSD(amount, currency) {
        // Simple conversion rates (in real app, use live API)
        const rates = {
            USD: 1,
            EUR: 1.1,
            GBP: 1.27,
            CHF: 1.15,
            CAD: 0.74,
            SGD: 0.74
        };
        return amount * (rates[currency] || 1);
    }
}
//# sourceMappingURL=recommendationService.js.map