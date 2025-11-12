/**
 * Component to display verse analysis results.
 * Shows verse text, prosodic scansion (taqti3), detected meter (bahr), and quality score.
 * Includes multi-candidate detection UI and feedback collection.
 */

'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import type { AnalyzeResponse } from '@/types/analyze';
import UncertaintyBanner from './UncertaintyBanner';
import MultiCandidateView from './MultiCandidateView';
import FeedbackDialog from './FeedbackDialog';

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
  const { text, taqti3, bahr, score, alternative_meters, detection_uncertainty } = result;

  // State for feedback dialog
  const [showFeedbackDialog, setShowFeedbackDialog] = useState(false);
  const [selectedMeter, setSelectedMeter] = useState<string | undefined>(
    bahr?.name_ar
  );

  // Check if we should show multi-candidate view
  const hasAlternatives = alternative_meters && alternative_meters.length > 0;
  const isUncertain = detection_uncertainty?.is_uncertain;

  const handleMeterSelected = (meterNameAr: string) => {
    setSelectedMeter(meterNameAr);
  };

  const handleReportCorrectMeter = () => {
    setShowFeedbackDialog(true);
  };

  const handleAddDiacritics = () => {
    // Scroll back to input form
    window.scrollTo({ top: 0, behavior: 'smooth' });
    // Could also trigger some hint/guide for adding diacritics
  };

  const handleLearnMore = () => {
    // Open learn more link (could be a modal or external link)
    window.open('https://ar.wikipedia.org/wiki/عروض_(شعر)', '_blank');
  };

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
      <motion.div 
        variants={itemVariants}
        whileHover="hover"
        initial="initial"
        className="bg-white shadow-lg rounded-lg p-6 transition-shadow hover:shadow-xl"
      >
        <h3 className="text-sm font-medium text-gray-500 mb-3">البيت الشعري</h3>
        <p
          dir="rtl"
          className="font-[family-name:var(--font-amiri)] text-2xl leading-relaxed text-gray-900"
        >
          {text}
        </p>
      </motion.div>

      {/* Taqti3 Card */}
      {taqti3 && taqti3.trim() && taqti3 !== 'غير محدد' && taqti3 !== 'خطأ في التحليل' && (
        <motion.div
          variants={itemVariants}
          whileHover="hover"
          initial="initial"
          className="bg-white shadow-lg rounded-lg p-6 transition-shadow hover:shadow-xl"
        >
          <h3 className="text-sm font-medium text-gray-500 mb-3">التقطيع العروضي</h3>
          <p
            dir="rtl"
            className="font-mono text-lg text-blue-900 bg-blue-50 p-4 rounded-md overflow-x-auto whitespace-pre-wrap"
          >
            {taqti3}
          </p>
        </motion.div>
      )}

      {/* Uncertainty Banner - Show when detection is uncertain */}
      {detection_uncertainty && isUncertain && (
        <motion.div variants={itemVariants}>
          <UncertaintyBanner
            uncertainty={detection_uncertainty}
            onAddDiacritics={handleAddDiacritics}
            onLearnMore={handleLearnMore}
          />
        </motion.div>
      )}

      {/* Multi-Candidate View - Show when there are alternatives */}
      {bahr && hasAlternatives && alternative_meters && (
        <motion.div variants={itemVariants}>
          <MultiCandidateView
            topMeter={bahr}
            alternatives={alternative_meters}
            onMeterSelected={handleMeterSelected}
            onReportCorrectMeter={handleReportCorrectMeter}
          />
        </motion.div>
      )}

      {/* Traditional Bahr Card - Show only when no alternatives */}
      {bahr && !hasAlternatives && (
        <motion.div
          variants={itemVariants}
          whileHover="hover"
          initial="initial"
          className="bg-white shadow-lg rounded-lg p-6 transition-shadow hover:shadow-xl"
        >
          <h3 className="text-sm font-medium text-gray-500 mb-3">البحر الشعري</h3>
          <div className="space-y-4">
            <div className="flex items-baseline justify-between">
              <span className="text-xl font-bold text-gray-900">{bahr.name_ar}</span>
              <span className="text-sm text-gray-500 font-mono">{bahr.name_en}</span>
            </div>

            {/* Confidence */}
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

            {/* Match Quality (V2 NEW) */}
            {bahr.match_quality && (
              <div className="flex items-center justify-between pt-2 border-t border-gray-100">
                <span className="text-sm font-medium text-gray-600">جودة المطابقة</span>
                <span
                  className={`text-sm font-semibold px-3 py-1 rounded-full ${
                    bahr.match_quality === 'exact'
                      ? 'bg-green-100 text-green-800'
                      : bahr.match_quality === 'strong'
                      ? 'bg-blue-100 text-blue-800'
                      : bahr.match_quality === 'moderate'
                      ? 'bg-yellow-100 text-yellow-800'
                      : 'bg-gray-100 text-gray-800'
                  }`}
                >
                  {bahr.match_quality === 'exact'
                    ? 'مطابقة تامة'
                    : bahr.match_quality === 'strong'
                    ? 'مطابقة قوية'
                    : bahr.match_quality === 'moderate'
                    ? 'مطابقة متوسطة'
                    : 'مطابقة ضعيفة'}
                </span>
              </div>
            )}

            {/* Transformations (V2 NEW) */}
            {bahr.transformations && bahr.transformations.length > 0 && (
              <div className="pt-2 border-t border-gray-100">
                <span className="text-sm font-medium text-gray-600 mb-2 block">الزحافات والعلل</span>
                <div className="flex flex-wrap gap-2">
                  {bahr.transformations.map((transform, idx) => (
                    <span
                      key={idx}
                      className={`text-xs px-2 py-1 rounded ${
                        transform === 'base'
                          ? 'bg-gray-100 text-gray-700'
                          : 'bg-purple-100 text-purple-800 font-medium'
                      }`}
                    >
                      {transform === 'base' ? 'أصلية' : transform}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Explanation (V2 NEW) */}
            {bahr.explanation_ar && (
              <div className="pt-2 border-t border-gray-100">
                <span className="text-sm font-medium text-gray-600 mb-1 block">التفسير</span>
                <p className="text-sm text-gray-700 leading-relaxed" dir="rtl">
                  {bahr.explanation_ar}
                </p>
                {bahr.explanation_en && (
                  <p className="text-xs text-gray-500 mt-1 leading-relaxed">
                    {bahr.explanation_en}
                  </p>
                )}
              </div>
            )}

            {/* Matched Pattern (V2 NEW - Advanced) */}
            {bahr.matched_pattern && (
              <details className="pt-2 border-t border-gray-100">
                <summary className="text-sm font-medium text-gray-600 cursor-pointer hover:text-gray-800">
                  التفاصيل التقنية
                </summary>
                <div className="mt-2 bg-gray-50 p-3 rounded">
                  <p className="text-xs text-gray-600 mb-1">النمط الصوتي:</p>
                  <code className="text-xs font-mono text-gray-800 block bg-white p-2 rounded border border-gray-200">
                    {bahr.matched_pattern}
                  </code>
                  <p className="text-xs text-gray-500 mt-2">
                    / = حركة (متحرك) | o = سكون (ساكن)
                  </p>
                </div>
              </details>
            )}
          </div>
        </motion.div>
      )}

      {/* Score Card */}
      <motion.div
        variants={itemVariants}
        whileHover="hover"
        initial="initial"
        className="bg-white shadow-lg rounded-lg p-6 transition-shadow hover:shadow-xl"
      >
        <h3 className="text-sm font-medium text-gray-500 mb-3">درجة الجودة</h3>
        <div>
          <div className="flex items-center justify-between mb-2">
            <span className="text-3xl font-bold text-gray-900">{score.toFixed(1)}</span>
            <span className="text-sm text-gray-500">من 100</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-4">
            <div
              className={`h-4 rounded-full transition-all duration-500 ${
                score >= 90
                  ? 'bg-green-500'
                  : score >= 80
                  ? 'bg-blue-500'
                  : score >= 70
                  ? 'bg-yellow-500'
                  : score >= 50
                  ? 'bg-orange-500'
                  : 'bg-red-500'
              }`}
              style={{ width: `${Math.min(score, 100)}%` }}
            />
          </div>
          <div className="mt-3 flex items-center gap-2">
            <span
              className={`inline-block px-3 py-1 text-sm font-semibold rounded-full ${
                score >= 90
                  ? 'bg-green-100 text-green-800'
                  : score >= 80
                  ? 'bg-blue-100 text-blue-800'
                  : score >= 70
                  ? 'bg-yellow-100 text-yellow-800'
                  : score >= 50
                  ? 'bg-orange-100 text-orange-800'
                  : 'bg-red-100 text-red-800'
              }`}
            >
              {score >= 90
                ? '✨ ممتاز'
                : score >= 80
                ? '✓ جيد جداً'
                : score >= 70
                ? '~ جيد'
                : score >= 50
                ? '⚠ مقبول'
                : '✗ ضعيف'}
            </span>
            <p className="text-sm text-gray-600">
              {score >= 90
                ? 'البيت موافق للوزن تماماً'
                : score >= 80
                ? 'البيت موافق للوزن مع اختلافات طفيفة'
                : score >= 70
                ? 'البيت جيد مع بعض الملاحظات'
                : score >= 50
                ? 'البيت يحتاج إلى مراجعة'
                : 'البيت يحتاج إلى تحسين'}
            </p>
          </div>
        </div>
      </motion.div>

      {/* Rhyme Card (V2 NEW) */}
      {result.rhyme && (
        <motion.div
          variants={itemVariants}
          whileHover="hover"
          initial="initial"
          className="bg-white shadow-lg rounded-lg p-6 transition-shadow hover:shadow-xl"
        >
          <h3 className="text-sm font-medium text-gray-500 mb-3">القافية</h3>
          <div className="space-y-3">
            {/* Rawi */}
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-gray-600">حرف الروي</span>
              <span className="text-2xl font-bold text-purple-900">{result.rhyme.rawi}</span>
            </div>

            {/* Rhyme Types */}
            {result.rhyme.rhyme_types && result.rhyme.rhyme_types.length > 0 && (
              <div>
                <span className="text-sm font-medium text-gray-600 mb-2 block">نوع القافية</span>
                <div className="flex flex-wrap gap-2">
                  {result.rhyme.rhyme_types.map((type, idx) => (
                    <span
                      key={idx}
                      className="text-xs px-3 py-1 rounded-full bg-purple-100 text-purple-800 font-medium"
                    >
                      {type}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Description */}
            {result.rhyme.description_ar && (
              <div className="pt-2 border-t border-gray-100">
                <p className="text-sm text-gray-700 leading-relaxed" dir="rtl">
                  {result.rhyme.description_ar}
                </p>
                {result.rhyme.description_en && (
                  <p className="text-xs text-gray-500 mt-1">
                    {result.rhyme.description_en}
                  </p>
                )}
              </div>
            )}
          </div>
        </motion.div>
      )}

      {/* Errors and Suggestions */}
      {result.errors && result.errors.length > 0 && (
        <motion.div 
          variants={itemVariants}
          whileHover="hover"
          initial="initial"
          className="bg-red-50 border border-red-200 shadow-lg rounded-lg p-6 transition-shadow hover:shadow-xl"
        >
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
        <motion.div 
          variants={itemVariants}
          whileHover="hover"
          initial="initial"
          className="bg-blue-50 border border-blue-200 shadow-lg rounded-lg p-6 transition-shadow hover:shadow-xl"
        >
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

      {/* Feedback Dialog - Hidden until user clicks "Report Correct Meter" */}
      {bahr && alternative_meters && (
        <FeedbackDialog
          isOpen={showFeedbackDialog}
          onClose={() => setShowFeedbackDialog(false)}
          text={text}
          detectedMeter={bahr}
          alternatives={alternative_meters}
          selectedMeter={selectedMeter}
        />
      )}
    </motion.div>
  );
}
