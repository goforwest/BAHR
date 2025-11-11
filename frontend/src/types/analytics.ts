/**
 * Analytics Types
 * Defines event tracking structure for usage analytics
 */

export type AnalyticsEventName =
  | 'page_view'
  | 'analyze_submit'
  | 'analyze_success'
  | 'analyze_error'
  | 'example_click'
  | 'retry_click'
  | 'reset_click'
  | 'api_call'
  | 'api_error';

export interface AnalyticsEvent {
  name: AnalyticsEventName;
  timestamp: number;
  properties?: Record<string, string | number | boolean>;
  sessionId: string;
  userId?: string;
}

export interface AnalyticsSession {
  sessionId: string;
  startTime: number;
  pageViews: number;
  events: AnalyticsEvent[];
}

export interface AnalyticsStats {
  totalSessions: number;
  totalPageViews: number;
  totalAnalyses: number;
  successRate: number;
  avgResponseTime: number;
  topErrors: Array<{ error: string; count: number }>;
  dailyUsage: Array<{ date: string; count: number }>;
}
