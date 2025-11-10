# 🛡️ استراتيجية معالجة الأخطاء الشاملة
## Error Handling, Graceful Degradation & User Communication

---

## 📋 نظرة عامة

دليل شامل لمعالجة الأخطاء بطريقة احترافية مع رسائل واضحة بالعربية والإنجليزية.

**تم الإنشاء:** November 8, 2025  
**الأهمية:** حرجة - تؤثر على تجربة المستخدم

---

## 🎯 مبادئ معالجة الأخطاء

### المبادئ الأساسية:

```yaml
1. User-Friendly:
   - رسائل واضحة بالعربية
   - تجنب المصطلحات التقنية
   - اقتراح حلول ممكنة

2. Informative:
   - توضيح سبب الخطأ
   - خطوات لتصحيح المشكلة
   - متى يمكن المحاولة مرة أخرى

3. Actionable:
   - زر "حاول مرة أخرى"
   - رابط للمساعدة
   - خيار الإبلاغ عن مشكلة

4. Logged:
   - كل خطأ يُسجل مع السياق
   - معرف فريد لكل خطأ
   - تتبع الأخطاء المتكررة

5. Monitored:
   - تنبيهات للأخطاء الحرجة
   - لوحة معلومات للأخطاء
   - تحليل أنماط الأخطاء
```

---

## 📝 رسائل الأخطاء بالعربية

### قاموس الرسائل:

