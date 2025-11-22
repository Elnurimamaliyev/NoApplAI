import { UserDocument, Recommendation } from '../types/index.js';
export declare class RecommendationService {
    static getRecommendations(userDocuments: UserDocument[], userGPA?: number, preferredCountries?: string[]): Recommendation[];
    private static calculateMatchScore;
    private static generateReasons;
    private static convertToUSD;
}
//# sourceMappingURL=recommendationService.d.ts.map