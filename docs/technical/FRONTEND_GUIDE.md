# 🖥️ دليل معمارية Frontend
## Next.js + React + TypeScript

---

## 📋 نظرة عامة

هذا الدليل يوضح كامل معمارية Frontend لمشروع بَحْر، مع التركيز على:
- **تجربة المستخدم المحسّنة** للنصوص العربية
- **أداء عالي** وتحميل سريع
- **تصميم متجاوب** يدعم جميع الأحجام
- **إمكانية الوصول** (Accessibility) 
- **قابلية التوسع** والصيانة

---

## 🏗️ معمارية النظام (System Architecture)

```
Frontend Architecture:
┌─────────────────────────────────────────┐
│            User Interface               │
│  ┌─────────────┐ ┌─────────────┐       │
│  │   Pages     │ │ Components  │       │
│  └─────────────┘ └─────────────┘       │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│         Application Layer               │
│  ┌─────────────┐ ┌─────────────┐       │
│  │    Hooks    │ │    Store    │       │
│  └─────────────┘ └─────────────┘       │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│           Service Layer                 │
│  ┌─────────────┐ ┌─────────────┐       │
│  │  API Client │ │   Utils     │       │
│  └─────────────┘ └─────────────┘       │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│          External APIs                  │
│     (Backend + Third-party)             │
└─────────────────────────────────────────┘
```

---

## 🗂️ هيكل المجلدات المفصل

```
frontend/
├── public/
│   ├── images/
│   │   ├── logo/
│   │   │   ├── logo-light.svg
│   │   │   ├── logo-dark.svg
│   │   │   └── favicon.ico
│   │   ├── illustrations/
│   │   │   ├── hero-poetry.svg
│   │   │   ├── analysis-visualization.svg
│   │   │   └── meter-patterns.svg
│   │   └── examples/
│   │       └── sample-verses.jpg
│   ├── fonts/
│   │   ├── Amiri/         # خط عربي كلاسيكي
│   │   ├── Cairo/         # خط عربي حديث
│   │   └── NotoSansArabic/ # خط احتياطي
│   └── manifest.json      # PWA manifest
│
├── src/
│   ├── app/               # App Router (Next.js 13+)
│   │   ├── layout.tsx     # Root layout
│   │   ├── loading.tsx    # Global loading UI
│   │   ├── error.tsx      # Global error boundary
│   │   ├── not-found.tsx  # 404 page
│   │   ├── page.tsx       # Home page
│   │   │
│   │   ├── analyze/       # Analysis section
│   │   │   ├── page.tsx
│   │   │   ├── layout.tsx
│   │   │   └── loading.tsx
│   │   │
│   │   ├── examples/      # Examples showcase
│   │   │   ├── page.tsx
│   │   │   └── [category]/
│   │   │       └── page.tsx
│   │   │
│   │   ├── about/         # About pages
│   │   │   ├── page.tsx
│   │   │   ├── prosody/
│   │   │   │   └── page.tsx
│   │   │   └── project/
│   │   │       └── page.tsx
│   │   │
│   │   └── api/           # API routes (if needed)
│   │       └── health/
│   │           └── route.ts
│   │
│   ├── components/        # Reusable components
│   │   ├── ui/            # Basic UI components
│   │   │   ├── button.tsx
│   │   │   ├── input.tsx
│   │   │   ├── card.tsx
│   │   │   ├── badge.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── loading.tsx
│   │   │   ├── error-boundary.tsx
│   │   │   └── index.ts   # Export all
│   │   │
│   │   ├── layout/        # Layout components
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   ├── Navigation.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── ThemeProvider.tsx
│   │   │
│   │   ├── analyzer/      # Analysis components
│   │   │   ├── TextInput.tsx
│   │   │   ├── AnalysisSettings.tsx
│   │   │   ├── AnalyzeButton.tsx
│   │   │   ├── ResultsDisplay.tsx
│   │   │   ├── ProsodyVisualization.tsx
│   │   │   ├── MeterInfo.tsx
│   │   │   ├── QualityScore.tsx
│   │   │   └── index.ts
│   │   │
│   │   ├── examples/      # Examples components
│   │   │   ├── PresetVerses.tsx
│   │   │   ├── QuickDemo.tsx
│   │   │   ├── CategoryFilter.tsx
│   │   │   └── VerseCard.tsx
│   │   │
│   │   ├── forms/         # Form components
│   │   │   ├── ContactForm.tsx
│   │   │   ├── FeedbackForm.tsx
│   │   │   └── SubscribeForm.tsx
│   │   │
│   │   └── shared/        # Shared components
│   │       ├── ArabicText.tsx
│   │       ├── LanguageToggle.tsx
│   │       ├── ShareButton.tsx
│   │       ├── CopyToClipboard.tsx
│   │       └── BackToTop.tsx
│   │
│   ├── hooks/             # Custom React hooks
│   │   ├── useAnalyze.ts
│   │   ├── useMeters.ts
│   │   ├── useExamples.ts
│   │   ├── useLocalStorage.ts
│   │   ├── useDebounce.ts
│   │   ├── useKeyboard.ts
│   │   └── index.ts
│   │
│   ├── store/             # State management
│   │   ├── index.ts       # Store configuration
│   │   ├── slices/
│   │   │   ├── analysisSlice.ts
│   │   │   ├── uiSlice.ts
│   │   │   ├── settingsSlice.ts
│   │   │   └── examplesSlice.ts
│   │   └── providers/
│   │       └── StoreProvider.tsx
│   │
│   ├── lib/               # Utilities & services
│   │   ├── api/
│   │   │   ├── client.ts    # API client setup
│   │   │   ├── endpoints.ts # API endpoints
│   │   │   ├── types.ts     # API types
│   │   │   └── queries.ts   # React Query hooks
│   │   │
│   │   ├── utils/
│   │   │   ├── arabic.ts    # Arabic text utilities
│   │   │   ├── validation.ts # Form validation
│   │   │   ├── formatting.ts # Text formatting
│   │   │   ├── constants.ts  # App constants
│   │   │   └── helpers.ts    # Helper functions
│   │   │
│   │   ├── config/
│   │   │   ├── env.ts       # Environment variables
│   │   │   ├── routes.ts    # App routes
│   │   │   └── features.ts  # Feature flags
│   │   │
│   │   └── types/
│   │       ├── api.ts       # API response types
│   │       ├── common.ts    # Common types
│   │       └── prosody.ts   # Prosody-specific types
│   │
│   └── styles/            # Styling
│       ├── globals.css    # Global styles
│       ├── components.css # Component styles
│       ├── arabic.css     # Arabic typography
│       ├── themes.css     # Theme variables
│       └── animations.css # Custom animations
│
├── __tests__/             # Test files
│   ├── components/
│   ├── hooks/
│   ├── utils/
│   └── pages/
│
├── docs/                  # Component documentation
│   └── storybook/
│
├── package.json
├── next.config.js
├── tailwind.config.js
├── tsconfig.json
├── eslint.config.js
├── jest.config.js
├── Dockerfile
└── README.md
```

