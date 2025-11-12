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
 * Information about an alternative meter candidate - MULTI-CANDIDATE NEW
 */
export interface AlternativeMeter {
  /** Meter ID */
  id: number;
  /** Arabic name of the meter */
  name_ar: string;
  /** English transliteration */
  name_en: string;
  /** Confidence score (0.0 to 1.0) */
  confidence: number;
  /** The exact phonetic pattern that matched */
  matched_pattern: string;
  /** Transformations applied */
  transformations?: string[];
  /** Confidence difference from top candidate */
  confidence_diff: number;
}

/**
 * Information about detection uncertainty - MULTI-CANDIDATE NEW
 */
export interface DetectionUncertainty {
  /** Whether the detection is uncertain */
  is_uncertain: boolean;
  /** Reason for uncertainty: 'low_confidence', 'close_candidates' */
  reason?: string;
  /** Difference between top 2 candidates (if applicable) */
  top_diff?: number;
  /** Recommendation for the user: 'add_diacritics', 'manual_review' */
  recommendation?: string;
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
  /** Alternative meter candidates when detection is uncertain (MULTI-CANDIDATE NEW) */
  alternative_meters?: AlternativeMeter[] | null;
  /** Detection uncertainty information (MULTI-CANDIDATE NEW) */
  detection_uncertainty?: DetectionUncertainty | null;
  /** List of prosodic errors detected */
  errors: string[];
  /** List of improvement suggestions */
  suggestions: string[];
  /** Overall quality score (0-100) */
  score: number;
}

/**
 * Meter feedback request schema - FEEDBACK NEW
 */
export interface MeterFeedback {
  /** Original input text */
  text: string;
  /** Normalized version of the text */
  normalized_text: string;
  /** The meter that was detected by the system (Arabic name) */
  detected_meter: string;
  /** Confidence score of the detected meter */
  detected_confidence: number;
  /** The meter the user selected (may be same as detected) */
  user_selected_meter: string;
  /** List of alternative meters shown to the user */
  alternatives_shown: string[];
  /** Whether the input text had diacritical marks */
  has_tashkeel: boolean;
  /** Optional comment from the user */
  user_comment?: string;
  /** Feedback submission timestamp */
  timestamp: string;
}

/**
 * Feedback submission response - FEEDBACK NEW
 */
export interface FeedbackResponse {
  /** Success or error status */
  status: string;
  /** User-friendly message */
  message: string;
  /** Unique feedback identifier */
  feedback_id: string;
}
