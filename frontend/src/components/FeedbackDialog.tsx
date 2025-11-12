/**
 * FeedbackDialog Component
 *
 * Modal dialog for collecting user feedback on meter detection.
 * Allows users to report the correct meter and add optional comments.
 */

import React, { useState } from 'react';
import { submitMeterFeedback } from '@/lib/api';
import type { MeterFeedback, BahrInfo, AlternativeMeter } from '@/types/analyze';

interface FeedbackDialogProps {
  isOpen: boolean;
  onClose: () => void;
  /** Original input text */
  text: string;
  /** Detected meter */
  detectedMeter: BahrInfo;
  /** Alternative meters shown to user */
  alternatives: AlternativeMeter[];
  /** Currently selected meter (may be different from detected) */
  selectedMeter?: string;
}

export default function FeedbackDialog({
  isOpen,
  onClose,
  text,
  detectedMeter,
  alternatives,
  selectedMeter,
}: FeedbackDialogProps) {
  const [comment, setComment] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitStatus, setSubmitStatus] = useState<'idle' | 'success' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState('');

  // Collect all meter options
  const allMeters = [
    detectedMeter.name_ar,
    ...alternatives.map((alt) => alt.name_ar),
  ];

  const [correctMeter, setCorrectMeter] = useState(
    selectedMeter || detectedMeter.name_ar
  );

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSubmitStatus('idle');
    setErrorMessage('');

    try {
      // Check if text has diacritics (تشكيل)
      const hasTashkeel = /[\u064B-\u0652]/.test(text);

      // Build feedback data
      const feedbackData: MeterFeedback = {
        text: text,
        normalized_text: text, // Frontend doesn't normalize, backend will handle it
        detected_meter: detectedMeter.name_ar,
        detected_confidence: detectedMeter.confidence,
        user_selected_meter: correctMeter,
        alternatives_shown: allMeters,
        has_tashkeel: hasTashkeel,
        user_comment: comment.trim(),
        timestamp: new Date().toISOString(),
      };

      // Submit to API
      const response = await submitMeterFeedback(feedbackData);

      if (response.status === 'success') {
        setSubmitStatus('success');
        // Close dialog after 2 seconds
        setTimeout(() => {
          onClose();
          // Reset state
          setComment('');
          setSubmitStatus('idle');
        }, 2000);
      }
    } catch (error) {
      console.error('Failed to submit feedback:', error);
      setSubmitStatus('error');
      setErrorMessage(
        error instanceof Error ? error.message : 'Failed to submit feedback'
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-gray-900">
              💬 أبلغ عن البحر الصحيح | Report Correct Meter
            </h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 transition-colors"
              aria-label="Close"
            >
              <svg
                className="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
        </div>

        {/* Body */}
        <form onSubmit={handleSubmit} className="px-6 py-4">
          {/* Show original text */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              النص | Text
            </label>
            <div className="p-3 bg-gray-50 rounded border border-gray-200 text-right">
              <p className="text-lg">{text}</p>
            </div>
          </div>

          {/* Show detected meter */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              البحر المكتشف | Detected Meter
            </label>
            <div className="p-3 bg-red-50 rounded border border-red-200">
              <p className="text-lg font-bold">
                {detectedMeter.name_ar} ({detectedMeter.name_en}) -{' '}
                {(detectedMeter.confidence * 100).toFixed(2)}%
              </p>
            </div>
          </div>

          {/* Select correct meter */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              البحر الصحيح | Correct Meter *
            </label>
            <select
              value={correctMeter}
              onChange={(e) => setCorrectMeter(e.target.value)}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {allMeters.map((meter) => (
                <option key={meter} value={meter}>
                  {meter}
                  {meter === detectedMeter.name_ar && ' (مكتشف | detected)'}
                </option>
              ))}
            </select>
          </div>

          {/* Optional comment */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              تعليق إضافي (اختياري) | Additional Comment (Optional)
            </label>
            <textarea
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              rows={3}
              placeholder="أضف أي ملاحظات إضافية هنا... | Add any additional notes here..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            />
          </div>

          {/* Status messages */}
          {submitStatus === 'success' && (
            <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-md">
              <p className="text-green-800 text-sm">
                ✓ شكراً لملاحظاتك! | Thank you for your feedback!
              </p>
            </div>
          )}

          {submitStatus === 'error' && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md">
              <p className="text-red-800 text-sm">
                ✗ فشل في إرسال الملاحظات | Failed to submit feedback
              </p>
              {errorMessage && (
                <p className="text-red-600 text-xs mt-1">{errorMessage}</p>
              )}
            </div>
          )}

          {/* Footer buttons */}
          <div className="flex justify-end gap-3 pt-4 border-t border-gray-200">
            <button
              type="button"
              onClick={onClose}
              disabled={isSubmitting}
              className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition-colors disabled:opacity-50"
            >
              إلغاء | Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting || submitStatus === 'success'}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSubmitting ? (
                <>
                  <svg
                    className="animate-spin inline-block h-4 w-4 mr-2"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                  جاري الإرسال... | Submitting...
                </>
              ) : (
                'إرسال | Submit'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