---

## 🎨 نظام التصميم (Design System)

### Colors & Typography:

```typescript
// styles/theme.ts
export const theme = {
  colors: {
    // Primary colors (inspired by Arabic calligraphy)
    primary: {
      50: '#f0f9ff',
      100: '#e0f2fe', 
      500: '#0ea5e9',  // Main blue
      600: '#0284c7',
      900: '#0c4a6e'
    },
    
    // Arabic gold accent
    accent: {
      100: '#fef3c7',
      500: '#f59e0b',   // Arabic gold
      600: '#d97706'
    },
    
    // Semantic colors
    success: '#10b981',
    warning: '#f59e0b', 
    error: '#ef4444',
    info: '#3b82f6'
  },
  
  typography: {
    fonts: {
      arabic: ['Amiri', 'Cairo', 'Noto Sans Arabic', 'sans-serif'],
      english: ['Inter', 'system-ui', 'sans-serif'],
      mono: ['Fira Code', 'monospace']
    },
    
    sizes: {
      xs: '0.75rem',    // 12px
      sm: '0.875rem',   // 14px  
      base: '1rem',     // 16px
      lg: '1.125rem',   // 18px
      xl: '1.25rem',    // 20px
      '2xl': '1.5rem',  // 24px
      '3xl': '1.875rem' // 30px
    }
  },
  
  spacing: {
    xs: '0.5rem',   // 8px
    sm: '0.75rem',  // 12px
    md: '1rem',     // 16px
    lg: '1.5rem',   // 24px
    xl: '2rem',     // 32px
    '2xl': '3rem'   // 48px
  }
} as const;
```

