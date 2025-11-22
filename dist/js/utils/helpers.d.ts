export declare function generateId(): string;
export declare function formatFileSize(bytes: number): string;
export declare function formatDate(date: Date): string;
export declare function isValidEmail(email: string): boolean;
export declare function readFileAsBase64(file: File): Promise<string>;
export declare function truncateText(text: string, maxLength: number): string;
export declare function debounce<T extends (...args: any[]) => any>(func: T, wait: number): (...args: Parameters<T>) => void;
//# sourceMappingURL=helpers.d.ts.map