```python
# app/core/errors/messages.py
"""
رسائل الأخطاء باللغتين العربية والإنجليزية
"""

ERROR_MESSAGES = {
    # Analysis Errors
    'analysis_failed': {
        'ar': 'عذراً، فشل تحليل النص. الرجاء المحاولة مرة أخرى',
        'en': 'Sorry, text analysis failed. Please try again',
        'code': 'ERR_ANALYSIS_001',
        'severity': 'error',
        'retry': True
    },
    
    'invalid_arabic': {
        'ar': 'النص المُدخل لا يحتوي على أحرف عربية كافية للتحليل',
        'en': 'Input text does not contain sufficient Arabic characters',
        'code': 'ERR_INPUT_001',
        'severity': 'warning',
        'retry': False,
        'suggestion_ar': 'تأكد من إدخال نص عربي صحيح',
        'suggestion_en': 'Please ensure you enter valid Arabic text'
    },
    
    'meter_uncertain': {
        'ar': 'لم نستطع تحديد البحر الشعري بثقة كافية',
        'en': 'Unable to determine poetic meter with sufficient confidence',
        'code': 'ERR_METER_001',
        'severity': 'info',
        'retry': False,
        'suggestion_ar': 'قد يكون النص شعراً حراً، أو يحتوي على اختلافات عن البحور الكلاسيكية',
        'suggestion_en': 'This may be free verse or contain variations from classical meters'
    },
    
    'text_too_short': {
        'ar': 'النص قصير جداً. يُفضل إدخال بيت كامل على الأقل',
        'en': 'Text is too short. Please enter at least one complete verse',
        'code': 'ERR_INPUT_002',
        'severity': 'warning',
        'retry': False,
        'min_length': 10
    },
    
    'text_too_long': {
        'ar': 'النص طويل جداً. الحد الأقصى {max_length} كلمة',
        'en': 'Text is too long. Maximum {max_length} words allowed',
        'code': 'ERR_INPUT_003',
        'severity': 'warning',
        'retry': False,
        'max_length': 1000
    },
    
    'timeout': {
        'ar': 'انتهت مهلة التحليل. الرجاء تجربة نص أقصر أو المحاولة لاحقاً',
        'en': 'Analysis timed out. Please try shorter text or try again later',
        'code': 'ERR_TIMEOUT_001',
        'severity': 'error',
        'retry': True,
        'retry_delay': 5
    },
    
    # Database Errors
    'database_error': {
        'ar': 'خطأ في قاعدة البيانات. فريقنا يعمل على إصلاحه',
        'en': 'Database error occurred. Our team is working on it',
        'code': 'ERR_DB_001',
        'severity': 'critical',
        'retry': True,
        'retry_delay': 10
    },
    
    'connection_error': {
        'ar': 'فشل الاتصال بالخادم. تحقق من اتصال الإنترنت',
        'en': 'Failed to connect to server. Check your internet connection',
        'code': 'ERR_NETWORK_001',
        'severity': 'error',
        'retry': True
    },
    
    # Authentication Errors
    'auth_required': {
        'ar': 'يجب تسجيل الدخول للوصول إلى هذه الميزة',
        'en': 'Authentication required to access this feature',
        'code': 'ERR_AUTH_001',
        'severity': 'warning',
        'retry': False,
        'action': 'redirect_login'
    },
    
    'invalid_token': {
        'ar': 'انتهت صلاحية الجلسة. الرجاء تسجيل الدخول مرة أخرى',
        'en': 'Session expired. Please login again',
        'code': 'ERR_AUTH_002',
        'severity': 'warning',
        'retry': False,
        'action': 'redirect_login'
    },
    
    # Rate Limiting
    'rate_limit_exceeded': {
        'ar': 'لقد تجاوزت الحد المسموح من الطلبات. الرجاء الانتظار {wait_time} ثانية',
        'en': 'Rate limit exceeded. Please wait {wait_time} seconds',
        'code': 'ERR_RATE_001',
        'severity': 'warning',
        'retry': True,
        'wait_time': 60
    },
    
    # NLP Library Errors
    'nlp_library_error': {
        'ar': 'خطأ في مكتبة معالجة اللغة. سنحاول طريقة بديلة',
        'en': 'NLP library error. Trying alternative method',
        'code': 'ERR_NLP_001',
        'severity': 'warning',
        'retry': True,
        'fallback': True
    },
    'model_unavailable': {
        'ar': 'خدمة النموذج غير متاحة حالياً. سنستخدم وضعاً مبسطاً مؤقتاً',
        'en': 'Model service is currently unavailable. Falling back to simplified mode',
        'code': 'ERR_MODEL_001',
        'severity': 'warning',
        'retry': True,
        'fallback': True
    },
    
    # Validation Errors
    'invalid_format': {
        'ar': 'تنسيق النص غير صحيح',
        'en': 'Invalid text format',
        'code': 'ERR_VALIDATION_001',
        'severity': 'warning',
        'retry': False
    },
    
    'forbidden_content': {
        'ar': 'المحتوى المُدخل يحتوي على نصوص ممنوعة',
        'en': 'Input contains forbidden content',
        'code': 'ERR_VALIDATION_002',
        'severity': 'error',
        'retry': False
    },
    
    # Generic Errors
    'unknown_error': {
        'ar': 'حدث خطأ غير متوقع. الرجاء المحاولة مرة أخرى',
        'en': 'An unexpected error occurred. Please try again',
        'code': 'ERR_UNKNOWN_001',
        'severity': 'error',
        'retry': True
    },
    
    'maintenance_mode': {
        'ar': 'المنصة قيد الصيانة حالياً. نعتذر عن الإزعاج',
        'en': 'Platform is currently under maintenance. Sorry for the inconvenience',
        'code': 'ERR_MAINTENANCE_001',
        'severity': 'info',
        'retry': True,
        'retry_delay': 300
    }
}


def get_error_message(error_key: str, language: str = 'ar', **kwargs) -> dict:
    """
    الحصول على رسالة خطأ بتنسيق موحد
    
    Args:
        error_key: مفتاح الخطأ من ERROR_MESSAGES
        language: اللغة ('ar' أو 'en')
        **kwargs: متغيرات إضافية للرسالة
    
    Returns:
        dict: رسالة الخطأ مع التفاصيل
    """
    if error_key not in ERROR_MESSAGES:
        error_key = 'unknown_error'
    
    error = ERROR_MESSAGES[error_key].copy()
    message = error[language]
    
    # استبدال المتغيرات في الرسالة
    if kwargs:
        message = message.format(**kwargs)
    
    return {
        'message': message,
        'code': error['code'],
        'severity': error['severity'],
        'can_retry': error.get('retry', False),
        'retry_delay': error.get('retry_delay', 0),
        'suggestion': error.get(f'suggestion_{language}', ''),
        'action': error.get('action', None)
    }
```

---

## 🔄 Graceful Degradation Strategy

### مستويات التدهور التدريجي:

