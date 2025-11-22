// Document types
export var DocumentType;
(function (DocumentType) {
    DocumentType["CV"] = "cv";
    DocumentType["Transcript"] = "transcript";
    DocumentType["Certificate"] = "certificate";
    DocumentType["MotivationLetter"] = "motivation_letter";
    DocumentType["RecommendationLetter"] = "recommendation_letter";
})(DocumentType || (DocumentType = {}));
// Application types
export var ApplicationStatus;
(function (ApplicationStatus) {
    ApplicationStatus["Draft"] = "draft";
    ApplicationStatus["Submitted"] = "submitted";
    ApplicationStatus["UnderReview"] = "under_review";
    ApplicationStatus["Accepted"] = "accepted";
    ApplicationStatus["Rejected"] = "rejected";
    ApplicationStatus["Waitlisted"] = "waitlisted";
})(ApplicationStatus || (ApplicationStatus = {}));
//# sourceMappingURL=index.js.map