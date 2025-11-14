/**
 * Analytics Hook
 * Client-side analytics for tracking user behavior and usage patterns
 */

"use client";

import { useEffect, useCallback, useRef } from "react";
import type {
  AnalyticsEvent,
  AnalyticsEventName,
  AnalyticsSession,
} from "@/types/analytics";

const STORAGE_KEY = "bahr_analytics_session";
const SESSION_TIMEOUT = 30 * 60 * 1000; // 30 minutes

/**
 * Generate a simple session ID
 */
function generateSessionId(): string {
  return `${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
}

/**
 * Get or create analytics session
 */
function getSession(): AnalyticsSession {
  if (typeof window === "undefined") {
    return {
      sessionId: generateSessionId(),
      startTime: Date.now(),
      pageViews: 0,
      events: [],
    };
  }

  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      const session: AnalyticsSession = JSON.parse(stored);
      const timeSinceStart = Date.now() - session.startTime;

      // Reuse session if within timeout
      if (timeSinceStart < SESSION_TIMEOUT) {
        return session;
      }
    }
  } catch (error) {
    console.warn("Failed to retrieve analytics session:", error);
  }

  // Create new session
  const newSession: AnalyticsSession = {
    sessionId: generateSessionId(),
    startTime: Date.now(),
    pageViews: 0,
    events: [],
  };

  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(newSession));
  } catch (error) {
    console.warn("Failed to save analytics session:", error);
  }

  return newSession;
}

/**
 * Save session to localStorage
 */
function saveSession(session: AnalyticsSession): void {
  if (typeof window === "undefined") return;

  try {
    // Keep only last 100 events to prevent storage overflow
    const trimmedSession = {
      ...session,
      events: session.events.slice(-100),
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(trimmedSession));
  } catch (error) {
    console.warn("Failed to save analytics session:", error);
  }
}

/**
 * Send analytics event to backend (optional)
 */
async function sendToBackend(event: AnalyticsEvent): Promise<void> {
  try {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    await fetch(`${apiUrl}/api/v1/analytics`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(event),
    });
  } catch (error) {
    // Silently fail - analytics shouldn't break the app
    console.debug("Analytics event not sent:", error);
  }
}

export function useAnalytics() {
  const sessionRef = useRef<AnalyticsSession | null>(null);

  useEffect(() => {
    // Initialize session on mount
    sessionRef.current = getSession();
  }, []);

  /**
   * Track a custom event
   */
  const track = useCallback(
    (
      name: AnalyticsEventName,
      properties?: Record<string, string | number | boolean>,
    ) => {
      if (!sessionRef.current) {
        sessionRef.current = getSession();
      }

      const event: AnalyticsEvent = {
        name,
        timestamp: Date.now(),
        sessionId: sessionRef.current.sessionId,
        properties,
      };

      // Add to session
      sessionRef.current.events.push(event);
      saveSession(sessionRef.current);

      // Send to backend (async, non-blocking)
      sendToBackend(event);

      // Log in development
      if (process.env.NODE_ENV === "development") {
        console.log("📊 Analytics:", name, properties);
      }
    },
    [],
  );

  /**
   * Track page view
   */
  const trackPageView = useCallback(
    (path: string) => {
      if (!sessionRef.current) {
        sessionRef.current = getSession();
      }

      sessionRef.current.pageViews += 1;
      saveSession(sessionRef.current);

      track("page_view", { path });
    },
    [track],
  );

  /**
   * Get current session stats
   */
  const getSessionStats = useCallback(() => {
    if (!sessionRef.current) {
      sessionRef.current = getSession();
    }

    const analyzeEvents = sessionRef.current.events.filter(
      (e) => e.name === "analyze_submit",
    );
    const successEvents = sessionRef.current.events.filter(
      (e) => e.name === "analyze_success",
    );
    const errorEvents = sessionRef.current.events.filter(
      (e) => e.name === "analyze_error",
    );

    return {
      sessionId: sessionRef.current.sessionId,
      duration: Date.now() - sessionRef.current.startTime,
      pageViews: sessionRef.current.pageViews,
      totalEvents: sessionRef.current.events.length,
      analyses: analyzeEvents.length,
      successes: successEvents.length,
      errors: errorEvents.length,
    };
  }, []);

  return {
    track,
    trackPageView,
    getSessionStats,
  };
}
