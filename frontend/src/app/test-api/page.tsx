/**
 * Test page for API client
 * Simple page to verify the analyze API endpoint works correctly
 */

'use client';

import { useState } from 'react';
import { useAnalyze } from '@/hooks/useAnalyze';

export default function TestPage() {
  const [verse, setVerse] = useState('إذا غامَرتَ في شَرَفٍ مَرومِ');
  const { mutate, data, isPending, error } = useAnalyze();

  const handleTest = () => {
    mutate({
      text: verse,
      detect_bahr: true,
      suggest_corrections: false,
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white p-8" dir="rtl">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-center mb-8 font-cairo">
          اختبار API Client
        </h1>

        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <label className="block mb-2 font-cairo font-semibold">
            أدخل بيت شعر للتحليل:
          </label>
          <textarea
            value={verse}
            onChange={(e) => setVerse(e.target.value)}
            className="w-full p-4 border rounded-lg font-amiri text-lg mb-4"
            rows={3}
            placeholder="إذا غامَرتَ في شَرَفٍ مَرومِ"
          />
          
          <button
            onClick={handleTest}
            disabled={isPending}
            className="bg-blue-600 text-white px-8 py-3 rounded-lg font-cairo font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {isPending ? 'جارٍ التحليل...' : 'تحليل'}
          </button>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-6 mb-6">
            <h2 className="text-xl font-bold text-red-800 mb-2 font-cairo">
              ❌ خطأ
            </h2>
            <p className="text-red-700 font-cairo">
              {error.message}
            </p>
          </div>
        )}

        {/* Results Display */}
        {data && (
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-bold mb-4 font-cairo text-green-800">
              ✅ النتيجة
            </h2>
            
            <div className="space-y-4">
              <div>
                <h3 className="font-cairo font-semibold text-gray-700 mb-2">النص:</h3>
                <p className="font-amiri text-lg">{data.text}</p>
              </div>

              <div>
                <h3 className="font-cairo font-semibold text-gray-700 mb-2">التقطيع:</h3>
                <p className="font-mono text-lg bg-gray-50 p-3 rounded">{data.taqti3}</p>
              </div>

              {data.bahr && (
                <div>
                  <h3 className="font-cairo font-semibold text-gray-700 mb-2">البحر:</h3>
                  <div className="bg-blue-50 p-4 rounded">
                    <p className="font-cairo text-lg">
                      <span className="font-bold">{data.bahr.name_ar}</span>
                      {' '}
                      ({data.bahr.name_en})
                    </p>
                    <p className="text-gray-600 mt-1">
                      الثقة: {(data.bahr.confidence * 100).toFixed(1)}%
                    </p>
                  </div>
                </div>
              )}

              <div>
                <h3 className="font-cairo font-semibold text-gray-700 mb-2">الدرجة:</h3>
                <div className="flex items-center gap-4">
                  <div className="flex-1 bg-gray-200 rounded-full h-4">
                    <div
                      className="bg-green-600 h-4 rounded-full transition-all duration-500"
                      style={{ width: `${data.score}%` }}
                    />
                  </div>
                  <span className="font-bold text-lg">{data.score.toFixed(1)}</span>
                </div>
              </div>

              {data.errors.length > 0 && (
                <div>
                  <h3 className="font-cairo font-semibold text-red-700 mb-2">الأخطاء:</h3>
                  <ul className="list-disc list-inside font-cairo text-red-600">
                    {data.errors.map((err, i) => (
                      <li key={i}>{err}</li>
                    ))}
                  </ul>
                </div>
              )}

              {data.suggestions.length > 0 && (
                <div>
                  <h3 className="font-cairo font-semibold text-blue-700 mb-2">الاقتراحات:</h3>
                  <ul className="list-disc list-inside font-cairo text-blue-600">
                    {data.suggestions.map((sug, i) => (
                      <li key={i}>{sug}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            {/* Raw JSON Response */}
            <details className="mt-6">
              <summary className="cursor-pointer font-cairo font-semibold text-gray-700 hover:text-gray-900">
                عرض البيانات الخام (JSON)
              </summary>
              <pre className="mt-2 bg-gray-900 text-green-400 p-4 rounded overflow-x-auto text-sm">
                {JSON.stringify(data, null, 2)}
              </pre>
            </details>
          </div>
        )}
      </div>
    </div>
  );
}
