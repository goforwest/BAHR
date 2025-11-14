/**
 * MultiCandidateView Component
 *
 * Displays multiple meter candidates when detection is uncertain,
 * allowing users to select the correct meter and provide feedback.
 */

import React, { useState } from "react";
import type { BahrInfo, AlternativeMeter } from "@/types/analyze";

interface MultiCandidateViewProps {
  /** The top detected meter */
  topMeter: BahrInfo;
  /** Alternative meter candidates */
  alternatives: AlternativeMeter[];
  /** Callback when user selects a different meter */
  onMeterSelected?: (meterNameAr: string) => void;
  /** Callback when user wants to report correct meter */
  onReportCorrectMeter?: () => void;
}

export default function MultiCandidateView({
  topMeter,
  alternatives,
  onMeterSelected,
  onReportCorrectMeter,
}: MultiCandidateViewProps) {
  const [selectedMeter, setSelectedMeter] = useState<string>(topMeter.name_ar);
  const [expandedId, setExpandedId] = useState<number | null>(null);

  // Combine top meter with alternatives
  const allCandidates = [
    {
      ...topMeter,
      confidence_diff: 0,
      rank: 1,
      medal: "🥇",
    },
    ...alternatives.map((alt, idx) => ({
      ...alt,
      rank: idx + 2,
      medal: idx === 0 ? "🥈" : idx === 1 ? "🥉" : "🏅",
    })),
  ];

  const handleSelection = (meterNameAr: string) => {
    setSelectedMeter(meterNameAr);
    if (onMeterSelected) {
      onMeterSelected(meterNameAr);
    }
  };

  const toggleExpanded = (id: number) => {
    setExpandedId(expandedId === id ? null : id);
  };

  return (
    <div className="bg-white border-2 border-amber-300 rounded-lg p-4 mb-4">
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-amber-200">
        <h3 className="text-lg font-bold text-gray-900">
          ⚠️ احتمالات متعددة | Multiple Possibilities
        </h3>
        {onReportCorrectMeter && (
          <button
            onClick={onReportCorrectMeter}
            className="text-sm px-3 py-1 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
          >
            💬 أبلغ عن البحر الصحيح | Report Correct Meter
          </button>
        )}
      </div>

      <div className="space-y-3">
        {allCandidates.map((candidate) => (
          <div
            key={candidate.id}
            className={`
              border-2 rounded-lg p-4 transition-all cursor-pointer
              ${
                selectedMeter === candidate.name_ar
                  ? "border-blue-500 bg-blue-50"
                  : "border-gray-200 hover:border-gray-300 bg-white"
              }
            `}
            onClick={() => handleSelection(candidate.name_ar)}
          >
            <div className="flex items-start justify-between">
              <div className="flex items-start space-x-3 space-x-reverse flex-1">
                {/* Radio button */}
                <div className="flex-shrink-0 mt-1">
                  <input
                    type="radio"
                    name="meter-selection"
                    checked={selectedMeter === candidate.name_ar}
                    onChange={() => handleSelection(candidate.name_ar)}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300"
                    onClick={(e) => e.stopPropagation()}
                  />
                </div>

                {/* Meter info */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center flex-wrap gap-2 mb-2">
                    <span
                      className="text-xl"
                      aria-label={`Rank ${candidate.rank}`}
                    >
                      {candidate.medal}
                    </span>
                    <h4 className="text-lg font-bold text-gray-900">
                      {candidate.name_ar}
                    </h4>
                    <span className="text-sm text-gray-600">
                      ({candidate.name_en})
                    </span>
                  </div>

                  {/* Confidence bar */}
                  <div className="mb-2">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm font-medium text-gray-700">
                        الثقة | Confidence
                      </span>
                      <span className="text-sm font-bold text-gray-900">
                        {(candidate.confidence * 100).toFixed(2)}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full transition-all ${
                          candidate.rank === 1
                            ? "bg-green-500"
                            : candidate.rank === 2
                              ? "bg-blue-500"
                              : "bg-gray-400"
                        }`}
                        style={{ width: `${candidate.confidence * 100}%` }}
                      />
                    </div>
                    {"confidence_diff" in candidate &&
                      candidate.confidence_diff > 0 && (
                        <p className="text-xs text-gray-500 mt-1">
                          -{(candidate.confidence_diff * 100).toFixed(2)}% من
                          الأول | from top
                        </p>
                      )}
                  </div>

                  {/* Expandable details */}
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      toggleExpanded(candidate.id);
                    }}
                    className="text-sm text-blue-600 hover:text-blue-800 flex items-center gap-1"
                  >
                    {expandedId === candidate.id ? "▼" : "▶"} عرض التفاصيل |
                    Show details
                  </button>

                  {expandedId === candidate.id && (
                    <div className="mt-3 p-3 bg-gray-50 rounded text-sm space-y-2">
                      <div>
                        <span className="font-medium">النمط | Pattern:</span>
                        <code className="block mt-1 text-xs bg-white p-2 rounded border border-gray-200 overflow-x-auto dir-ltr">
                          {candidate.matched_pattern}
                        </code>
                      </div>
                      {candidate.transformations &&
                        candidate.transformations.length > 0 && (
                          <div>
                            <span className="font-medium">
                              التحولات | Transformations:
                            </span>
                            <div className="flex flex-wrap gap-1 mt-1">
                              {candidate.transformations.map((trans, idx) => (
                                <span
                                  key={idx}
                                  className="inline-block px-2 py-1 bg-white rounded border border-gray-200 text-xs"
                                >
                                  {trans}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg text-sm text-gray-700">
        <p>
          💡 <strong>نصيحة | Tip:</strong> اختر البحر الذي تعتقد أنه صحيح.
          سيساعد اختيارك في تحسين النظام. | Select the meter you believe is
          correct. Your selection helps improve the system.
        </p>
      </div>
    </div>
  );
}
