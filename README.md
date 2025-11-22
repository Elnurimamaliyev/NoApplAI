# NoApplAI - Automated University Application Portal

A web application for managing university applications with automated document handling, program recommendations, and application tracking.

## Features

- **User Authentication**: Sign up and sign in functionality
- **Document Upload**: Upload and manage application documents (CV, transcripts, certificates, etc.)
- **Program Recommendations**: Get personalized university program recommendations based on your profile
- **Application Tracking**: Track multiple applications with status updates
- **Mock Data & APIs**: Built-in mock data for testing and demonstration

## Technology Stack

- **HTML5**: Semantic markup and structure
- **CSS3**: Modern, responsive styling
- **TypeScript**: Type-safe JavaScript for better code quality
- **LocalStorage**: Client-side data persistence

## Project Structure

```
NoApplAI/
├── dist/                      # Production files
│   ├── css/
│   │   └── styles.css        # Main stylesheet
│   ├── js/                   # Compiled JavaScript
│   ├── index.html            # Home/Dashboard page
│   ├── upload.html           # Document upload page
│   ├── recommendations.html  # Program recommendations page
│   └── tracking.html         # Application tracking page
├── src/                      # TypeScript source files
│   ├── services/            # Business logic services
│   │   ├── mockData.ts      # Mock university programs
│   │   ├── recommendationService.ts
│   │   └── storageService.ts
│   ├── types/               # TypeScript interfaces
│   │   └── index.ts
│   ├── utils/               # Helper functions
│   │   └── helpers.ts
│   ├── index.ts             # Home page logic
│   ├── upload.ts            # Upload page logic
│   ├── recommendations.ts   # Recommendations page logic
│   └── tracking.ts          # Tracking page logic
├── package.json
├── tsconfig.json
└── README.md
```

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm (comes with Node.js)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Elnurimamaliyev/NoApplAI.git
cd NoApplAI
```

2. Install dependencies:
```bash
npm install
```

3. Build the TypeScript files:
```bash
npm run build
```

### Running the Application

1. Start a local web server:
```bash
npm run serve
```

2. Open your browser and navigate to:
```
http://localhost:8080
```

### Development Mode

To watch for changes and automatically recompile TypeScript:
```bash
npm run watch
```

## Usage Guide

### 1. Sign Up / Sign In
- Visit the home page
- Create a new account by clicking "Sign Up"
- Enter your name, email, and password
- Or sign in if you already have an account

### 2. Upload Documents
- Navigate to "Upload Documents" page
- Select document type from dropdown
- Choose a file from your computer
- Click "Upload Document"
- View and manage your uploaded documents

### 3. Get Recommendations
- Navigate to "Recommendations" page
- Enter your GPA
- Optionally select preferred countries
- Click "Apply Filters"
- View personalized program recommendations
- Click "Apply Now" to create an application

### 4. Track Applications
- Navigate to "Track Applications" page
- View all your applications
- Filter by status (Draft, Submitted, Under Review, etc.)
- Submit draft applications
- Update application status (demo feature)
- Delete draft applications

## Features in Detail

### Document Management
- Support for multiple document types:
  - CV/Resume
  - Academic Transcript
  - Certificates
  - Motivation Letter
  - Recommendation Letter
- File size validation (max 10MB)
- Base64 encoding for storage
- Download uploaded documents

### Recommendation Engine
- Match score calculation based on:
  - GPA requirements
  - Document completeness
  - Country preferences
  - Tuition affordability
- Detailed match reasons
- Filterable by GPA and country

### Application Tracking
- Multiple status types:
  - Draft
  - Submitted
  - Under Review
  - Accepted
  - Rejected
  - Waitlisted
- Status progression (demo)
- Application notes
- Document attachment tracking

## Mock Data

The application includes 8 pre-configured university programs from:
- USA (MIT, Stanford, Carnegie Mellon)
- UK (University of Cambridge)
- Switzerland (ETH Zurich)
- Germany (Technical University of Munich)
- Canada (University of Toronto)
- Singapore (National University of Singapore)

## Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge

## Future Enhancements

- Backend API integration
- Real authentication system
- File upload to cloud storage
- Email notifications
- Advanced search and filters
- Application deadline reminders
- Document templates
- Multi-language support

## License

MIT License

## Author

Elnur Imamaliyev