### Component Variants:

```typescript
// components/ui/button.tsx
import { cva, type VariantProps } from 'class-variance-authority'

const buttonVariants = cva(
  // Base styles
  'inline-flex items-center justify-center rounded-lg text-sm font-medium transition-colors focus-visible:outline-none disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-primary-500 text-white hover:bg-primary-600',
        secondary: 'bg-gray-100 text-gray-900 hover:bg-gray-200',
        outline: 'border border-gray-300 bg-white hover:bg-gray-50',
        ghost: 'hover:bg-gray-100',
        accent: 'bg-accent-500 text-white hover:bg-accent-600'
      },
      size: {
        sm: 'h-9 px-3',
        md: 'h-10 px-4 py-2', 
        lg: 'h-11 px-8',
        icon: 'h-10 w-10'
      },
      direction: {
        ltr: 'flex-row',
        rtl: 'flex-row-reverse'
      }
    },
    defaultVariants: {
      variant: 'default',
      size: 'md',
      direction: 'ltr'
    }
  }
)

interface ButtonProps 
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
          VariantProps<typeof buttonVariants> {
  isLoading?: boolean
  leftIcon?: React.ReactNode
  rightIcon?: React.ReactNode
}

export function Button({
  className,
  variant,
  size,
  direction,
  isLoading,
  leftIcon,
  rightIcon,
  children,
  disabled,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(buttonVariants({ variant, size, direction, className }))}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading && <Spinner className="w-4 h-4 mr-2" />}
      {leftIcon && <span className="mr-2">{leftIcon}</span>}
      {children}
      {rightIcon && <span className="ml-2">{rightIcon}</span>}
    </button>
  )
}
```

---

## 🔌 إدارة الحالة (State Management)

### Zustand Store Setup:

```typescript
// store/index.ts
import { create } from 'zustand'
import { devtools } from 'zustand/middleware'
import { analysisSlice } from './slices/analysisSlice'
import { uiSlice } from './slices/uiSlice'
import { settingsSlice } from './slices/settingsSlice'

export interface RootState {
  analysis: ReturnType<typeof analysisSlice>
  ui: ReturnType<typeof uiSlice>
  settings: ReturnType<typeof settingsSlice>
}

export const useStore = create<RootState>()(
  devtools(
    (set, get) => ({
      analysis: analysisSlice(set, get),
      ui: uiSlice(set, get),
      settings: settingsSlice(set, get)
    }),
    {
      name: 'bahr-store'
    }
  )
)
```

### Analysis Slice:

```typescript
// store/slices/analysisSlice.ts
import { StateCreator } from 'zustand'
import { AnalysisResult, AnalysisRequest } from '@/lib/types/api'

export interface AnalysisState {
  // Current analysis
  currentText: string
  currentResult: AnalysisResult | null
  isAnalyzing: boolean
  error: string | null
  
  // Analysis history
  history: AnalysisResult[]
  favorites: AnalysisResult[]
  
  // Settings
  settings: {
    removeDiacritics: boolean
    analysisMode: 'accurate' | 'fast'
    showAlternatives: boolean
  }
  
  // Actions
  setText: (text: string) => void
  analyze: (request: AnalysisRequest) => Promise<void>
  clearResult: () => void
  addToFavorites: (result: AnalysisResult) => void
  removeFromFavorites: (id: string) => void
  updateSettings: (settings: Partial<AnalysisState['settings']>) => void
}

export const analysisSlice: StateCreator<AnalysisState> = (set, get) => ({
  // Initial state
  currentText: '',
  currentResult: null,
  isAnalyzing: false,
  error: null,
  history: [],
  favorites: [],
  settings: {
    removeDiacritics: true,
    analysisMode: 'accurate',
    showAlternatives: true
  },
  
  // Actions
  setText: (text: string) => {
    set({ currentText: text, error: null })
  },
  
  analyze: async (request: AnalysisRequest) => {
    set({ isAnalyzing: true, error: null })
    
    try {
      const result = await analyzeText(request)
      
      set(state => ({
        currentResult: result,
        isAnalyzing: false,
        history: [result, ...state.history].slice(0, 50) // Keep last 50
      }))
    } catch (error) {
      set({ 
        error: error.message || 'حدث خطأ في التحليل',
        isAnalyzing: false 
      })
    }
  },
  
  clearResult: () => {
    set({ 
      currentResult: null, 
      currentText: '', 
      error: null 
    })
  },
  
  addToFavorites: (result: AnalysisResult) => {
    set(state => ({
      favorites: [...state.favorites, { ...result, id: Date.now() }]
    }))
  },
  
  removeFromFavorites: (id: string) => {
    set(state => ({
      favorites: state.favorites.filter(fav => fav.id !== id)
    }))
  },
  
  updateSettings: (newSettings) => {
    set(state => ({
      settings: { ...state.settings, ...newSettings }
    }))
  }
})
```

