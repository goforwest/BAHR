/**
 * Form component for Arabic verse analysis input.
 * Features RTL layout, Arabic validation, and loading states.
 */

'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { LoadingSpinner } from './LoadingSpinner';

// Validation schema with Zod
const analyzeSchema = z.object({
  text: z
    .string()
    .min(5, 'يجب أن يحتوي النص على 5 أحرف على الأقل')
    .max(500, 'يجب أن لا يتجاوز النص 500 حرف')
    .regex(/[\u0600-\u06FF]/, 'يجب أن يحتوي النص على أحرف عربية'),
});

type AnalyzeFormData = z.infer<typeof analyzeSchema>;

interface AnalyzeFormProps {
  onSubmit: (text: string) => void;
  isLoading?: boolean;
  error?: Error | null;
}

/**
 * Get user-friendly error message in Arabic
 */
function getErrorMessage(error: Error | null): string {
  if (!error) return '';
  
  const message = error.message.toLowerCase();
  
  // Network errors
  if (message.includes('network') || message.includes('fetch')) {
    return 'خطأ في الاتصال، يرجى المحاولة مرة أخرى';
  }
  
  // Server errors
  if (message.includes('500') || message.includes('server')) {
    return 'حدث خطأ في الخادم، يرجى المحاولة لاحقاً';
  }
  
  // Validation errors
  if (message.includes('invalid') || message.includes('validation')) {
    return 'يرجى إدخال بيت شعري صحيح';
  }
  
  // Default error message
  return error.message || 'حدث خطأ غير متوقع';
}

export function AnalyzeForm({ onSubmit, isLoading = false, error = null }: AnalyzeFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<AnalyzeFormData>({
    resolver: zodResolver(analyzeSchema),
  });

  const handleFormSubmit = (data: AnalyzeFormData) => {
    onSubmit(data.text);
  };

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="w-full max-w-3xl mx-auto">
      <div className="space-y-4">
        {/* API Error Message */}
        {error && (
          <div 
            className="bg-red-50 border-2 border-red-200 rounded-lg p-4 flex items-start gap-3"
            role="alert"
          >
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
            <p className="text-sm text-red-800 font-medium">{getErrorMessage(error)}</p>
          </div>
        )}

        {/* Verse Input Textarea */}
        <div>
          <label htmlFor="verse" className="block text-lg font-medium text-gray-700 mb-2">
            أدخل بيت الشعر
          </label>
          <textarea
            id="verse"
            {...register('text')}
            disabled={isLoading}
            rows={4}
            dir="rtl"
            className={`
              w-full px-4 py-3 rounded-lg border-2 
              font-[family-name:var(--font-amiri)] text-lg
              transition-colors duration-200
              ${errors.text 
                ? 'border-red-400 focus:border-red-500 focus:ring-red-200' 
                : 'border-gray-300 focus:border-blue-500 focus:ring-blue-200'
              }
              focus:outline-none focus:ring-2
              disabled:bg-gray-100 disabled:cursor-not-allowed
              placeholder:text-gray-400
            `}
            placeholder="إذا غامَرتَ في شَرَفٍ مَرومِ"
          />
          {errors.text && (
            <p className="mt-2 text-sm text-red-600" role="alert">
              {errors.text.message}
            </p>
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
