/**
 * TypeScript types for the analyze API endpoint.
 * These interfaces match the backend Pydantic schemas exactly.
 */

/**
 * Request schema for verse analysis (V2 with 100% accuracy features).
 */
export interface AnalyzeRequest {
  /** Arabic verse or text to analyze (required, 5-2000 chars) */
  text: string;
  /** Whether to detect the meter (bahr) - default: true */
  detect_bahr?: boolean;
  /** Whether to suggest prosodic corrections - default: false */
  suggest_corrections?: boolean;
  /** Whether to analyze rhyme (qafiyah) - default: true */
  analyze_rhyme?: boolean;
  /** Pre-computed phonetic pattern (optional, for 100% accuracy mode). Format: /=haraka, o=sakin */
  precomputed_pattern?: string;
  /** Expected meter name in Arabic (optional, enables smart disambiguation). Example: 'الطويل' */
  expected_meter?: string;
}

/**
 * Information about a detected meter (bahr) - Enhanced with V2 explainability.
 */
export interface BahrInfo {
  /** Meter ID (1-20) */
  id: number;
  /** Arabic name of the meter */
  name_ar: string;
  /** English transliteration */
  name_en: string;
  /** Detection confidence score (0.0 to 1.0) */
  confidence: number;
  /** Match quality: 'exact', 'strong', 'moderate', or 'weak' (V2 NEW) */
  match_quality?: string;
  /** The exact phonetic pattern that matched (V2 NEW) */
  matched_pattern?: string;
  /** Zihafat/Ilal applied at each position, e.g. ['base', 'قبض', 'base', 'حذف'] (V2 NEW) */
  transformations?: string[];
  /** Arabic explanation of how the match was made (V2 NEW) */
  explanation_ar?: string;
  /** English explanation of how the match was made (V2 NEW) */
  explanation_en?: string;
}

/**
 * Rhyme information (qafiyah) - V2 NEW
 */
export interface RhymeInfo {
  /** Main rhyme letter (حرف الروي) */
  rawi: string;
  /** Vowel on the rawi ('i', 'u', 'a', or '' for sukun) */
  rawi_vowel: string;
  /** List of rhyme type classifications */
  rhyme_types: string[];
  /** Arabic description of the qafiyah */
  description_ar: string;
  /** English description of the qafiyah */
  description_en: string;
}

/**
 * Response schema for verse analysis (V2 Enhanced).
 */
export interface AnalyzeResponse {
  /** Original input text */
  text: string;
  /** Prosodic scansion result (tafa'il pattern) */
  taqti3: string;
  /** Detected meter information (if detect_bahr=true) */
  bahr: BahrInfo | null;
  /** Rhyme (qafiyah) information (V2 NEW) */
  rhyme?: RhymeInfo | null;
  /** List of prosodic errors detected */
  errors: string[];
  /** List of improvement suggestions */
  suggestions: string[];
  /** Overall quality score (0-100) */
  score: number;
}
