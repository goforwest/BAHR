"use client";

import { useEffect } from "react";
import { useAnalytics } from "@/hooks/useAnalytics";

export default function Home() {
  const { trackPageView } = useAnalytics();

  // Track page view on mount
  useEffect(() => {
    trackPageView("/");
  }, [trackPageView]);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-br from-slate-50 to-blue-50 p-8">
      <main className="flex w-full max-w-4xl flex-col items-center gap-12 rounded-2xl border border-slate-200 bg-white p-12 shadow-xl">
        {/* Header */}
        <div className="flex flex-col items-center gap-4 text-center">
          <h1 className="text-6xl font-bold text-slate-900">بحر</h1>
          <p className="text-xl text-slate-600">
            BAHR - نظام ذكي لتحليل الشعر العربي
          </p>
        </div>

        {/* Sample Poetry Card */}
        <div className="w-full rounded-xl border border-slate-200 bg-slate-50 p-8">
          <div className="font-serif text-2xl leading-loose text-slate-800">
            <p className="mb-4">أَلا يا اِسلَمي يا دارَ مَيٍّ عَلى البِلى</p>
            <p className="mb-4">وَلا زالَ مُنهَلاً بِجَرعائِكِ القَطرُ</p>
            <p>فَيا دارَ مَيٍّ بِالعَلياءِ فَالسَّندِ</p>
          </div>
          <div className="mt-6 border-t border-slate-300 pt-4 text-sm text-slate-500">
            <p>— لبيد بن ربيعة</p>
          </div>
        </div>

        {/* Feature Grid */}
        <div className="grid w-full gap-6 sm:grid-cols-3">
          <div className="rounded-lg border border-slate-200 bg-white p-6 text-center transition-shadow hover:shadow-md">
            <div className="mb-3 text-4xl">🎼</div>
            <h3 className="mb-2 font-bold text-slate-900">كشف البحور</h3>
            <p className="text-sm text-slate-600">تحديد الأوزان العروضية</p>
          </div>

          <div className="rounded-lg border border-slate-200 bg-white p-6 text-center transition-shadow hover:shadow-md">
            <div className="mb-3 text-4xl">✨</div>
            <h3 className="mb-2 font-bold text-slate-900">تحليل القوافي</h3>
            <p className="text-sm text-slate-600">استخراج نمط القافية</p>
          </div>

          <div className="rounded-lg border border-slate-200 bg-white p-6 text-center transition-shadow hover:shadow-md">
            <div className="mb-3 text-4xl">📊</div>
            <h3 className="mb-2 font-bold text-slate-900">التقطيع العروضي</h3>
            <p className="text-sm text-slate-600">تفعيلات دقيقة للأبيات</p>
          </div>
        </div>

        {/* Status Badge */}
        <div className="flex items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50 px-4 py-2 text-sm font-medium text-emerald-700">
          <span className="h-2 w-2 animate-pulse rounded-full bg-emerald-500"></span>
          RTL + Arabic Fonts Initialized ✓
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-8 text-center text-sm text-slate-500">
        <p>بُني بواسطة Next.js 16 + Tailwind CSS v4 + shadcn/ui</p>
      </footer>
    </div>
  );
}