---

## 🎣 Custom Hooks

### useAnalyze Hook:

```typescript
// hooks/useAnalyze.ts
import { useStore } from '@/store'
import { useCallback } from 'react'
import { AnalysisRequest } from '@/lib/types/api'

export function useAnalyze() {
  const {
    currentText,
    currentResult,
    isAnalyzing,
    error,
    settings,
    setText,
    analyze,
    clearResult,
    addToFavorites
  } = useStore(state => state.analysis)
  
  const analyzeText = useCallback(async (text?: string) => {
    const textToAnalyze = text || currentText
    
    if (!textToAnalyze.trim()) {
      return
    }
    
    const request: AnalysisRequest = {
      text: textToAnalyze,
      options: {
        remove_diacritics: settings.removeDiacritics,
        analysis_mode: settings.analysisMode,
        return_alternatives: settings.showAlternatives
      }
    }
    
    await analyze(request)
  }, [currentText, settings, analyze])
  
  const analyzeExample = useCallback(async (exampleText: string) => {
    setText(exampleText)
    await analyzeText(exampleText)
  }, [setText, analyzeText])
  
  return {
    // State
    text: currentText,
    result: currentResult,
    isLoading: isAnalyzing,
    error,
    
    // Actions
    setText,
    analyzeText,
    analyzeExample,
    clearResult,
    addToFavorites,
    
    // Computed
    hasResult: !!currentResult,
    canAnalyze: currentText.trim().length > 0 && !isAnalyzing
  }
}
```

### useArabicText Hook:

```typescript
// hooks/useArabicText.ts
import { useState, useCallback } from 'react'
import { isArabicText, normalizeArabicText } from '@/lib/utils/arabic'

export function useArabicText(initialText = '') {
  const [text, setText] = useState(initialText)
  const [isRTL, setIsRTL] = useState(() => isArabicText(initialText))
  
  const handleTextChange = useCallback((newText: string) => {
    setText(newText)
    setIsRTL(isArabicText(newText))
  }, [])
  
  const normalize = useCallback(() => {
    const normalized = normalizeArabicText(text)
    setText(normalized)
    return normalized
  }, [text])
  
  const clear = useCallback(() => {
    setText('')
    setIsRTL(false)
  }, [])
  
  return {
    text,
    isRTL,
    isEmpty: text.trim().length === 0,
    wordCount: text.trim().split(/\s+/).filter(Boolean).length,
    
    // Actions
    setText: handleTextChange,
    normalize,
    clear
  }
}
```

---

## 🧩 Core Components

### Arabic Text Input:

```typescript
// components/analyzer/TextInput.tsx
'use client'

import { forwardRef } from 'react'
import { useArabicText } from '@/hooks/useArabicText'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'

interface TextInputProps {
  value?: string
  onChange?: (text: string) => void
  onAnalyze?: () => void
  placeholder?: string
  disabled?: boolean
  isLoading?: boolean
}

export const TextInput = forwardRef<HTMLTextAreaElement, TextInputProps>(({
  value = '',
  onChange,
  onAnalyze,
  placeholder = 'اكتب بيت الشعر هنا...',
  disabled = false,
  isLoading = false,
}, ref) => {
  const { text, isRTL, wordCount, setText, clear } = useArabicText(value)
  
  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newText = e.target.value
    setText(newText)
    onChange?.(newText)
  }
  
  const handleKeyDown = (e: React.KeyboardEvent) => {
    // Ctrl/Cmd + Enter to analyze
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault()
      onAnalyze?.()
    }
  }
  
  return (
    <Card className="p-6">
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold">نص الشعر</h3>
          <div className="text-sm text-gray-500">
            {wordCount} كلمة
          </div>
        </div>
        
        <Textarea
          ref={ref}
          value={text}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={disabled}
          dir={isRTL ? 'rtl' : 'ltr'}
          className={`
            min-h-[120px] text-lg leading-relaxed
            ${isRTL ? 'text-right font-arabic' : 'text-left'}
            focus:ring-2 focus:ring-primary-500
            resize-none
          `}
        />
        
        <div className="flex items-center justify-between">
          <Button
            variant="outline"
            size="sm"
            onClick={clear}
            disabled={disabled || !text.trim()}
          >
            مسح النص
          </Button>
          
          <Button
            onClick={onAnalyze}
            disabled={disabled || !text.trim() || isLoading}
            isLoading={isLoading}
            className="min-w-[120px]"
          >
            {isLoading ? 'جاري التحليل...' : 'تحليل البيت'}
          </Button>
        </div>
      </div>
    </Card>
  )
})

TextInput.displayName = 'TextInput'
```

