/**
 * TypeScript types for the analyze API endpoint.
 * These interfaces match the backend Pydantic schemas exactly.
 */

/**
 * Request schema for verse analysis.
 */
export interface AnalyzeRequest {
  /** Arabic verse or text to analyze (required, 5-2000 chars) */
  text: string;
  /** Whether to detect the meter (bahr) - default: true */
  detect_bahr?: boolean;
  /** Whether to suggest prosodic corrections - default: false */
  suggest_corrections?: boolean;
}

/**
 * Information about a detected meter (bahr).
 */
export interface BahrInfo {
  /** Arabic name of the meter */
  name_ar: string;
  /** English transliteration */
  name_en: string;
  /** Detection confidence score (0.0 to 1.0) */
  confidence: number;
}

/**
 * Response schema for verse analysis.
 */
export interface AnalyzeResponse {
  /** Original input text */
  text: string;
  /** Prosodic scansion result (tafa'il pattern) */
  taqti3: string;
  /** Detected meter information (if detect_bahr=true) */
  bahr: BahrInfo | null;
  /** List of prosodic errors detected */
  errors: string[];
  /** List of improvement suggestions */
  suggestions: string[];
  /** Overall quality score (0-100) */
  score: number;
}
