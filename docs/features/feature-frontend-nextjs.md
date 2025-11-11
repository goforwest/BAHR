# Feature: Frontend (Next.js 14 + RTL) - Implementation Guide

**Feature ID:** `feature-frontend-nextjs`  
**Status:** Production-Ready  
**Last Updated:** November 8, 2025  
**Estimated Implementation Time:** 20-24 hours

---

## 1. Objective & Description

### What
Implement Next.js 14 frontend application with App Router, RTL (Right-to-Left) support for Arabic, TypeScript, TanStack Query for API integration, and responsive UI components for verse analysis.

### Why
- **Modern Stack:** Next.js 14 with App Router and React Server Components
- **Arabic First:** Full RTL support with proper text direction
- **Type Safety:** TypeScript for maintainability
- **Performance:** Server-side rendering and caching
- **UX:** Real-time analysis with loading states and error handling

### Success Criteria
- ✅ Next.js 14 App Router setup with TypeScript
- ✅ RTL support with proper Arabic font rendering
- ✅ TanStack Query integration for API calls
- ✅ Verse input form with validation
- ✅ Analysis results display with meter visualization
- ✅ Authentication UI (login/register)
- ✅ Responsive design (mobile-first)
- ✅ Test coverage ≥70% for components

---

## 2. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                Frontend Architecture (Next.js 14)                    │
└─────────────────────────────────────────────────────────────────────┘

Browser
    │
    │  User navigates to /
    ▼
┌──────────────────────────────────────┐
│ Next.js App Router                   │
│ - app/layout.tsx (Root layout)       │
│ - app/page.tsx (Home page)           │
│ - app/analyze/page.tsx               │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ React Server Components              │
│ - Server-side rendering              │
│ - Static generation                  │
└──────────┬───────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│ Client Components                    │
│ - VerseInputForm                     │
│ - AnalysisResults                    │
│ - AuthForm                           │
└──────────┬───────────────────────────┘
           │
           │  TanStack Query
           ▼
┌──────────────────────────────────────┐
│ API Client Layer                     │
│ - /lib/api/client.ts                 │
│ - Fetch wrapper                      │
│ - Error handling                     │
└──────────┬───────────────────────────┘
           │
           │  HTTP POST /api/v1/analyses
           ▼
    Backend API (FastAPI)

Directory Structure:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
frontend/
├── app/
│   ├── layout.tsx            # Root layout with RTL
│   ├── page.tsx              # Home page
│   ├── analyze/
│   │   └── page.tsx          # Analysis page
│   └── auth/
│       ├── login/page.tsx
│       └── register/page.tsx
├── components/
│   ├── ui/
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   └── Card.tsx
│   ├── VerseInputForm.tsx
│   ├── AnalysisResults.tsx
│   └── MeterVisualization.tsx
├── lib/
│   ├── api/
│   │   ├── client.ts         # API client
│   │   └── types.ts          # TypeScript types
│   └── utils/
│       └── rtl.ts            # RTL helpers
├── hooks/
│   ├── useAnalysis.ts        # TanStack Query hook
│   └── useAuth.ts
├── styles/
│   └── globals.css
└── public/
    └── fonts/                # Arabic fonts
```

---

## 3. Input/Output Contracts

### 3.1 TypeScript API Types

```typescript
// frontend/lib/api/types.ts
/**
 * API type definitions matching backend schemas.
 * 
 * Source: docs/technical/API_SPECIFICATION.yaml:1-300
 */

export interface BilingualMessage {
  en: string;
  ar: string;
}

export interface ErrorDetail {
  field: string;
  issue: string;
  message?: string;
}

export interface ErrorResponse {
  code: string;
  message: BilingualMessage;
  details?: ErrorDetail[];
}

export interface ResponseMeta {
  request_id: string;
  timestamp: string;
  version: string;
  processing_time_ms?: number;
  cached?: boolean;
}

export interface ResponseEnvelope<T> {
  success: boolean;
  data: T | null;
  error: ErrorResponse | null;
  meta: ResponseMeta;
}

export interface AnalysisRequest {
  text: string;
  language?: string;
}

export interface AnalysisResult {
  id: string;
  text: string;
  normalized_text: string;
  pattern: string;
  detected_meter: string;
  confidence: number;
  syllable_count: number;
  processing_time_ms: number;
  created_at: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  full_name: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}