### Prosody Visualization:

```typescript
// components/analyzer/ProsodyVisualization.tsx
'use client'

import { motion } from 'framer-motion'
import { Card } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { AnalysisResult } from '@/lib/types/api'

interface ProsodyVisualizationProps {
  result: AnalysisResult
  className?: string
}

export function ProsodyVisualization({ result, className }: ProsodyVisualizationProps) {
  const { prosodic_analysis, meter_detection } = result
  
  // Convert pattern to visual elements
  const patternElements = prosodic_analysis.pattern.split(' ').map((element, index) => {
    const isLong = element === '-'
    const isShort = element === 'u'
    
    return {
      id: index,
      type: isLong ? 'long' : isShort ? 'short' : 'separator',
      symbol: element,
      duration: isLong ? 'طويل' : isShort ? 'قصير' : ''
    }
  })
  
  return (
    <Card className={`p-6 ${className}`}>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <h3 className="text-xl font-bold">التحليل العروضي</h3>
          <Badge variant="accent" className="text-lg px-3 py-1">
            {meter_detection.detected_meter}
          </Badge>
        </div>
        
        {/* Original text */}
        <div className="space-y-2">
          <p className="text-sm font-medium text-gray-600">النص الأصلي:</p>
          <p className="text-lg leading-relaxed font-arabic text-right bg-gray-50 p-4 rounded-lg">
            {result.input_text}
          </p>
        </div>
        
        {/* Taqti3 pattern */}
        <div className="space-y-2">
          <p className="text-sm font-medium text-gray-600">التقطيع:</p>
          <p className="text-lg leading-relaxed font-arabic text-right bg-blue-50 p-4 rounded-lg">
            {prosodic_analysis.taqti3}
          </p>
        </div>
        
        {/* Visual pattern */}
        <div className="space-y-2">
          <p className="text-sm font-medium text-gray-600">النمط الإيقاعي:</p>
          <div className="flex items-center justify-center space-x-1 bg-gray-50 p-4 rounded-lg">
            {patternElements.map((element, index) => (
              <motion.div
                key={element.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="flex flex-col items-center"
              >
                {element.type !== 'separator' && (
                  <>
                    <div
                      className={`
                        rounded-full border-2 mb-1
                        ${element.type === 'long' 
                          ? 'w-8 h-8 bg-blue-500 border-blue-600' 
                          : 'w-4 h-4 bg-red-400 border-red-500'}
                      `}
                    />
                    <span className="text-xs text-gray-500">
                      {element.symbol}
                    </span>
                  </>
                )}
                {element.type === 'separator' && (
                  <div className="w-2 h-8 flex items-center">
                    <div className="w-px h-6 bg-gray-300" />
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </div>
        
        {/* Confidence and quality */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-1">
            <p className="text-sm font-medium text-gray-600">الثقة في التحليل:</p>
            <div className="flex items-center space-x-2">
              <div className="flex-1 bg-gray-200 rounded-full h-3">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${meter_detection.confidence * 100}%` }}
                  transition={{ duration: 1, ease: 'easeOut' }}
                  className="bg-green-500 h-3 rounded-full"
                />
              </div>
              <span className="text-sm font-mono">
                {(meter_detection.confidence * 100).toFixed(1)}%
              </span>
            </div>
          </div>
          
          <div className="space-y-1">
            <p className="text-sm font-medium text-gray-600">تقييم الجودة:</p>
            <div className="flex items-center space-x-2">
              <div className="flex-1 bg-gray-200 rounded-full h-3">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${result.quality_score * 100}%` }}
                  transition={{ duration: 1, ease: 'easeOut', delay: 0.2 }}
                  className="bg-blue-500 h-3 rounded-full"
                />
              </div>
              <span className="text-sm font-mono">
                {(result.quality_score * 100).toFixed(1)}%
              </span>
            </div>
          </div>
        </div>
        
        {/* Suggestions */}
        {result.suggestions && result.suggestions.length > 0 && (
          <div className="space-y-2">
            <p className="text-sm font-medium text-gray-600">ملاحظات:</p>
            <ul className="space-y-1">
              {result.suggestions.map((suggestion, index) => (
                <li key={index} className="text-sm text-gray-700 flex items-start">
                  <span className="text-blue-500 mr-2">•</span>
                  {suggestion}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </Card>
  )
}
```

