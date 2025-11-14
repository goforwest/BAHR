# Multi-Candidate Meter Detection UI - Implementation Spec

**Status:** Ready for Frontend Implementation
**Estimated Effort:** 2-3 days
**Priority:** High (improves user experience for uncertain detections)

---

## 🎯 **Objective**

Show users **multiple meter candidates** when detection is uncertain, allowing them to:
1. See alternative possibilities (e.g., "الرجز (98%) or الطويل (98%)?")
2. Provide feedback on correctness
3. Help improve the system through feedback collection

---

## 📊 **When to Show Multiple Candidates**

### Trigger Conditions

Show multiple candidates when **any** of these conditions are met:

```python
# Backend logic (already implemented via API)
show_multiple = (
    confidence < 0.90 or                    # Low confidence
    (top2_diff < 0.05 and confidence < 0.95)  # Close race
)
```

**Examples:**
- الرجز: 98.39%, الطويل: 97.62% → **Show both** (diff: 0.77%)
- الطويل: 95%, الكامل: 85% → **Show top 1** (diff: 10%, clear winner)
- البسيط: 93%, المتقارب: 82% → **Show top 1** (diff: 11%)

---

## 🎨 **UI Design Mockup**

### Current UI (Single Meter)
```
┌─────────────────────────────────────┐
│ Detected Meter: الطويل              │
│ Confidence: 95%                     │
│ Quality: Excellent                  │
└─────────────────────────────────────┘
```

### New UI (Multiple Candidates)
```
┌──────────────────────────────────────────────────┐
│ ⚠️ Uncertain Detection - Multiple Possibilities  │
├──────────────────────────────────────────────────┤
│                                                  │
│ 🥇 الرجز (al-Rajaz)            98.4% ◯ Select  │
│    Pattern: /o/o//o/o/o//o/o/o//                │
│    Transformations: base, خبن, base             │
│                                                  │
│ 🥈 الطويل (at-Tawil)           97.6% ◯ Select  │
│    Pattern: /o//o//o/o/o/o//o//o/o/            │
│    Transformations: base, قبض, base, حذف        │
│                                                  │
│ 🥉 السريع (as-Sari')           95.2% ◯ Select  │
│    Pattern: /o/o//o/o///o///o                  │
│    Transformations: base, خبن, خبن              │
│                                                  │
├──────────────────────────────────────────────────┤
│ [ 💬 Report Correct Meter ]                     │
└──────────────────────────────────────────────────┘
```

### Additional Recommendations Section
```
┌──────────────────────────────────────────────────┐
│ 💡 Recommendation                                 │
│                                                  │
│ The detection is uncertain because the verse    │
│ is undiacritized. Adding diacritics (tashkeel)  │
│ will significantly improve accuracy.             │
│                                                  │
│ [ 📝 Add Diacritics ] [ ℹ️ Learn More ]         │
└──────────────────────────────────────────────────┘
```

---

## 🔧 **API Changes Required**

### Current Response (Single Meter)
```json
{
  "bahr": {
    "id": 1,
    "name_ar": "الطويل",
    "name_en": "at-Tawil",
    "confidence": 0.95,
    "match_quality": "exact",
    "matched_pattern": "/o//o//o/o/o/o//o//o/o/",
    "transformations": ["base", "base", "base", "base"]
  }
}
```

### Enhanced Response (Multiple Candidates)
```json
{
  "bahr": {
    "id": 1,
    "name_ar": "الرجز",
    "name_en": "al-Rajaz",
    "confidence": 0.9839,
    "match_quality": "exact",
    "matched_pattern": "/o/o//o/o/o//o/o/o//",
    "transformations": ["base", "خبن", "base"]
  },
  "alternative_meters": [
    {
      "id": 2,
      "name_ar": "الطويل",
      "name_en": "at-Tawil",
      "confidence": 0.9762,
      "match_quality": "strong",
      "matched_pattern": "/o//o//o/o/o/o//o//o/o/",
      "transformations": ["base", "قبض", "base", "حذف"],
      "confidence_diff": 0.0077
    },
    {
      "id": 8,
      "name_ar": "السريع",
      "name_en": "as-Sari'",
      "confidence": 0.9524,
      "match_quality": "strong",
      "matched_pattern": "/o/o//o/o///o///o",
      "transformations": ["base", "خبن", "خبن"],
      "confidence_diff": 0.0315
    }
  ],
  "detection_uncertainty": {
    "is_uncertain": true,
    "reason": "close_candidates",
    "top_diff": 0.0077,
    "recommendation": "add_diacritics"
  }
}
```

