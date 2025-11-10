/**
 * Component to display verse analysis results.
 * Shows verse text, prosodic scansion (taqti3), detected meter (bahr), and quality score.
 */

'use client';

import { motion } from 'framer-motion';
import type { AnalyzeResponse } from '@/types/analyze';

interface AnalyzeResultsProps {
  result: AnalyzeResponse;
  onReset?: () => void;
}

// Animation variants for fade-in effect
const containerVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.4,
      staggerChildren: 0.1,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 10 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.3 },
  },
};

export function AnalyzeResults({ result, onReset }: AnalyzeResultsProps) {
  const { text, taqti3, bahr, score } = result;

  return (
    <motion.div
      className="w-full max-w-3xl mx-auto mt-8 space-y-6"
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {/* Reset Button */}
      {onReset && (
        <motion.div variants={itemVariants} className="flex justify-end">
          <button
            onClick={onReset}
            className="px-6 py-2 bg-white hover:bg-gray-50 text-gray-700 font-medium rounded-lg shadow-md hover:shadow-lg transition-all duration-200 flex items-center gap-2 border border-gray-200"
          >
            <svg
              className="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
              />
            </svg>
            <span>تحليل جديد</span>
          </button>
        </motion.div>
      )}

      {/* Verse Text Card */}
      <motion.div variants={itemVariants} className="bg-white shadow-lg rounded-lg p-6">
        <h3 className="text-sm font-medium text-gray-500 mb-3">البيت الشعري</h3>
        <p
          dir="rtl"
          className="font-[family-name:var(--font-amiri)] text-2xl leading-relaxed text-gray-900"
        >
          {text}
        </p>
      </motion.div>

      {/* Taqti3 Card */}
      <motion.div variants={itemVariants} className="bg-white shadow-lg rounded-lg p-6">
        <h3 className="text-sm font-medium text-gray-500 mb-3">التقطيع العروضي</h3>
        <p
          dir="rtl"
          className="font-mono text-lg text-blue-900 bg-blue-50 p-4 rounded-md overflow-x-auto"
        >
          {taqti3}
        </p>
      </motion.div>

      {/* Bahr Card */}
      {bahr && (
        <motion.div variants={itemVariants} className="bg-white shadow-lg rounded-lg p-6">
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
        </motion.div>
      )}

      {/* Score Card */}
      <motion.div variants={itemVariants} className="bg-white shadow-lg rounded-lg p-6">
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
      </motion.div>

      {/* Errors and Suggestions */}
      {result.errors && result.errors.length > 0 && (
        <motion.div variants={itemVariants} className="bg-red-50 border border-red-200 shadow-lg rounded-lg p-6">
          <h3 className="text-sm font-medium text-red-800 mb-3">الأخطاء العروضية</h3>
          <ul className="space-y-2">
            {result.errors.map((error, index) => (
              <li key={index} className="text-sm text-red-700 flex items-start gap-2">
                <span className="text-red-500 mt-0.5">•</span>
                <span>{error}</span>
              </li>
            ))}
          </ul>
        </motion.div>
      )}

      {result.suggestions && result.suggestions.length > 0 && (
        <motion.div variants={itemVariants} className="bg-blue-50 border border-blue-200 shadow-lg rounded-lg p-6">
          <h3 className="text-sm font-medium text-blue-800 mb-3">اقتراحات التحسين</h3>
          <ul className="space-y-2">
            {result.suggestions.map((suggestion, index) => (
              <li key={index} className="text-sm text-blue-700 flex items-start gap-2">
                <span className="text-blue-500 mt-0.5">•</span>
                <span>{suggestion}</span>
              </li>
            ))}
          </ul>
        </motion.div>
      )}
    </motion.div>
  );
}