---

## 📱 Responsive Design

### Breakpoints Configuration:

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    screens: {
      'xs': '475px',
      'sm': '640px',
      'md': '768px',
      'lg': '1024px',
      'xl': '1280px',
      '2xl': '1536px'
    },
    
    extend: {
      fontFamily: {
        'arabic': ['Amiri', 'Cairo', 'Noto Sans Arabic', 'sans-serif'],
        'sans': ['Inter', 'system-ui', 'sans-serif']
      }
    }
  },
  
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
  ]
}
```

### Mobile-First Components:

```typescript
// components/layout/Navigation.tsx
'use client'

import { useState } from 'react'
import { Menu, X } from 'lucide-react'
import { Button } from '@/components/ui/button'

export function Navigation() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  
  const navItems = [
    { href: '/', label: 'الرئيسية' },
    { href: '/analyze', label: 'تحليل الشعر' },
    { href: '/examples', label: 'أمثلة' },
    { href: '/about', label: 'حول المشروع' }
  ]
  
  return (
    <nav className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex-shrink-0">
            <h1 className="text-2xl font-bold text-primary-600 font-arabic">
              بَحْر
            </h1>
          </div>
          
          {/* Desktop Navigation */}
          <div className="hidden md:block">
            <div className="flex items-center space-x-8 space-x-reverse">
              {navItems.map((item) => (
                <a
                  key={item.href}
                  href={item.href}
                  className="text-gray-700 hover:text-primary-600 px-3 py-2 text-sm font-medium transition-colors"
                >
                  {item.label}
                </a>
              ))}
            </div>
          </div>
          
          {/* Mobile menu button */}
          <div className="md:hidden">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            >
              {isMobileMenuOpen ? (
                <X className="h-6 w-6" />
              ) : (
                <Menu className="h-6 w-6" />
              )}
            </Button>
          </div>
        </div>
        
        {/* Mobile Navigation */}
        {isMobileMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 bg-gray-50">
              {navItems.map((item) => (
                <a
                  key={item.href}
                  href={item.href}
                  className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-primary-600 hover:bg-gray-100 rounded-md"
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  {item.label}
                </a>
              ))}
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}
```

---

## ♿ إمكانية الوصول (Accessibility)

### ARIA Implementation:

```typescript
// components/ui/input.tsx
import { forwardRef } from 'react'
import { cn } from '@/lib/utils'

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  helperText?: string
}

export const Input = forwardRef<HTMLInputElement, InputProps>(({
  className,
  type = 'text',
  label,
  error,
  helperText,
  id,
  ...props
}, ref) => {
  const inputId = id || `input-${Math.random().toString(36).substr(2, 9)}`
  const errorId = error ? `${inputId}-error` : undefined
  const helperId = helperText ? `${inputId}-helper` : undefined
  
  return (
    <div className="space-y-2">
      {label && (
        <label
          htmlFor={inputId}
          className="block text-sm font-medium text-gray-700"
        >
          {label}
        </label>
      )}
      
      <input
        ref={ref}
        id={inputId}
        type={type}
        className={cn(
          'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm',
          'focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
          'disabled:cursor-not-allowed disabled:bg-gray-50',
          error && 'border-red-300 focus:ring-red-500 focus:border-red-500',
          className
        )}
        aria-invalid={error ? 'true' : 'false'}
        aria-describedby={cn(errorId, helperId).trim() || undefined}
        {...props}
      />
      
      {error && (
        <p id={errorId} className="text-sm text-red-600" role="alert">
          {error}
        </p>
      )}
      
      {helperText && !error && (
        <p id={helperId} className="text-sm text-gray-500">
          {helperText}
        </p>
      )}
    </div>
  )
})