### Backend Implementation (in `analyze_v2.py`)

```python
# After detection
if detection_result:
    # Get top 3 candidates for comparison
    all_candidates = detect_with_phoneme_fitness(
        normalized_text,
        has_tashkeel,
        bahr_detector_v2,
        top_k=3,
        use_hybrid_scoring=True
    )

    # Check if uncertain
    is_uncertain = False
    reason = None

    if detection_result.confidence < 0.90:
        is_uncertain = True
        reason = "low_confidence"
    elif len(all_candidates) >= 2:
        top_diff = all_candidates[0][2] - all_candidates[1][2]  # score diff
        if top_diff < 0.05:
            is_uncertain = True
            reason = "close_candidates"

    # Build alternative meters list
    alternative_meters = []
    if is_uncertain and len(all_candidates) > 1:
        for meter_id, name_ar, score, pattern in all_candidates[1:]:
            meter = METERS_REGISTRY.get(meter_id)
            if meter:
                alternative_meters.append({
                    "id": meter_id,
                    "name_ar": name_ar,
                    "name_en": meter.name_en,
                    "confidence": score,
                    "matched_pattern": pattern,
                    "confidence_diff": all_candidates[0][2] - score
                })

    # Add to response
    response_data["alternative_meters"] = alternative_meters
    response_data["detection_uncertainty"] = {
        "is_uncertain": is_uncertain,
        "reason": reason,
        "top_diff": top_diff if len(all_candidates) >= 2 else None,
        "recommendation": "add_diacritics" if not has_tashkeel else None
    }
```

---

## 💾 **Feedback Collection**

### New Endpoint: Submit Meter Feedback

**Endpoint:** `POST /api/v1/feedback/meter`

**Request:**
```json
{
  "text": "قفا نبك من ذكرى حبيب ومنزل",
  "normalized_text": "قفا نبك من ذكري حبيب ومنزل",
  "detected_meter": "الرجز",
  "detected_confidence": 0.9839,
  "user_selected_meter": "الطويل",
  "alternatives_shown": ["الرجز", "الطويل", "السريع"],
  "has_tashkeel": false,
  "user_comment": "This is the famous Mu'allaqah verse",
  "timestamp": "2025-11-12T10:30:00Z"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Thank you for your feedback!",
  "feedback_id": "fb_1234567890"
}
```

### Backend Implementation

```python
# New file: backend/app/api/v1/endpoints/feedback.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import json
from pathlib import Path

router = APIRouter()

class MeterFeedback(BaseModel):
    text: str
    normalized_text: str
    detected_meter: str
    detected_confidence: float
    user_selected_meter: str
    alternatives_shown: list[str]
    has_tashkeel: bool
    user_comment: str = ""
    timestamp: datetime

@router.post("/meter")
async def submit_meter_feedback(feedback: MeterFeedback):
    """
    Collect user feedback on meter detection.

    This data can be used to:
    1. Identify problematic verses
    2. Train ML models
    3. Improve detection rules
    """
    # Save to feedback log (append to JSONL file)
    feedback_file = Path("data/feedback/meter_feedback.jsonl")
    feedback_file.parent.mkdir(parents=True, exist_ok=True)

    with open(feedback_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(feedback.dict(), ensure_ascii=False) + '\n')

    # Generate feedback ID
    feedback_id = f"fb_{int(datetime.now().timestamp())}"

    return {
        "status": "success",
        "message": "شكراً لملاحظاتك! | Thank you for your feedback!",
        "feedback_id": feedback_id
    }
```

---

## 🎯 **Frontend Tasks**

### 1. Update Analyze Result Component
**File:** `frontend/src/components/AnalyzeResult.tsx` (or equivalent)

- [ ] Add `alternativeMeters` prop support
- [ ] Add `detectionUncertainty` prop support
- [ ] Create `MultiCandidateView` component
- [ ] Add radio buttons or cards for meter selection
- [ ] Show confidence percentages with visual bars
- [ ] Display pattern and transformations (collapsible)

