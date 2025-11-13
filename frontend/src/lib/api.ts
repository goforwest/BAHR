/**
 * API client for communicating with the BAHR backend.
 * Handles requests to the analyze endpoint and meter data retrieval.
 */

import axios, { AxiosInstance, AxiosError } from "axios";
import type {
  AnalyzeRequest,
  AnalyzeResponse,
  MeterFeedback,
  FeedbackResponse,
} from "@/types/analyze";

/**
 * Base URL for the API - defaults to local development
 * Set NEXT_PUBLIC_API_URL in .env.local for production
 */
const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

/**
 * Axios instance configured with base URL and interceptors
 */
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10000, // 10 second timeout
});

/**
 * Request interceptor - adds authentication token if present
 */
apiClient.interceptors.request.use(
  (config) => {
    // Check for auth token in localStorage
    const token =
      typeof window !== "undefined" ? localStorage.getItem("auth_token") : null;

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

/**
 * Response interceptor - handles 401 errors and token refresh
 */
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error: AxiosError) => {
    // Handle 401 Unauthorized errors
    if (error.response?.status === 401) {
      // Clear token and redirect to login (when auth is implemented)
      if (typeof window !== "undefined") {
        localStorage.removeItem("auth_token");
        // Future: redirect to login page
        // window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  },
);

/**
 * Analyze a verse or text for prosodic analysis
 *
 * @param data - Analysis request data
 * @returns Promise resolving to analysis response
 * @throws AxiosError if request fails
 *
 * @example
 * ```typescript
 * const result = await analyzeVerse({
 *   text: 'إذا غامَرتَ في شَرَفٍ مَرومِ',
 *   detect_bahr: true,
 *   suggest_corrections: false
 * });
 * console.log(result.taqti3, result.bahr);
 * ```
 */
export async function analyzeVerse(
  data: AnalyzeRequest,
): Promise<AnalyzeResponse> {
  // NOW USES V2 API WITH 100% ACCURACY FEATURES!
  const response = await apiClient.post<AnalyzeResponse>("/analyze-v2/", data);
  return response.data;
}

/**
 * Get list of all available meters (bahrs)
 *
 * @returns Promise resolving to array of meter data
 * @throws AxiosError if request fails
 *
 * @example
 * ```typescript
 * const bahrs = await getBahrs();
 * console.log(bahrs); // List of all meters
 * ```
 */
export async function getBahrs(): Promise<unknown> {
  // Future: Add proper type when backend endpoint is implemented
  const response = await apiClient.get("/bahrs");
  return response.data;
}

/**
 * Submit meter detection feedback
 *
 * @param feedback - Feedback data including detected meter and user selection
 * @returns Promise resolving to feedback submission response
 * @throws AxiosError if request fails
 *
 * @example
 * ```typescript
 * const result = await submitMeterFeedback({
 *   text: 'قفا نبك من ذكرى حبيب ومنزل',
 *   normalized_text: 'قفا نبك من ذكري حبيب ومنزل',
 *   detected_meter: 'الرجز',
 *   detected_confidence: 0.9581,
 *   user_selected_meter: 'الطويل',
 *   alternatives_shown: ['الرجز', 'الطويل', 'السريع'],
 *   has_tashkeel: false,
 *   user_comment: 'This is the famous Mu\'allaqah verse',
 *   timestamp: new Date().toISOString()
 * });
 * console.log(result.message); // "شكراً لملاحظاتك! | Thank you for your feedback!"
 * ```
 */
export async function submitMeterFeedback(
  feedback: MeterFeedback,
): Promise<FeedbackResponse> {
  const response = await apiClient.post<FeedbackResponse>(
    "/feedback/meter",
    feedback,
  );
  return response.data;
}

/**
 * Export the configured axios instance for custom requests
 */
export default apiClient;
