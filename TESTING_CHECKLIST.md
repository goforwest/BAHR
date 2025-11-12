# Multi-Candidate Detection - Testing Checklist

**Status:** Ready for Testing
**Date:** 2025-11-12

---

## 🧪 **Backend Testing**

### API Endpoints

- [ ] **GET /api/v1/analyze-v2/** - Returns multi-candidate data
  ```bash
  curl -X POST http://localhost:8000/api/v1/analyze-v2/ \
    -H "Content-Type: application/json" \
    -d '{"text": "قفا نبك من ذكرى حبيب ومنزل", "detect_bahr": true}'
  ```
  - [ ] Response includes `alternative_meters` field
  - [ ] Response includes `detection_uncertainty` field
  - [ ] Mu'allaqah verse shows الرجز and الطويل as close alternatives

- [ ] **POST /api/v1/feedback/meter** - Accepts feedback
  ```bash
  curl -X POST http://localhost:8000/api/v1/feedback/meter \
    -H "Content-Type: application/json" \
    -d '{
      "text": "قفا نبك من ذكرى حبيب ومنزل",
      "normalized_text": "قفا نبك من ذكري حبيب ومنزل",
      "detected_meter": "الرجز",
      "detected_confidence": 0.9581,
      "user_selected_meter": "الطويل",
      "alternatives_shown": ["الرجز", "الطويل"],
      "has_tashkeel": false,
      "timestamp": "2025-11-12T10:00:00Z"
    }'
  ```
  - [ ] Returns success status and feedback_id
  - [ ] Data saved to `data/feedback/meter_feedback.jsonl`

- [ ] **GET /api/v1/feedback/stats** - Returns statistics
  ```bash
  curl http://localhost:8000/api/v1/feedback/stats
  ```
  - [ ] Shows total feedback count
  - [ ] Shows correction rate
  - [ ] Shows confused meter pairs

### Python Scripts

- [ ] **Multi-candidate detection test**
  ```bash
  cd /home/user/BAHR
  python test_multi_candidate.py
  ```
  - [ ] Shows 3 candidates for Mu'allaqah verse
  - [ ] Flags as UNCERTAIN (close_candidates)
  - [ ] Difference is 0.42%

- [ ] **Feedback collection test**
  ```bash
  python test_feedback.py
  ```
  - [ ] Successfully submits feedback
  - [ ] Returns bilingual success message
  - [ ] Creates feedback file

- [ ] **Confusion analysis**
  ```bash
  python -m backend.app.tools.analyze_confusion_patterns
  ```
  - [ ] Shows summary report
  - [ ] Identifies الرجز ↔ الطويل pattern
  - [ ] Calculates correction rate

---

## 🎨 **Frontend Testing**

### Prerequisites

```bash
cd /home/user/BAHR/frontend
npm install
npm run dev
```

Open http://localhost:3000 in browser.

### Test Cases

#### Test Case 1: Uncertain Detection (Mu'allaqah Verse)

**Input:**
```
قفا نبك من ذكرى حبيب ومنزل
```

**Expected UI:**
- [ ] ⚠️ UncertaintyBanner appears
  - [ ] Shows "Multiple close possibilities detected"
  - [ ] Shows confidence difference (0.42%)
  - [ ] Shows "Add Diacritics" button

- [ ] 📋 MultiCandidateView displays
  - [ ] Shows 3 candidates with medals (🥇🥈🥉)
  - [ ] الرجز at 95.81%
  - [ ] الطويل at 95.39%
  - [ ] السريع at 94.59%
  - [ ] Confidence bars render correctly
  - [ ] Radio buttons work
  - [ ] "Show details" expands pattern/transformations

- [ ] 💬 "Report Correct Meter" button visible
  - [ ] Clicking opens FeedbackDialog
  - [ ] Dialog pre-selects user's meter choice
  - [ ] Can add optional comment
  - [ ] Submit button works
  - [ ] Success message shows
  - [ ] Dialog closes after 2 seconds

#### Test Case 2: Certain Detection

**Input:**
```
أَلا لَيتَ الشَبابَ يَعودُ يَوماً
```
(with diacritics)

**Expected UI:**
- [ ] No UncertaintyBanner
- [ ] No MultiCandidateView
- [ ] Traditional single Bahr card shown
- [ ] Shows الطويل with high confidence (>95%)

#### Test Case 3: Feedback Submission

**Steps:**
1. Submit Mu'allaqah verse
2. Select الطويل from alternatives
3. Click "Report Correct Meter"
4. Add comment: "This is the famous Mu'allaqah"
5. Submit

**Expected:**
- [ ] FeedbackDialog shows correct detected meter
- [ ] Dropdown has all alternatives
- [ ] Comment field accepts Arabic/English
- [ ] Submit button shows loading state
- [ ] Success message appears
- [ ] Backend receives feedback (check logs)
- [ ] Feedback saved to JSONL file

---

## 🔄 **Integration Testing**

### End-to-End Flow

- [ ] **Flow 1: User correction improves system**
  1. User submits verse → Gets uncertain detection
  2. User selects correct meter → Submits feedback
  3. Feedback stored → Appears in stats endpoint
  4. Confusion analysis identifies pattern

- [ ] **Flow 2: Add diacritics recommendation**
  1. Submit undiacritized verse → Shows uncertainty
  2. Click "Add Diacritics" → Scrolls to input
  3. User adds diacritics → Resubmits
  4. Detection confidence improves → No uncertainty

---

## 📊 **Performance Testing**

- [ ] **Backend Performance**
  - [ ] Multi-candidate detection < 2 seconds
  - [ ] Feedback submission < 500ms
  - [ ] Stats endpoint < 1 second (with 100+ feedback entries)

- [ ] **Frontend Performance**
  - [ ] Components render smoothly
  - [ ] Animations don't lag
  - [ ] Dialog opens/closes without delay
  - [ ] Radio button selection is instant

---

## 🌐 **Cross-Browser Testing**

- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari (if available)
- [ ] Mobile browsers (responsive design)

### RTL (Right-to-Left) Testing

- [ ] Arabic text displays correctly RTL
- [ ] English text displays correctly LTR
- [ ] Mixed content aligns properly
- [ ] Margins/padding respect direction

---

## ♿ **Accessibility Testing**

- [ ] **Keyboard Navigation**
  - [ ] Tab through all interactive elements
  - [ ] Radio buttons selectable with keyboard
  - [ ] Dialog closable with Escape key
  - [ ] Submit with Enter key

- [ ] **Screen Readers**
  - [ ] ARIA labels present
  - [ ] Meter names announced correctly
  - [ ] Confidence percentages readable
  - [ ] Button purposes clear

- [ ] **Visual**
  - [ ] Sufficient color contrast
  - [ ] Focus indicators visible
  - [ ] Text readable at 200% zoom

---

## 🐛 **Error Handling**

- [ ] **Network Errors**
  - [ ] Backend down → Shows error message
  - [ ] Timeout → Shows retry option
  - [ ] 500 error → User-friendly message

- [ ] **Validation Errors**
  - [ ] Empty text → Validation message
  - [ ] Too long text → Character limit warning
  - [ ] Invalid characters → Sanitized or rejected

- [ ] **Feedback Errors**
  - [ ] Failed submission → Error notification
  - [ ] Network timeout → Retry button
  - [ ] Server error → Helpful message

---

## 📈 **Data Quality Testing**

- [ ] **Feedback Data Integrity**
  - [ ] All required fields present in JSONL
  - [ ] Timestamps in correct format
  - [ ] Arabic text encoded properly (UTF-8)
  - [ ] No data corruption

- [ ] **Confusion Analysis Accuracy**
  - [ ] Correctly identifies meter pairs
  - [ ] Accurate correction counts
  - [ ] Proper directionality analysis

---

## 🚀 **Deployment Readiness**

- [ ] **Environment Variables**
  - [ ] NEXT_PUBLIC_API_URL set for production
  - [ ] Backend API_BASE_URL configured
  - [ ] CORS settings allow frontend domain

- [ ] **Backend Setup**
  - [ ] `data/feedback/` directory created
  - [ ] Write permissions for feedback file
  - [ ] API endpoints registered in router

- [ ] **Frontend Build**
  ```bash
  cd frontend
  npm run build
  ```
  - [ ] Build succeeds without errors
  - [ ] No TypeScript errors
  - [ ] No console warnings

---

## ✅ **Sign-Off Checklist**

Before declaring "ready for production":

- [ ] All backend API tests pass
- [ ] All frontend UI tests pass
- [ ] End-to-end flows work
- [ ] Performance is acceptable
- [ ] Accessibility requirements met
- [ ] Error handling tested
- [ ] Cross-browser compatibility verified
- [ ] Mobile responsiveness confirmed
- [ ] Documentation complete
- [ ] Team reviewed and approved

---

## 📝 **Testing Notes**

**Tested By:** _______________
**Date:** _______________
**Environment:** _______________

**Issues Found:**
1.
2.
3.

**Overall Status:** ⬜ Pass | ⬜ Fail | ⬜ Needs Review

---

**Last Updated:** 2025-11-12
**Version:** 1.0
