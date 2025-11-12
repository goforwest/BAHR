/**
 * Form component for Arabic verse analysis input.
 * Features RTL layout, Arabic validation, and loading states.
 */

'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { LoadingSpinner } from './LoadingSpinner';

// Validation schema with Zod (V2 Enhanced)
const analyzeSchema = z.object({
  text: z
    .string()
    .min(5, 'يجب أن يحتوي النص على 5 أحرف على الأقل')
    .max(500, 'يجب أن لا يتجاوز النص 500 حرف')
    .regex(/[\u0600-\u06FF]/, 'يجب أن يحتوي النص على أحرف عربية'),
  precomputed_pattern: z.string().optional(),
  expected_meter: z.string().optional(),
  showAdvanced: z.boolean().optional(),
});

type AnalyzeFormData = z.infer<typeof analyzeSchema>;

interface AnalyzeFormProps {
  onSubmit: (text: string, precomputedPattern?: string, expectedMeter?: string) => void;
  onRetry?: () => void;
  isLoading?: boolean;
  error?: Error | null;
}

/**
 * Get user-friendly error message in Arabic with retry suggestions
 */
function getErrorMessage(error: Error | null): { title: string; message: string; canRetry: boolean } {
  if (!error) return { title: '', message: '', canRetry: false };
  
  const message = error.message.toLowerCase();
  
  // Network errors
  if (message.includes('network') || message.includes('fetch') || message.includes('failed to fetch')) {
    return {
      title: 'خطأ في الاتصال',
      message: 'تعذر الاتصال بالخادم. يرجى التحقق من اتصالك بالإنترنت والمحاولة مرة أخرى.',
      canRetry: true
    };
  }
  
  // Server errors (500)
  if (message.includes('500') || message.includes('server error') || message.includes('internal server')) {
    return {
      title: 'خطأ في الخادم',
      message: 'حدث خطأ مؤقت في الخادم. يرجى المحاولة مرة أخرى بعد قليل.',
      canRetry: true
    };
  }
  
  // Validation errors (400, 422)
  if (message.includes('invalid') || message.includes('validation') || message.includes('400') || message.includes('422')) {
    return {
      title: 'خطأ في المدخلات',
      message: 'يرجى التأكد من إدخال بيت شعري صحيح باللغة العربية.',
      canRetry: false
    };
  }
  
  // Timeout errors
  if (message.includes('timeout') || message.includes('timed out')) {
    return {
      title: 'انتهت مهلة الطلب',
      message: 'استغرق التحليل وقتاً أطول من المتوقع. يرجى المحاولة مرة أخرى.',
      canRetry: true
    };
  }
  
  // Default error message
  return {
    title: 'حدث خطأ',
    message: error.message || 'حدث خطأ غير متوقع. يرجى المحاولة مرة أخرى.',
    canRetry: true
  };
}