```

---

## 4. Step-by-Step Implementation

### Step 1: Initialize Next.js 14 Project

```bash
# Create Next.js project
npx create-next-app@14 frontend --typescript --tailwind --app --no-src-dir

cd frontend

# Install dependencies
npm install @tanstack/react-query axios
npm install -D @types/node

# Install Arabic font support
npm install next-font
```

### Step 2: Configure RTL Support

```tsx
// frontend/app/layout.tsx
/**
 * Root layout with RTL support.
 * 
 * Source: docs/technical/FRONTEND_GUIDE.md:1-80
 */

import type { Metadata } from 'next';
import { Tajawal } from 'next/font/google';
import './globals.css';

// Arabic font
const tajawal = Tajawal({
  subsets: ['arabic'],
  weight: ['300', '400', '500', '700'],
  variable: '--font-tajawal',
});

export const metadata: Metadata = {
  title: 'بحر - تحليل الشعر العربي',
  description: 'نظام تحليل البحور الشعرية العربية',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ar" dir="rtl">
      <body className={`${tajawal.variable} font-sans`}>
        {children}
      </body>
    </html>
  );
}
```

```css
/* frontend/styles/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  /* RTL support */
  [dir="rtl"] {
    text-align: right;
  }
  
  /* Arabic font optimization */
  body {
    font-family: var(--font-tajawal), -apple-system, sans-serif;
    direction: rtl;
  }
  
  /* Input RTL */
  input, textarea {
    direction: rtl;
    text-align: right;
  }
}
```

### Step 3: Create API Client

```typescript
// frontend/lib/api/client.ts
/**
 * API client with envelope handling.
 * 
 * Source: docs/technical/API_SPECIFICATION.yaml:45-120
 */

import axios, { AxiosError } from 'axios';
import type { ResponseEnvelope } from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
});

// Request interceptor (add auth token)
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor (unwrap envelope)
apiClient.interceptors.response.use(
  (response) => {
    const envelope = response.data as ResponseEnvelope<any>;
    
    if (envelope.success) {
      return { ...response, data: envelope.data };
    } else {
      // Convert envelope error to axios error
      throw new AxiosError(
        envelope.error?.message.ar || envelope.error?.message.en || 'خطأ',
        envelope.error?.code,
        response.config,
        response.request,
        response
      );
    }
  },
  (error: AxiosError) => {
    // Handle network errors
    if (!error.response) {
      throw new Error('فشل الاتصال بالخادم');
    }
    
    const envelope = error.response.data as ResponseEnvelope<any>;
    throw new AxiosError(
      envelope.error?.message.ar || 'حدث خطأ',
      envelope.error?.code,
      error.config,
      error.request,
      error.response
    );
  }
);

export default apiClient;
```

### Step 4: Create TanStack Query Hook

```typescript
// frontend/hooks/useAnalysis.ts
/**
 * TanStack Query hook for verse analysis.
 * 
 * Source: implementation-guides/feature-analysis-api.md:340-420
 */

import { useMutation, useQuery } from '@tanstack/react-query';
import apiClient from '@/lib/api/client';
import type { AnalysisRequest, AnalysisResult } from '@/lib/api/types';

export function useAnalysis() {
  return useMutation({
    mutationFn: async (request: AnalysisRequest): Promise<AnalysisResult> => {
      const response = await apiClient.post<AnalysisResult>(
        '/api/v1/analyses',
        request
      );
      return response.data;
    },
    onError: (error) => {
      console.error('Analysis failed:', error);
    },
  });
}

export function useAnalysisHistory() {
  return useQuery({
    queryKey: ['analyses'],
    queryFn: async (): Promise<AnalysisResult[]> => {
      const response = await apiClient.get<AnalysisResult[]>('/api/v1/analyses');
      return response.data;
    },
  });
}
```

### Step 5: Create Verse Input Form Component

```tsx
// frontend/components/VerseInputForm.tsx
/**
 * Verse input form with validation.
 * 
 * Source: docs/technical/FRONTEND_GUIDE.md:120-220
 */

'use client';

import { useState } from 'react';
import { useAnalysis } from '@/hooks/useAnalysis';
import type { AnalysisResult } from '@/lib/api/types';