Input.displayName = 'Input'
```

### Keyboard Navigation:

```typescript
// hooks/useKeyboard.ts
import { useEffect, useCallback } from 'react'

interface KeyboardShortcuts {
  [key: string]: () => void
}

export function useKeyboard(shortcuts: KeyboardShortcuts, deps: any[] = []) {
  const handleKeyDown = useCallback((event: KeyboardEvent) => {
    const { key, ctrlKey, metaKey, shiftKey, altKey } = event
    
    // Build shortcut key
    let shortcut = ''
    if (ctrlKey || metaKey) shortcut += 'ctrl+'
    if (shiftKey) shortcut += 'shift+'
    if (altKey) shortcut += 'alt+'
    shortcut += key.toLowerCase()
    
    if (shortcuts[shortcut]) {
      event.preventDefault()
      shortcuts[shortcut]()
    }
  }, [shortcuts])
  
  useEffect(() => {
    document.addEventListener('keydown', handleKeyDown)
    return () => document.removeEventListener('keydown', handleKeyDown)
  }, [handleKeyDown])
}

// Usage in components
export function AnalyzerPage() {
  const { analyzeText, clearResult } = useAnalyze()
  
  useKeyboard({
    'ctrl+enter': analyzeText,
    'ctrl+shift+c': clearResult,
    'escape': clearResult
  })
  
  return (
    // Component JSX...
  )
}
```

---

## 🚀 Performance Optimization

### Code Splitting:

```typescript
// app/analyze/page.tsx
import dynamic from 'next/dynamic'
import { Suspense } from 'react'
import { LoadingSpinner } from '@/components/ui/loading'

// Lazy load heavy components
const ProsodyVisualization = dynamic(
  () => import('@/components/analyzer/ProsodyVisualization'),
  {
    loading: () => <LoadingSpinner />,
    ssr: false // Disable SSR for client-only components
  }
)

const AdvancedSettings = dynamic(
  () => import('@/components/analyzer/AdvancedSettings'),
  {
    loading: () => <div>جاري التحميل...</div>
  }
)

export default function AnalyzePage() {
  return (
    <div className="space-y-6">
      <TextInput />
      
      <Suspense fallback={<LoadingSpinner />}>
        <ProsodyVisualization />
      </Suspense>
      
      <Suspense fallback={<div>جاري تحميل الإعدادات...</div>}>
        <AdvancedSettings />
      </Suspense>
    </div>
  )
}
```

### Image Optimization:

```typescript
// components/shared/OptimizedImage.tsx
import Image from 'next/image'
import { useState } from 'react'

interface OptimizedImageProps {
  src: string
  alt: string
  width: number
  height: number
  className?: string
  priority?: boolean
}

export function OptimizedImage({ 
  src, 
  alt, 
  width, 
  height, 
  className,
  priority = false 
}: OptimizedImageProps) {
  const [isLoading, setIsLoading] = useState(true)
  
  return (
    <div className={`relative overflow-hidden ${className}`}>
      <Image
        src={src}
        alt={alt}
        width={width}
        height={height}
        priority={priority}
        onLoadingComplete={() => setIsLoading(false)}
        className={`
          transition-opacity duration-300
          ${isLoading ? 'opacity-0' : 'opacity-100'}
        `}
        sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
      />
      
      {isLoading && (
        <div className="absolute inset-0 bg-gray-200 animate-pulse" />
      )}
    </div>
  )
}
```

---

## 🧪 Testing Strategy

### Component Testing:

```typescript
// __tests__/components/TextInput.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { TextInput } from '@/components/analyzer/TextInput'

