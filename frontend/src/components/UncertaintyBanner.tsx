/**
 * UncertaintyBanner Component
 *
 * Displays a warning banner when meter detection is uncertain,
 * with recommendations for improving accuracy.
 */

import React from 'react';
import type { DetectionUncertainty } from '@/types/analyze';

interface UncertaintyBannerProps {
  uncertainty: DetectionUncertainty;
  onAddDiacritics?: () => void;
  onLearnMore?: () => void;
}

export default function UncertaintyBanner({
  uncertainty,
  onAddDiacritics,
  onLearnMore,
}: UncertaintyBannerProps) {
  // Don't show if detection is certain
  if (!uncertainty.is_uncertain) {
    return null;
  }

  // Determine message based on reason
  const getMessage = () => {
    switch (uncertainty.reason) {
      case 'low_confidence':
        return {
          ar: 'الثقة في التحديد منخفضة',
          en: 'Detection confidence is low',
        };
      case 'close_candidates':
        return {
          ar: 'هناك عدة احتمالات قريبة',
          en: 'Multiple close possibilities detected',
        };
      default:
        return {
          ar: 'التحديد غير مؤكد',
          en: 'Detection is uncertain',
        };
    }
  };

  const message = getMessage();

  return (
    <div className="bg-amber-50 border-l-4 border-amber-500 p-4 mb-4 rounded-r-md">
      <div className="flex items-start">
        <div className="flex-shrink-0">
          <svg
            className="h-5 w-5 text-amber-400"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            fill="currentColor"
            aria-hidden="true"
          >
            <path
              fillRule="evenodd"
              d="M8.485 3.495c.673-1.167 2.357-1.167 3.03 0l6.28 10.875c.673 1.167-.17 2.625-1.516 2.625H3.72c-1.347 0-2.189-1.458-1.515-2.625L8.485 3.495zM10 6a.75.75 0 01.75.75v3.5a.75.75 0 01-1.5 0v-3.5A.75.75 0 0110 6zm0 9a1 1 0 100-2 1 1 0 000 2z"
              clipRule="evenodd"
            />
          </svg>
        </div>
        <div className="mr-3 flex-1">
          <h3 className="text-sm font-medium text-amber-800">
            ⚠️ {message.ar} | {message.en}
          </h3>
          <div className="mt-2 text-sm text-amber-700">
            <p className="mb-2">
              {uncertainty.top_diff !== undefined && (
                <>
                  الفرق بين أعلى اختيارين: {(uncertainty.top_diff * 100).toFixed(2)}% |{' '}
                  Top 2 difference: {(uncertainty.top_diff * 100).toFixed(2)}%
                </>
              )}
            </p>

            {uncertainty.recommendation === 'add_diacritics' && (
              <div className="mt-3 space-y-2">
                <p className="font-medium">
                  💡 توصية | Recommendation:
                </p>
                <p>
                  إضافة التشكيل ستحسن الدقة بشكل كبير |
                  Adding diacritics (tashkeel) will significantly improve accuracy
                </p>
                <div className="mt-3 flex flex-wrap gap-2">
                  {onAddDiacritics && (
                    <button
                      onClick={onAddDiacritics}
                      className="inline-flex items-center px-3 py-2 border border-amber-600 text-sm font-medium rounded-md text-amber-700 bg-white hover:bg-amber-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-amber-500 transition-colors"
                    >
                      📝 أضف التشكيل | Add Diacritics
                    </button>
                  )}
                  {onLearnMore && (
                    <button
                      onClick={onLearnMore}
                      className="inline-flex items-center px-3 py-2 border border-amber-600 text-sm font-medium rounded-md text-amber-700 bg-white hover:bg-amber-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-amber-500 transition-colors"
                    >
                      ℹ️ اعرف المزيد | Learn More
                    </button>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