export function AnalyzeForm({ onSubmit, onRetry, isLoading = false, error = null }: AnalyzeFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
    setValue,
  } = useForm<AnalyzeFormData>({
    resolver: zodResolver(analyzeSchema),
    defaultValues: {
      showAdvanced: false,
    },
  });

  const handleFormSubmit = (data: AnalyzeFormData) => {
    onSubmit(data.text, data.precomputed_pattern, data.expected_meter);
  };

  const showAdvanced = watch('showAdvanced');

  const currentText = watch('text') || '';
  const errorInfo = getErrorMessage(error);
  const charCount = currentText.length;
  const maxChars = 500;

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="w-full max-w-3xl mx-auto">
      <div className="space-y-4">
        {/* API Error Message */}
        {error && (
          <div 
            className="bg-red-50 border-2 border-red-200 rounded-lg p-4"
            role="alert"
          >
            <div className="flex items-start gap-3">
              <svg
                className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z"
                  clipRule="evenodd"
                />
              </svg>
              <div className="flex-1">
                <h4 className="text-sm font-bold text-red-800 mb-1">{errorInfo.title}</h4>
                <p className="text-sm text-red-700">{errorInfo.message}</p>
                {errorInfo.canRetry && onRetry && (
                  <button
                    onClick={onRetry}
                    type="button"
                    className="mt-3 inline-flex items-center gap-2 px-4 py-2 bg-red-100 hover:bg-red-200 text-red-800 text-sm font-medium rounded-md transition-colors"
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
                    <span>إعادة المحاولة</span>
                  </button>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Verse Input Textarea */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <label htmlFor="verse" className="block text-lg font-medium text-gray-700">
              أدخل بيت الشعر
            </label>
            <span className={`text-sm ${charCount > maxChars ? 'text-red-600 font-bold' : 'text-gray-500'}`}>
              {charCount} / {maxChars}
            </span>
          </div>
          <textarea
            id="verse"
            {...register('text')}
            disabled={isLoading}
            rows={4}
            dir="rtl"
            className={`
              w-full px-4 py-3 rounded-lg border-2 
              font-[family-name:var(--font-amiri)] text-lg
              transition-all duration-200
              ${errors.text 
                ? 'border-red-400 focus:border-red-500 focus:ring-red-200' 
                : isLoading
                ? 'border-gray-300'
                : 'border-gray-300 focus:border-blue-500 focus:ring-blue-200'
              }
              focus:outline-none focus:ring-2
              disabled:bg-gray-100 disabled:cursor-not-allowed disabled:text-gray-500
              placeholder:text-gray-400
              resize-none
            `}
            placeholder="إذا غامَرتَ في شَرَفٍ مَرومِ *** فَلا تَقنَع بِما دونَ النُجومِ"
            aria-describedby={errors.text ? "verse-error" : "verse-help"}
          />
          {errors.text && (
            <p id="verse-error" className="mt-2 text-sm text-red-600 flex items-center gap-1" role="alert">
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              {errors.text.message}
            </p>
          )}
          {!errors.text && !isLoading && (
            <p id="verse-help" className="mt-2 text-sm text-gray-500">
              💡 يمكنك إدخال بيت أو أبيات من الشعر العربي الكلاسيكي
            </p>
          )}
        </div>

        {/* Advanced Options (V2 NEW) */}
        <div className="border-t border-gray-200 pt-4">
          <button
            type="button"
            onClick={() => setValue('showAdvanced', !showAdvanced)}
            className="flex items-center gap-2 text-sm font-medium text-gray-600 hover:text-gray-800 transition-colors"
          >
            <svg
              className={`w-4 h-4 transition-transform ${showAdvanced ? 'rotate-90' : ''}`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
            <span>خيارات متقدمة (دقة 100%)</span>
            <span className="text-xs px-2 py-0.5 bg-green-100 text-green-800 rounded-full">جديد</span>
          </button>

          {showAdvanced && (
            <div className="mt-4 space-y-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
              <div className="flex items-start gap-2 text-xs text-gray-600 mb-3">
                <svg className="w-4 h-4 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                </svg>
                <p>
                  للحصول على دقة 100%، يمكنك إدخال النمط الصوتي المحسوب مسبقاً أو البحر المتوقع.
                  هذه الميزات موجهة للمستخدمين المتقدمين والباحثين.
                </p>
              </div>

              {/* Pre-computed Pattern */}
              <div>
                <label htmlFor="precomputed_pattern" className="block text-sm font-medium text-gray-700 mb-1">
                  النمط الصوتي المحسوب مسبقاً (اختياري)
                </label>
                <input
                  id="precomputed_pattern"
                  type="text"
                  {...register('precomputed_pattern')}
                  disabled={isLoading}
                  dir="ltr"
                  className="w-full px-3 py-2 rounded border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 focus:outline-none font-mono text-sm disabled:bg-gray-100"
                  placeholder="/o////o/o/o/o//o//o/o/o"
                />
                <p className="mt-1 text-xs text-gray-500">
                  صيغة: / = حركة (متحرك) | o = سكون (ساكن). مثال: <code className="bg-gray-100 px-1 rounded">/o////o/</code>
                </p>
              </div>

              {/* Expected Meter */}
              <div>
                <label htmlFor="expected_meter" className="block text-sm font-medium text-gray-700 mb-1">
                  البحر المتوقع (اختياري)
                </label>
                <select
                  id="expected_meter"
                  {...register('expected_meter')}
                  disabled={isLoading}
                  className="w-full px-3 py-2 rounded border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 focus:outline-none disabled:bg-gray-100"
                  dir="rtl"
                >
                  <option value="">-- اختر البحر --</option>
                  <option value="الطويل">الطويل</option>
                  <option value="البسيط">البسيط</option>
                  <option value="الوافر">الوافر</option>
                  <option value="الكامل">الكامل</option>
                  <option value="المتقارب">المتقارب</option>
                  <option value="الرمل">الرمل</option>
                  <option value="الخفيف">الخفيف</option>
                  <option value="الرجز">الرجز</option>
                  <option value="السريع">السريع</option>
                  <option value="المديد">المديد</option>
                  <option value="الهزج">الهزج</option>
                  <option value="المنسرح">المنسرح</option>
                  <option value="المجتث">المجتث</option>
                  <option value="المتدارك">المتدارك</option>
                  <option value="المضارع">المضارع</option>
                  <option value="المقتضب">المقتضب</option>
                </select>
                <p className="mt-1 text-xs text-gray-500">
                  تحديد البحر المتوقع يساعد في حل الحالات الغامضة بدقة أعلى
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Submit Button */}
        <div>
          <button
            type="submit"
            disabled={isLoading}
            className={`
              w-full px-6 py-3 rounded-lg font-bold text-lg
              transition-all duration-200
              ${isLoading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700 active:bg-blue-800'
              }
              text-white shadow-lg hover:shadow-xl
              disabled:shadow-none
              flex items-center justify-center gap-2
            `}
          >
            {isLoading ? (
              <>
                <LoadingSpinner size="sm" className="text-white" />
                <span>جارٍ التحليل...</span>
              </>
            ) : (
              'حلّل'
            )}
          </button>
        </div>
      </div>
    </form>
  );
}