interface VerseInputFormProps {
  onSuccess?: (result: AnalysisResult) => void;
}

export default function VerseInputForm({ onSuccess }: VerseInputFormProps) {
  const [text, setText] = useState('');
  const analysisMutation = useAnalysis();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!text.trim()) {
      alert('الرجاء إدخال نص');
      return;
    }

    try {
      const result = await analysisMutation.mutateAsync({ text });
      onSuccess?.(result);
      setText(''); // Clear form
    } catch (error) {
      // Error handled by mutation
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="verse-input" className="block text-lg font-semibold mb-2">
          أدخل البيت الشعري
        </label>
        <textarea
          id="verse-input"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="مثال: أَلا عِم صَباحاً أَيُّها الطَلَلُ البالي"
          className="w-full p-4 border-2 border-gray-300 rounded-lg 
                     focus:border-blue-500 focus:outline-none
                     text-right text-lg min-h-[120px]
                     disabled:bg-gray-100"
          disabled={analysisMutation.isPending}
          maxLength={1000}
        />
        <div className="text-sm text-gray-500 mt-1">
          {text.length}/1000 حرف
        </div>
      </div>

      {analysisMutation.error && (
        <div className="bg-red-50 border-r-4 border-red-500 p-4 rounded">
          <p className="text-red-700">
            {analysisMutation.error.message}
          </p>
        </div>
      )}

      <button
        type="submit"
        disabled={analysisMutation.isPending || !text.trim()}
        className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg
                   font-semibold text-lg hover:bg-blue-700
                   disabled:bg-gray-400 disabled:cursor-not-allowed
                   transition-colors"
      >
        {analysisMutation.isPending ? 'جاري التحليل...' : 'تحليل البيت'}
      </button>
    </form>
  );
}
```

### Step 6: Create Analysis Results Component

```tsx
// frontend/components/AnalysisResults.tsx
/**
 * Display analysis results with meter visualization.
 */

'use client';

import type { AnalysisResult } from '@/lib/api/types';

interface AnalysisResultsProps {
  result: AnalysisResult;
}

export default function AnalysisResults({ result }: AnalysisResultsProps) {
  const confidenceColor = 
    result.confidence >= 0.8 ? 'text-green-600' :
    result.confidence >= 0.6 ? 'text-yellow-600' :
    'text-red-600';

  return (
    <div className="bg-white shadow-lg rounded-lg p-6 space-y-4">
      <h2 className="text-2xl font-bold text-gray-800">نتيجة التحليل</h2>

      {/* Original Text */}
      <div>
        <h3 className="text-lg font-semibold text-gray-700 mb-2">النص الأصلي:</h3>
        <p className="text-xl text-gray-900 leading-relaxed p-4 bg-gray-50 rounded">
          {result.text}
        </p>
      </div>

      {/* Detected Meter */}
      <div className="border-t pt-4">
        <h3 className="text-lg font-semibold text-gray-700 mb-2">البحر الشعري:</h3>
        <p className="text-3xl font-bold text-blue-600">
          {result.detected_meter}
        </p>
      </div>

      {/* Confidence */}
      <div className="flex items-center gap-4">
        <span className="text-gray-700 font-semibold">مستوى الثقة:</span>
        <span className={`text-2xl font-bold ${confidenceColor}`}>
          {(result.confidence * 100).toFixed(1)}%
        </span>
        <div className="flex-1 bg-gray-200 rounded-full h-4 overflow-hidden">
          <div
            className={`h-full ${
              result.confidence >= 0.8 ? 'bg-green-600' :
              result.confidence >= 0.6 ? 'bg-yellow-600' :
              'bg-red-600'
            }`}
            style={{ width: `${result.confidence * 100}%` }}
          />
        </div>
      </div>

      {/* Prosodic Pattern */}
      <div className="border-t pt-4">
        <h3 className="text-lg font-semibold text-gray-700 mb-2">النمط العروضي:</h3>
        <p className="font-mono text-lg text-gray-800 bg-gray-50 p-4 rounded 
                      break-all leading-relaxed">
          {result.pattern}
        </p>
      </div>

      {/* Syllable Count */}
      <div className="flex gap-8 text-gray-700">
        <div>
          <span className="font-semibold">عدد المقاطع:</span>
          <span className="mr-2 text-lg font-bold text-blue-600">
            {result.syllable_count}
          </span>
        </div>
        <div>
          <span className="font-semibold">وقت المعالجة:</span>
          <span className="mr-2 text-lg font-bold text-blue-600">
            {result.processing_time_ms}ms
          </span>
        </div>
      </div>
    </div>
  );
}
```

### Step 7: Create Analysis Page

```tsx
// frontend/app/analyze/page.tsx
/**
 * Main analysis page.
 */

