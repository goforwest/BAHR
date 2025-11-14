/**
 * Analytics Dashboard - View usage statistics
 */

"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useAnalytics } from "@/hooks/useAnalytics";

interface StatsData {
  total_sessions: number;
  total_events: number;
  total_analyses: number;
  success_rate: number;
  top_events: Array<{ name: string; count: number }>;
}

export default function AnalyticsPage() {
  const { getSessionStats, trackPageView } = useAnalytics();
  const [stats, setStats] = useState<StatsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const sessionStats = getSessionStats();

  useEffect(() => {
    trackPageView("/analytics");
    fetchStats();
  }, [trackPageView]);

  const fetchStats = async () => {
    try {
      setLoading(true);
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const response = await fetch(`${apiUrl}/api/v1/analytics/stats?days=7`);

      if (!response.ok) {
        throw new Error("Failed to fetch analytics");
      }

      const data = await response.json();
      setStats(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                📊 لوحة التحليلات
              </h1>
              <p className="mt-2 text-sm text-gray-600">
                إحصائيات الاستخدام والتحليل
              </p>
            </div>
            <Link
              href="/"
              className="text-blue-600 hover:text-blue-700 font-medium text-sm transition-colors"
            >
              ← العودة للرئيسية
            </Link>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Current Session Stats */}
        <section className="mb-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            الجلسة الحالية
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="bg-white rounded-lg shadow p-6">
              <div className="text-sm text-gray-600 mb-2">معرف الجلسة</div>
              <div className="text-xs font-mono text-gray-900 truncate">
                {sessionStats.sessionId}
              </div>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <div className="text-sm text-gray-600 mb-2">مشاهدات الصفحات</div>
              <div className="text-3xl font-bold text-blue-600">
                {sessionStats.pageViews}
              </div>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <div className="text-sm text-gray-600 mb-2">إجمالي الأحداث</div>
              <div className="text-3xl font-bold text-blue-600">
                {sessionStats.totalEvents}
              </div>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <div className="text-sm text-gray-600 mb-2">التحليلات</div>
              <div className="text-3xl font-bold text-green-600">
                {sessionStats.analyses}
              </div>
            </div>
          </div>
        </section>

        {/* Global Stats */}
        <section>
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            الإحصائيات العامة (آخر 7 أيام)
          </h2>

          {loading && (
            <div className="bg-white rounded-lg shadow p-12 text-center">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
              <p className="mt-4 text-gray-600">جاري التحميل...</p>
            </div>
          )}

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
              <p className="text-red-700">⚠️ {error}</p>
              <button
                onClick={fetchStats}
                className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
              >
                إعادة المحاولة
              </button>
            </div>
          )}

          {stats && !loading && (
            <div className="space-y-6">
              {/* Summary Cards */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div className="bg-white rounded-lg shadow p-6">
                  <div className="text-sm text-gray-600 mb-2">
                    إجمالي الجلسات
                  </div>
                  <div className="text-3xl font-bold text-gray-900">
                    {stats.total_sessions.toLocaleString()}
                  </div>
                </div>
                <div className="bg-white rounded-lg shadow p-6">
                  <div className="text-sm text-gray-600 mb-2">
                    إجمالي الأحداث
                  </div>
                  <div className="text-3xl font-bold text-blue-600">
                    {stats.total_events.toLocaleString()}
                  </div>
                </div>
                <div className="bg-white rounded-lg shadow p-6">
                  <div className="text-sm text-gray-600 mb-2">التحليلات</div>
                  <div className="text-3xl font-bold text-green-600">
                    {stats.total_analyses.toLocaleString()}
                  </div>
                </div>
                <div className="bg-white rounded-lg shadow p-6">
                  <div className="text-sm text-gray-600 mb-2">نسبة النجاح</div>
                  <div className="text-3xl font-bold text-green-600">
                    {(stats.success_rate * 100).toFixed(1)}%
                  </div>
                </div>
              </div>

              {/* Top Events */}
              {stats.top_events && stats.top_events.length > 0 && (
                <div className="bg-white rounded-lg shadow p-6">
                  <h3 className="text-lg font-bold text-gray-900 mb-4">
                    الأحداث الأكثر شيوعًا
                  </h3>
                  <div className="space-y-3">
                    {stats.top_events.map((event, index) => (
                      <div
                        key={index}
                        className="flex items-center justify-between"
                      >
                        <div className="flex items-center gap-3">
                          <span className="text-2xl font-bold text-gray-400">
                            {index + 1}
                          </span>
                          <span className="font-mono text-sm text-gray-700">
                            {event.name}
                          </span>
                        </div>
                        <div className="flex items-center gap-4">
                          <div className="text-right">
                            <div className="text-lg font-bold text-blue-600">
                              {event.count.toLocaleString()}
                            </div>
                          </div>
                          <div className="w-32 bg-gray-200 rounded-full h-2">
                            <div
                              className="bg-blue-600 h-2 rounded-full"
                              style={{
                                width: `${(event.count / stats.top_events[0].count) * 100}%`,
                              }}
                            />
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
