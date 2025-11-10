/**
 * Analyze Page - Main interface for Arabic verse analysis.
 * Users can input verses and see comprehensive prosodic analysis results.
 */

'use client';

import { useState } from 'react';
import Link from 'next/link';
import { AnalyzeForm } from '@/components/AnalyzeForm';
import { AnalyzeResults } from '@/components/AnalyzeResults';
import { useAnalyze } from '@/hooks/useAnalyze';
import type { AnalyzeResponse } from '@/types/analyze';

export default function AnalyzePage() {
  const [result, setResult] = useState<AnalyzeResponse | null>(null);
  const { mutate, isPending, error } = useAnalyze();

  const handleSubmit = (text: string) => {
    mutate(
      { text, detect_bahr: true, suggest_corrections: false },
      {
        onSuccess: (data) => {
          setResult(data);
        },
      }
    );
  };

  const handleReset = () => {
    setResult(null);
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
        {/* Form Section */}
        <section className="mb-12">
          <AnalyzeForm onSubmit={handleSubmit} isLoading={isPending} error={error} />
        </section>

        {/* Results Section */}
        {result && (
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