'use client';

import { useState } from 'react';
import VerseInputForm from '@/components/VerseInputForm';
import AnalysisResults from '@/components/AnalysisResults';
import type { AnalysisResult } from '@/lib/api/types';

export default function AnalyzePage() {
  const [result, setResult] = useState<AnalysisResult | null>(null);

  return (
    <main className="min-h-screen bg-gradient-to-b from-blue-50 to-white py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            بحر
          </h1>
          <p className="text-xl text-gray-600">
            نظام تحليل البحور الشعرية العربية
          </p>
        </header>

        <div className="bg-white shadow-xl rounded-lg p-8 mb-8">
          <VerseInputForm onSuccess={setResult} />
        </div>

        {result && <AnalysisResults result={result} />}
      </div>
    </main>
  );
}
```

### Step 8: Configure TanStack Query Provider

```tsx
// frontend/app/providers.tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState } from 'react';

export default function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000, // 1 minute
            retry: 1,
          },
        },
      })
  );

  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}
```

```tsx
// frontend/app/layout.tsx (updated)
import Providers from './providers';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ar" dir="rtl">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

---

## 5. Reference Implementation (Full Code)

See Step-by-Step Implementation sections above for complete code.

---

## 6. Unit & Integration Tests

```typescript
// frontend/__tests__/components/VerseInputForm.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import VerseInputForm from '@/components/VerseInputForm';

const queryClient = new QueryClient();

function Wrapper({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}

describe('VerseInputForm', () => {
  it('renders input field', () => {
    render(<VerseInputForm />, { wrapper: Wrapper });
    expect(screen.getByLabelText(/أدخل البيت الشعري/)).toBeInTheDocument();
  });

  it('validates empty input', async () => {
    render(<VerseInputForm />, { wrapper: Wrapper });
    
    const button = screen.getByRole('button', { name: /تحليل البيت/ });
    fireEvent.click(button);
    
    // Should show alert (or validation message)
    await waitFor(() => {
      expect(button).not.toBeDisabled();
    });
  });
});
```

---

## 7. CI/CD Pipeline

```yaml
# .github/workflows/frontend-tests.yml
name: Frontend Tests

on:
  push:
    paths:
      - 'frontend/**'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      
      - name: Run tests
        run: |
          cd frontend
          npm test
      
      - name: Build
        run: |
          cd frontend
          npm run build
```

---

## 8. Deployment Checklist

- [ ] Configure NEXT_PUBLIC_API_URL environment variable
- [ ] Deploy to Vercel
- [ ] Test RTL rendering
- [ ] Verify Arabic font loading
- [ ] Test API integration
- [ ] Configure caching headers
- [ ] Test responsive design (mobile/tablet/desktop)
- [ ] Add analytics
- [ ] Test authentication flow
- [ ] Configure CSP headers

---

## 9. Observability

- Vercel Analytics for page views
- Error tracking with Sentry
- Web Vitals monitoring
- API response time tracking

---

## 10. Security & Safety

- **API URL Validation:** Ensure HTTPS in production
- **Token Storage:** Use httpOnly cookies (not localStorage)
- **XSS Protection:** Sanitize user input
- **CSRF Protection:** Add CSRF tokens

---

## 11. Backwards Compatibility

- **None** - Initial implementation

---

## 12. Source Documentation Citations

1. **docs/technical/FRONTEND_GUIDE.md:1-300** - Frontend architecture
2. **docs/technical/API_SPECIFICATION.yaml:1-500** - API contracts
3. **implementation-guides/IMPROVED_PROMPT.md:740-762** - Feature specification

---

**Implementation Complete!** ✅  
**Estimated Time:** 20-24 hours  
**Test Coverage Target:** ≥ 70%  
**Framework:** Next.js 14 + TypeScript + TanStack Query
