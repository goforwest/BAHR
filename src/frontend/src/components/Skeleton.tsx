/**
 * Skeleton loader component for loading states.
 * Provides smooth placeholder animations while content is loading.
 */

"use client";

import { cn } from "@/lib/utils";

interface SkeletonProps {
  className?: string;
}

export function Skeleton({ className }: SkeletonProps) {
  return (
    <div className={cn("animate-pulse rounded-md bg-gray-200/60", className)} />
  );
}

/**
 * Loading skeleton for verse analysis results
 */
export function AnalysisLoadingSkeleton() {
  return (
    <div
      className="w-full max-w-3xl mx-auto mt-8 space-y-6"
      role="status"
      aria-label="جارٍ تحليل البيت الشعري"
    >
      {/* Verse Text Skeleton */}
      <div className="bg-white shadow-lg rounded-lg p-6">
        <Skeleton className="h-4 w-24 mb-3" />
        <Skeleton className="h-8 w-full mb-2" />
        <Skeleton className="h-8 w-5/6" />
      </div>

      {/* Taqti3 Skeleton */}
      <div className="bg-white shadow-lg rounded-lg p-6">
        <Skeleton className="h-4 w-32 mb-3" />
        <div className="bg-blue-50 p-4 rounded-md">
          <Skeleton className="h-6 w-full mb-2" />
          <Skeleton className="h-6 w-4/5" />
        </div>
      </div>

      {/* Bahr Skeleton */}
      <div className="bg-white shadow-lg rounded-lg p-6">
        <Skeleton className="h-4 w-28 mb-3" />
        <div className="space-y-3">
          <div className="flex items-baseline justify-between">
            <Skeleton className="h-7 w-32" />
            <Skeleton className="h-5 w-20" />
          </div>
          <div>
            <div className="flex items-center justify-between mb-2">
              <Skeleton className="h-4 w-16" />
              <Skeleton className="h-4 w-12" />
            </div>
            <Skeleton className="h-2.5 w-full rounded-full" />
          </div>
        </div>
      </div>

      {/* Score Skeleton */}
      <div className="bg-white shadow-lg rounded-lg p-6">
        <Skeleton className="h-4 w-20 mb-3" />
        <div>
          <div className="flex items-center justify-between mb-2">
            <Skeleton className="h-8 w-16" />
            <Skeleton className="h-4 w-16" />
          </div>
          <Skeleton className="h-4 w-full rounded-full" />
          <Skeleton className="h-4 w-48 mt-2" />
        </div>
      </div>

      <span className="sr-only">جارٍ تحليل البيت الشعري، يرجى الانتظار...</span>
    </div>
  );
}

/**
 * Inline loading skeleton for small components
 */
export function InlineSkeleton({ lines = 1 }: { lines?: number }) {
  return (
    <div className="space-y-2">
      {Array.from({ length: lines }).map((_, i) => (
        <Skeleton key={i} className="h-4 w-full" />
      ))}
    </div>
  );
}