```python
# app/core/prosody/resilient_analyzer.py
"""
محلل مرن مع استراتيجيات احتياطية
"""

from enum import Enum
from typing import Optional, Dict, Any

class AnalysisMode(Enum):
    FULL = "full"           # تحليل كامل مع NLP
    FALLBACK = "fallback"   # تحليل بديل بدون NLP
    BASIC = "basic"         # تحليل أساسي فقط
    CACHED = "cached"       # من الذاكرة المؤقتة فقط

class ResilientAnalyzer:
    """محلل يتدهور تدريجياً عند حدوث أخطاء"""
    
    def __init__(self):
        self.primary_analyzer = None
        self.fallback_analyzer = None
        self.cache = None
        
        self._init_analyzers()
    
    def _init_analyzers(self):
        """تهيئة المحللات مع معالجة الأخطاء"""
        try:
            from app.core.prosody.camel_analyzer import CAMeLAnalyzer
            self.primary_analyzer = CAMeLAnalyzer()
        except Exception as e:
            logger.error(f"Failed to initialize CAMeL analyzer: {e}")
        
        try:
            from app.core.prosody.rule_analyzer import RuleBasedAnalyzer
            self.fallback_analyzer = RuleBasedAnalyzer()
        except Exception as e:
            logger.error(f"Failed to initialize fallback analyzer: {e}")
    
    def analyze(self, text: str, mode: AnalysisMode = AnalysisMode.FULL) -> Dict[str, Any]:
        """
        تحليل النص مع التدهور التدريجي
        
        المراحل:
        1. محاولة التحليل الكامل مع NLP
        2. إذا فشل، استخدام محلل قائم على القواعد
        3. إذا فشل، تحليل أساسي جداً
        4. إذا فشل كل شيء، إرجاع رسالة خطأ واضحة
        """
        
        # المحاولة 1: تحليل كامل
        if mode == AnalysisMode.FULL and self.primary_analyzer:
            try:
                result = self.primary_analyzer.analyze(text)
                result['analysis_mode'] = 'full'
                return result
            except Exception as e:
                logger.warning(f"Primary analyzer failed: {e}, falling back")
                result_hint = get_error_message('model_unavailable')
        
        # المحاولة 2: محلل احتياطي
        if mode in [AnalysisMode.FULL, AnalysisMode.FALLBACK] and self.fallback_analyzer:
            try:
                result = self.fallback_analyzer.analyze(text)
                result['analysis_mode'] = 'fallback'
                result['warning'] = result_hint if 'result_hint' in locals() else get_error_message('nlp_library_error')
                return result
            except Exception as e:
                logger.warning(f"Fallback analyzer failed: {e}, using basic mode")
        
        # المحاولة 3: تحليل أساسي جداً
        if mode in [AnalysisMode.FULL, AnalysisMode.FALLBACK, AnalysisMode.BASIC]:
            try:
                result = self._basic_analysis(text)
                result['analysis_mode'] = 'basic'
                result['warning'] = get_error_message('nlp_library_error')
                return result
            except Exception as e:
                logger.error(f"Even basic analysis failed: {e}")
        
        # كل شيء فشل
        raise AnalysisException(
            error_key='analysis_failed',
            details={'text_length': len(text), 'mode': mode.value}
        )
    
    def _basic_analysis(self, text: str) -> Dict[str, Any]:
        """تحليل أساسي جداً كملاذ أخير"""
        words = text.split()
        
        return {
            'input_text': text,
            'word_count': len(words),
            'char_count': len(text),
            'contains_arabic': any('\u0600' <= c <= '\u06FF' for c in text),
            'detected_meter': None,
            'confidence': 0.0,
            'message_ar': 'تحليل أساسي فقط متاح حالياً',
            'message_en': 'Only basic analysis available currently'
        }


class AnalysisException(Exception):
    """استثناء مخصص لأخطاء التحليل"""
    
    def __init__(self, error_key: str, details: Optional[Dict] = None):
        self.error_key = error_key
        self.details = details or {}
        self.message_data = get_error_message(error_key)
        super().__init__(self.message_data['message'])
```

---

## 🔁 Retry Logic

### استراتيجية إعادة المحاولة:

