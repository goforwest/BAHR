/**
 * Form component for Arabic verse analysis input.
 * Features RTL layout, Arabic validation, and loading states.
 */

'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

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
}

export function AnalyzeForm({ onSubmit, isLoading = false }: AnalyzeFormProps) {
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
                <svg
                  className="animate-spin h-5 w-5 text-white"
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
                  />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  />
                </svg>
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