### 2. Create Feedback Dialog
**File:** `frontend/src/components/FeedbackDialog.tsx`

- [ ] Modal/dialog for feedback submission
- [ ] Text area for optional comments
- [ ] Submit button with API integration
- [ ] Success/error toast notifications
- [ ] Track feedback in analytics

### 3. Add Uncertainty Banner
**File:** `frontend/src/components/UncertaintyBanner.tsx`

- [ ] Warning icon + message
- [ ] "Add Diacritics" button (opens diacritization guide)
- [ ] "Learn More" link (explains meter detection)
- [ ] Only show when `detection_uncertainty.is_uncertain === true`

### 4. Update API Client
**File:** `frontend/src/api/analyze.ts`

- [ ] Update response types to include `alternative_meters`
- [ ] Update response types to include `detection_uncertainty`
- [ ] Add `submitMeterFeedback()` function

### 5. Add Analytics Tracking
- [ ] Track when multiple candidates are shown
- [ ] Track which meter users select (if they interact)
- [ ] Track feedback submission rate
- [ ] Track "Add Diacritics" button clicks

---

## 📊 **Success Metrics**

Track these metrics after launch:

1. **Uncertainty Rate**: % of detections marked as uncertain
2. **User Interaction Rate**: % of users who select a different meter
3. **Feedback Submission Rate**: % of uncertain cases with feedback
4. **Most Confused Pairs**: Which meter pairs are most often confused (e.g., الطويل/الرجز)
5. **Diacritics Impact**: Compare accuracy before/after diacritics added

---

## 🚀 **Implementation Phases**

### Phase 1: Backend (2-3 hours)
- [ ] Add `alternative_meters` to API response
- [ ] Add `detection_uncertainty` logic
- [ ] Create feedback endpoint
- [ ] Test with golden set

### Phase 2: Frontend Core (1 day)
- [ ] Create `MultiCandidateView` component
- [ ] Update API client
- [ ] Basic uncertainty display
- [ ] Test with mock data

### Phase 3: Frontend Polish (1 day)
- [ ] Add feedback dialog
- [ ] Add uncertainty banner
- [ ] Visual improvements (icons, colors, animations)
- [ ] Responsive design

### Phase 4: Analytics & Monitoring (0.5 day)
- [ ] Add event tracking
- [ ] Set up feedback dashboard
- [ ] Monitor metrics

---

## 🎨 **Design Tokens**

```css
/* Colors */
--uncertain-warning: #ff9800;  /* Orange for uncertainty banner */
--candidate-1st: #4caf50;      /* Green for top candidate */
--candidate-2nd: #2196f3;      /* Blue for 2nd candidate */
--candidate-3rd: #9e9e9e;      /* Gray for 3rd candidate */

/* Spacing */
--candidate-card-gap: 12px;
--confidence-bar-height: 6px;

/* Borders */
--candidate-border: 2px solid var(--candidate-color);
--candidate-border-radius: 8px;
```

---

## 📚 **Example User Flows**

### Flow 1: User Sees Uncertainty, Accepts Top Candidate
1. User submits undiacritized verse
2. System shows: "الرجز (98%) or الطويل (98%)?"
3. User reads both, agrees with الرجز
4. User clicks "Continue" (no action needed)

### Flow 2: User Corrects Detection
1. User submits undiacritized verse
2. System shows: "الرجز (98%) or الطويل (98%)?"
3. User knows it's actually الطويل (famous poem)
4. User selects الطويل radio button
5. Analysis updates with correct meter
6. Feedback logged automatically

### Flow 3: User Adds Diacritics
1. User submits undiacritized verse
2. System shows uncertainty + "Add Diacritics" button
3. User clicks button, sees diacritization guide
4. User adds diacritics, resubmits
5. Confidence improves to 99%, single candidate shown

---

## ✅ **Testing Checklist**

- [ ] Test with Mu'allaqah verse (should show الرجز/الطويل)
- [ ] Test with clear cases (should show single meter)
- [ ] Test with diacritized text (should have fewer uncertainties)
- [ ] Test feedback submission (should log to file)
- [ ] Test on mobile (responsive design)
- [ ] Test with screen readers (accessibility)
- [ ] Load test feedback endpoint (rate limiting)

---

**Ready for implementation!** This spec provides everything needed for frontend developers to implement multi-candidate detection UI.