```python
# app/core/utils/retry.py
"""
منطق إعادة المحاولة مع Exponential Backoff
"""

import time
import functools
from typing import Callable, Type, Tuple
import logging

logger = logging.getLogger(__name__)


def retry_with_backoff(
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Optional[Callable] = None
):
    """
    Decorator لإعادة المحاولة مع تأخير تصاعدي
    
    Args:
        max_attempts: أقصى عدد محاولات
        initial_delay: التأخير الأولي (ثواني)
        backoff_factor: معامل التأخير التصاعدي
        exceptions: الأخطاء التي تستوجب إعادة المحاولة
        on_retry: دالة تُنفذ عند كل محاولة إعادة
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == max_attempts:
                        logger.error(
                            f"Function {func.__name__} failed after {max_attempts} attempts: {e}"
                        )
                        raise
                    
                    logger.warning(
                        f"Function {func.__name__} attempt {attempt}/{max_attempts} failed: {e}. "
                        f"Retrying in {delay}s..."
                    )
                    
                    if on_retry:
                        on_retry(attempt, e)
                    
                    time.sleep(delay)
                    delay *= backoff_factor
            
            raise last_exception
        
        return wrapper
    return decorator


# مثال استخدام
@retry_with_backoff(
    max_attempts=3,
    initial_delay=1.0,
    exceptions=(ConnectionError, TimeoutError)
)
def fetch_analysis_from_cache(text_hash: str):
    """جلب تحليل من الذاكرة المؤقتة مع إعادة محاولة"""
    return redis_client.get(f"analysis:{text_hash}")
```

---

## 📊 Error Logging & Tracking

### هيكل سجل الأخطاء:

```python
# app/core/logging/error_logger.py
"""
تسجيل الأخطاء بشكل منظم
"""

import logging
import json
import traceback
from datetime import datetime
from typing import Optional, Dict, Any
import uuid

class StructuredErrorLogger:
    """مسجل أخطاء منظم مع سياق كامل"""
    
    def __init__(self):
        self.logger = logging.getLogger('bahr.errors')
    
    def log_error(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        user_id: Optional[int] = None,
        request_id: Optional[str] = None
    ) -> str:
        """
        تسجيل خطأ مع كامل السياق
        
        Returns:
            error_id: معرف فريد للخطأ
        """
        error_id = str(uuid.uuid4())
        
        error_data = {
            'error_id': error_id,
            'timestamp': datetime.utcnow().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': traceback.format_exc(),
            'context': context or {},
            'user_id': user_id,
            'request_id': request_id
        }
        
        # تسجيل كـ JSON للبحث السهل
        self.logger.error(json.dumps(error_data, ensure_ascii=False, indent=2))
        
        # إرسال للمراقبة (Sentry, etc.)
        if self._should_alert(error):
            self._send_alert(error_data)
        
        return error_id
    
    def _should_alert(self, error: Exception) -> bool:
        """تحديد إذا كان يجب إرسال تنبيه"""
        critical_errors = (
            DatabaseError,
            MemoryError,
            SystemError
        )
        return isinstance(error, critical_errors)
    
    def _send_alert(self, error_data: Dict):
        """إرسال تنبيه للفريق"""
        # Integration with Sentry, Slack, Email, etc.
        pass


# استخدام في API endpoint
from fastapi import HTTPException

@app.post("/api/v1/analyze")
async def analyze_text(request: AnalyzeRequest):
    error_logger = StructuredErrorLogger()
    
    try:
        result = analyzer.analyze(request.text)
        return {"success": True, "data": result}
    
    except AnalysisException as e:
        error_id = error_logger.log_error(
            error=e,
            context={'text_length': len(request.text)},
            request_id=request.headers.get('X-Request-ID')
        )
        
        return JSONResponse(
            status_code=422,
            content={
                'success': False,
                'error': e.message_data,
                'error_id': error_id
            }
        )
    
    except Exception as e:
        error_id = error_logger.log_error(
            error=e,
            context={'endpoint': '/api/v1/analyze'}
        )
        
        return JSONResponse(
            status_code=500,
            content={
                'success': False,
                'error': get_error_message('unknown_error'),
                'error_id': error_id
            }
        )
```

---

## 🎨 Frontend Error Handling

### مكون عرض الأخطاء:

