/**
 * React Query hooks for verse analysis API.
 * Provides mutation hooks for analyzing Arabic verses.
 */

'use client';

import { useMutation, type UseMutationResult } from '@tanstack/react-query';
import { analyzeVerse } from '@/lib/api';
import type { AnalyzeRequest, AnalyzeResponse } from '@/types/analyze';

/**
 * Custom React Query hook for verse analysis
 * 
 * Uses useMutation for POST requests to the /analyze endpoint.
 * Handles loading states, errors, and successful responses automatically.
 * 
 * @returns Mutation object with mutate, data, isLoading, error, etc.
 * 
 * @example
 * ```typescript
 * function AnalyzeForm() {
 *   const { mutate, data, isLoading, error } = useAnalyze();
 * 
 *   const handleSubmit = (text: string) => {
 *     mutate({ text, detect_bahr: true });
 *   };
 * 
 *   if (isLoading) return <div>جارٍ التحليل...</div>;
 *   if (error) return <div>خطأ: {error.message}</div>;
 *   if (data) return <div>النتيجة: {data.taqti3}</div>;
 * }
 * ```
 */
export function useAnalyze(): UseMutationResult<
  AnalyzeResponse,
  Error,
  AnalyzeRequest,
  unknown
> {
  return useMutation<AnalyzeResponse, Error, AnalyzeRequest>({
    mutationFn: analyzeVerse,
    onSuccess: (data) => {
      // Optional: Log successful analysis
      console.log('Analysis completed:', data);
    },
    onError: (error) => {
      // Optional: Log errors
      console.error('Analysis failed:', error);
    },
  });
}

/**
 * Type export for the hook return value
 */
export type UseAnalyzeReturn = ReturnType<typeof useAnalyze>;
