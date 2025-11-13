/**
 * Analyze Page - Main interface for Arabic verse analysis.
 * Users can input verses and see comprehensive prosodic analysis results.
 */

"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { AnalyzeForm } from "@/components/AnalyzeForm";
import { AnalyzeResults } from "@/components/AnalyzeResults";
import { AnalysisLoadingSkeleton } from "@/components/Skeleton";
import { ExampleVerses } from "@/components/ExampleVerses";
import { Toast, useToast } from "@/components/Toast";
import { useAnalyze } from "@/hooks/useAnalyze";
import { useAnalytics } from "@/hooks/useAnalytics";
import type { AnalyzeResponse } from "@/types/analyze";

export default function AnalyzePage() {
  const [result, setResult] = useState<AnalyzeResponse | null>(null);
  const [lastSubmittedText, setLastSubmittedText] = useState<string>("");
  const { mutate, isPending, error, reset } = useAnalyze();
  const { toast, showSuccess, hideToast } = useToast();
  const { track, trackPageView } = useAnalytics();

  // Track page view on mount
  useEffect(() => {
    trackPageView("/analyze");
  }, [trackPageView]);

  const handleSubmit = (
    text: string,
    precomputedPattern?: string,
    expectedMeter?: string,
  ) => {
    setLastSubmittedText(text);

    // Track analysis submission (V2 Enhanced)
    track("analyze_submit", {
      verse_length: text.length,
      has_diacritics: /[\u064B-\u0652]/.test(text),
      using_advanced_features: !!(precomputedPattern || expectedMeter),
      has_precomputed_pattern: !!precomputedPattern,
      has_expected_meter: !!expectedMeter,
    });

    mutate(
      {
        text,
        detect_bahr: true,
        suggest_corrections: true,
        analyze_rhyme: true, // V2: Enable rhyme analysis
        precomputed_pattern: precomputedPattern, // V2: 100% accuracy mode
        expected_meter: expectedMeter, // V2: Smart disambiguation
      },
      {
        onSuccess: (data) => {
          setResult(data);
          showSuccess("تم تحليل البيت الشعري بنجاح");

          // Track successful analysis (V2 Enhanced)
          track("analyze_success", {
            bahr_detected: data.bahr?.name_ar || "unknown",
            match_quality: data.bahr?.match_quality || "unknown",
            score: data.score,
            has_rhyme: !!data.rhyme,
            using_v2_features: !!(precomputedPattern || expectedMeter),
          });
        },
        onError: (err) => {
          // Track analysis error
          track("analyze_error", {
            error_message: err.message,
          });
        },
      },
    );
  };

  const handleExampleSelect = (text: string) => {
    track("example_click", {
      verse_preview: text.substring(0, 20),
    });
    handleSubmit(text);
  };

  const handleRetry = () => {
    if (lastSubmittedText) {
      track("retry_click");
      reset(); // Clear error
      handleSubmit(lastSubmittedText);
    }
  };

  const handleReset = () => {
    track("reset_click");
    setResult(null);
    setLastSubmittedText("");
    reset();
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">محلل الشعر</h1>
              <p className="mt-2 text-sm text-gray-600">
                نظام ذكي لتحليل الأوزان العروضية في الشعر العربي
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
        {/* Toast Notifications */}
        <Toast
          message={toast.message}
          type={toast.type}
          show={toast.show}
          onClose={hideToast}
        />

        {/* Form Section */}
        <section className="mb-12">
          <AnalyzeForm
            onSubmit={handleSubmit}
            onRetry={handleRetry}
            isLoading={isPending}
            error={error}
          />
        </section>

        {/* Examples Section */}
        {!result && !isPending && (
          <section className="max-w-3xl mx-auto mb-12">
            <ExampleVerses
              onSelect={handleExampleSelect}
              disabled={isPending}
            />
          </section>
        )}

        {/* Loading State */}
        {isPending && <AnalysisLoadingSkeleton />}

        {/* Results Section */}
        {result && !isPending && (
          <section>
            <AnalyzeResults result={result} onReset={handleReset} />
          </section>
        )}

        {/* Empty State */}
        {!result && !isPending && !error && (
          <div className="max-w-3xl mx-auto text-center py-12">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-blue-100 mb-4">
              <svg
                className="w-8 h-8 text-blue-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              ابدأ بإدخال بيت شعري
            </h3>
            <p className="text-gray-600">
              أدخل البيت الشعري في الحقل أعلاه للحصول على تحليل عروضي شامل
            </p>
          </div>
        )}
      </main>
    </div>
  );
}