```typescript
// components/ErrorDisplay.tsx
import { AlertCircle, RefreshCw, HelpCircle } from 'lucide-react';

interface ErrorDisplayProps {
  error: {
    message: string;
    code: string;
    severity: 'info' | 'warning' | 'error' | 'critical';
    can_retry: boolean;
    suggestion?: string;
  };
  onRetry?: () => void;
  language?: 'ar' | 'en';
}

export function ErrorDisplay({ error, onRetry, language = 'ar' }: ErrorDisplayProps) {
  const severityColors = {
    info: 'bg-blue-50 border-blue-200 text-blue-800',
    warning: 'bg-yellow-50 border-yellow-200 text-yellow-800',
    error: 'bg-red-50 border-red-200 text-red-800',
    critical: 'bg-red-100 border-red-300 text-red-900'
  };

  return (
    <div
      className={`rounded-lg border-2 p-4 ${severityColors[error.severity]}`}
      dir={language === 'ar' ? 'rtl' : 'ltr'}
    >
      <div className="flex items-start gap-3">
        <AlertCircle className="w-5 h-5 mt-0.5 flex-shrink-0" />
        
        <div className="flex-1">
          <p className="font-semibold">{error.message}</p>
          
          {error.suggestion && (
            <p className="text-sm mt-2 opacity-90">{error.suggestion}</p>
          )}
          
          <p className="text-xs mt-2 opacity-70">
            {language === 'ar' ? 'رمز الخطأ' : 'Error code'}: {error.code}
          </p>
        </div>
        
        <div className="flex gap-2">
          {error.can_retry && onRetry && (
            <button
              onClick={onRetry}
              className="flex items-center gap-1 px-3 py-1.5 bg-white rounded-md hover:bg-gray-50 transition-colors text-sm"
            >
              <RefreshCw className="w-4 h-4" />
              {language === 'ar' ? 'إعادة المحاولة' : 'Retry'}
            </button>
          )}
          
          <button
            onClick={() => window.open('/help', '_blank')}
            className="flex items-center gap-1 px-3 py-1.5 bg-white rounded-md hover:bg-gray-50 transition-colors text-sm"
          >
            <HelpCircle className="w-4 h-4" />
            {language === 'ar' ? 'مساعدة' : 'Help'}
          </button>
        </div>
      </div>
    </div>
  );
}
```

---

## 📱 Toast Notifications

```typescript
// lib/toast.ts
import toast from 'react-hot-toast';

export const showErrorToast = (message: string, duration = 4000) => {
  toast.error(message, {
    duration,
    position: 'top-center',
    style: {
      fontFamily: 'Cairo, sans-serif',
      direction: 'rtl'
    }
  });
};

export const showSuccessToast = (message: string) => {
  toast.success(message, {
    duration: 3000,
    position: 'top-center',
    style: {
      fontFamily: 'Cairo, sans-serif',
      direction: 'rtl'
    }
  });
};

export const showInfoToast = (message: string) => {
  toast(message, {
    icon: 'ℹ️',
    duration: 3000,
    position: 'top-center'
  });
};
```

---

## 🧪 Testing Error Scenarios

```python
# tests/test_error_handling.py
import pytest
from app.core.errors.messages import get_error_message
from app.core.prosody.resilient_analyzer import ResilientAnalyzer

class TestErrorMessages:
    def test_arabic_error_messages(self):
        """التأكد من وجود رسائل عربية لكل خطأ"""
        error = get_error_message('invalid_arabic', language='ar')
        
        assert error['message']
        assert 'عربية' in error['message']  # Should mention Arabic
        assert error['code'] == 'ERR_INPUT_001'
    
    def test_error_with_variables(self):
        """اختبار الرسائل مع متغيرات"""
        error = get_error_message('text_too_long', language='ar', max_length=500)
        
        assert '500' in error['message']

class TestGracefulDegradation:
    def test_fallback_on_nlp_failure(self, monkeypatch):
        """اختبار التدهور التدريجي عند فشل NLP"""
        analyzer = ResilientAnalyzer()
        
        # محاكاة فشل المحلل الأساسي
        def mock_analyze_fail(text):
            raise Exception("CAMeL Tools failed")
        
        monkeypatch.setattr(
            analyzer.primary_analyzer,
            'analyze',
            mock_analyze_fail
        )
        
        # يجب أن يعمل المحلل الاحتياطي
        result = analyzer.analyze("قفا نبك")
        assert result['analysis_mode'] == 'fallback'
        assert 'warning' in result

class TestRetryLogic:
    def test_retry_on_transient_failure(self):
        """اختبار إعادة المحاولة عند فشل مؤقت"""
        attempts = []
        
        @retry_with_backoff(max_attempts=3, initial_delay=0.1)
        def flaky_function():
            attempts.append(1)
            if len(attempts) < 3:
                raise ConnectionError("Temporary failure")
            return "success"
        
        result = flaky_function()
        
        assert result == "success"
        assert len(attempts) == 3
```

---

**Last Updated:** November 8, 2025  
**Next Review:** Week 3 (after initial implementation)  
**Owner:** Backend + Frontend Leads
