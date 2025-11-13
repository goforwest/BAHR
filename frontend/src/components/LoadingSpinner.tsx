/**
 * Reusable loading spinner component with size variants.
 * Uses Tailwind CSS for styling and smooth animations.
 */

"use client";

import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const spinnerVariants = cva(
  "inline-block animate-spin rounded-full border-solid border-current border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]",
  {
    variants: {
      size: {
        sm: "h-4 w-4 border-2",
        md: "h-8 w-8 border-3",
        lg: "h-12 w-12 border-4",
      },
    },
    defaultVariants: {
      size: "md",
    },
  },
);

export interface LoadingSpinnerProps
  extends VariantProps<typeof spinnerVariants> {
  className?: string;
  label?: string;
}

/**
 * LoadingSpinner component
 *
 * @param size - Size variant: 'sm' | 'md' | 'lg'
 * @param className - Additional CSS classes
 * @param label - Optional accessible label for screen readers
 *
 * @example
 * ```tsx
 * <LoadingSpinner size="sm" />
 * <LoadingSpinner size="md" label="جارٍ التحميل..." />
 * <LoadingSpinner size="lg" className="text-blue-600" />
 * ```
 */
export function LoadingSpinner({
  size,
  className,
  label = "جارٍ التحميل...",
}: LoadingSpinnerProps) {
  return (
    <div
      role="status"
      aria-label={label}
      className="inline-flex items-center justify-center"
    >
      <div className={cn(spinnerVariants({ size }), className)} />
      <span className="sr-only">{label}</span>
    </div>
  );
}
