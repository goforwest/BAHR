/**
 * Component to display verse analysis results.
 * Shows verse text, prosodic scansion (taqti3), detected meter (bahr), and quality score.
 */

'use client';

import type { AnalyzeResponse } from '@/types/analyze';

interface AnalyzeResultsProps {
  result: AnalyzeResponse;
}

export function AnalyzeResults({ result }: AnalyzeResultsProps) {
  const { text, taqti3, bahr, score } = result;

  return (
    <div className="w-full max-w-3xl mx-auto mt-8 space-y-6">
      {/* Verse Text Card */}
      <div className="bg-white shadow-lg rounded-lg p-6">
        <h3 className="text-sm font-medium text-gray-500 mb-3">البيت الشعري</h3>
        <p
          dir="rtl"
          className="font-[family-name:var(--font-amiri)] text-2xl leading-relaxed text-gray-900"
        >
          {text}
        </p>
      </div>

      {/* Taqti3 Card */}
      <div className="bg-white shadow-lg rounded-lg p-6">
        <h3 className="text-sm font-medium text-gray-500 mb-3">التقطيع العروضي</h3>
        <p
          dir="rtl"
          className="font-mono text-lg text-blue-900 bg-blue-50 p-4 rounded-md overflow-x-auto"
        >
          {taqti3}
        </p>
      </div>

      {/* Bahr Card */}
      {bahr && (
        <div className="bg-white shadow-lg rounded-lg p-6">
          <h3 className="text-sm font-medium text-gray-500 mb-3">البحر الشعري</h3>
          <div className="space-y-3">
            <div className="flex items-baseline justify-between">
              <span className="text-xl font-bold text-gray-900">{bahr.name_ar}</span>
              <span className="text-sm text-gray-500 font-mono">{bahr.name_en}</span>
            </div>
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-600">نسبة الثقة</span>
                <span className="text-sm font-bold text-blue-600">
                  {(bahr.confidence * 100).toFixed(1)}%
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2.5">
                <div
                  className="bg-blue-600 h-2.5 rounded-full transition-all duration-500"
                  style={{ width: `${bahr.confidence * 100}%` }}
                />
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Score Card */}
      <div className="bg-white shadow-lg rounded-lg p-6">
        <h3 className="text-sm font-medium text-gray-500 mb-3">درجة الجودة</h3>
        <div>
          <div className="flex items-center justify-between mb-2">
            <span className="text-2xl font-bold text-gray-900">{score}</span>
            <span className="text-sm text-gray-500">من 100</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-4">
            <div
              className={`h-4 rounded-full transition-all duration-500 ${
                score >= 80
                  ? 'bg-green-500'
                  : score >= 60
                  ? 'bg-yellow-500'
                  : 'bg-red-500'
              }`}
              style={{ width: `${score}%` }}
            />
          </div>
          <p className="mt-2 text-sm text-gray-600">
            {score >= 80
              ? 'ممتاز! البيت موافق للوزن'
              : score >= 60
              ? 'جيد، مع بعض الملاحظات'
              : 'يحتاج إلى مراجعة'}
          </p>
        </div>
      </div>

      {/* Errors and Suggestions */}
      {result.errors && result.errors.length > 0 && (
        <div className="bg-red-50 border border-red-200 shadow-lg rounded-lg p-6">
          <h3 className="text-sm font-medium text-red-800 mb-3">الأخطاء العروضية</h3>
          <ul className="space-y-2">
            {result.errors.map((error, index) => (
              <li key={index} className="text-sm text-red-700 flex items-start gap-2">
                <span className="text-red-500 mt-0.5">•</span>
                <span>{error}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {result.suggestions && result.suggestions.length > 0 && (
        <div className="bg-blue-50 border border-blue-200 shadow-lg rounded-lg p-6">
          <h3 className="text-sm font-medium text-blue-800 mb-3">اقتراحات التحسين</h3>
          <ul className="space-y-2">
            {result.suggestions.map((suggestion, index) => (
              <li key={index} className="text-sm text-blue-700 flex items-start gap-2">
                <span className="text-blue-500 mt-0.5">•</span>
                <span>{suggestion}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