describe('TextInput Component', () => {
  const mockOnAnalyze = jest.fn()
  const mockOnChange = jest.fn()
  
  beforeEach(() => {
    jest.clearAllMocks()
  })
  
  it('renders with Arabic placeholder', () => {
    render(<TextInput onAnalyze={mockOnAnalyze} />)
    
    const textarea = screen.getByPlaceholderText('اكتب بيت الشعر هنا...')
    expect(textarea).toBeInTheDocument()
    expect(textarea).toHaveAttribute('dir', 'rtl')
  })
  
  it('calls onAnalyze when analyze button is clicked', async () => {
    const user = userEvent.setup()
    
    render(
      <TextInput 
        onAnalyze={mockOnAnalyze} 
        onChange={mockOnChange}
      />
    )
    
    const textarea = screen.getByRole('textbox')
    const analyzeButton = screen.getByText('تحليل البيت')
    
    // Type Arabic text
    await user.type(textarea, 'قفا نبك من ذكرى حبيب ومنزل')
    await user.click(analyzeButton)
    
    expect(mockOnAnalyze).toHaveBeenCalledTimes(1)
  })
  
  it('triggers analysis with Ctrl+Enter', async () => {
    const user = userEvent.setup()
    
    render(<TextInput onAnalyze={mockOnAnalyze} />)
    
    const textarea = screen.getByRole('textbox')
    
    await user.type(textarea, 'قفا نبك من ذكرى حبيب ومنزل')
    await user.keyboard('{Control>}{Enter}{/Control}')
    
    expect(mockOnAnalyze).toHaveBeenCalledTimes(1)
  })
  
  it('disables button when loading', () => {
    render(
      <TextInput 
        onAnalyze={mockOnAnalyze}
        isLoading={true}
        value="test text"
      />
    )
    
    const analyzeButton = screen.getByRole('button', { name: /جاري التحليل/ })
    expect(analyzeButton).toBeDisabled()
  })
})
```

### Integration Testing:

```typescript
// __tests__/pages/analyze.test.tsx
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { rest } from 'msw'
import { setupServer } from 'msw/node'
import AnalyzePage from '@/app/analyze/page'

// Mock API server
const server = setupServer(
  rest.post('/api/v1/analyze', (req, res, ctx) => {
    return res(
      ctx.json({
        success: true,
        data: {
          input_text: 'قفا نبك من ذكرى حبيب ومنزل',
          prosodic_analysis: {
            taqti3: 'فَعُولُنْ مَفَاعِيلُنْ فَعُولُنْ مَفَاعِلُنْ',
            pattern: '- u - | - u u - | - u - | - u u -'
          },
          meter_detection: {
            detected_meter: 'الطويل',
            confidence: 0.95
          },
          quality_score: 0.92
        }
      })
    )
  })
)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

describe('Analyze Page', () => {
  it('performs full analysis workflow', async () => {
    const user = userEvent.setup()
    
    render(<AnalyzePage />)
    
    // Find input and enter text
    const textarea = screen.getByPlaceholderText('اكتب بيت الشعر هنا...')
    await user.type(textarea, 'قفا نبك من ذكرى حبيب ومنزل')
    
    // Click analyze
    const analyzeButton = screen.getByText('تحليل البيت')
    await user.click(analyzeButton)
    
    // Wait for results
    await waitFor(() => {
      expect(screen.getByText('الطويل')).toBeInTheDocument()
    })
    
    // Check if analysis results are displayed
    expect(screen.getByText('فَعُولُنْ مَفَاعِيلُنْ فَعُولُنْ مَفَاعِلُنْ')).toBeInTheDocument()
    expect(screen.getByText('95.0%')).toBeInTheDocument()
  })
})
```

---

## 🎯 Next Steps

بعد إكمال Frontend Architecture، التالي:

1. **[Backend API Documentation](BACKEND_API.md)**
2. **[Database Design Document](DATABASE_SCHEMA.md)**  
3. **[Development Workflow Guide](DEVELOPMENT_WORKFLOW.md)**

---

## 📝 ملاحظات التطوير

### أولويات التطوير:
1. **أساسيات UI:** Button, Input, Card, Loading
2. **تحليل الشعر:** TextInput, ResultsDisplay, Visualization  
3. **التنقل:** Header, Footer, Navigation
4. **إعدادات:** AnalysisSettings, ThemeProvider
5. **تحسينات:** Accessibility, Performance, Testing

### أمور يجب مراعاتها:
- **RTL Support:** كل component يجب يدعم الكتابة من اليمين لليسار
- **Arabic Typography:** استخدام خطوط عربية مناسبة
- **Mobile First:** التصميم للهواتف أولاً
- **Performance:** Code splitting والتحميل التدريجي
- **Accessibility:** دعم screen readers وnavigation بالكيبورد

---

**🎨 هذا يكمل دليل معمارية Frontend - الواجهة التي ستسحر المستخدمين!**