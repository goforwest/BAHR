# 🏷️ Dataset Labeling Tool Specification
## Streamlit App for Efficient Verse Annotation

**Created:** November 8, 2025 (Based on Expert Review Feedback)
**Priority:** HIGH (Week 1 Friday - Quick Win #9)
**Time Investment:** 2-3 hours
**Impact:** 2x labeling speed (10-15 min/verse → 5-8 min/verse)
**Status:** Specification approved, awaiting implementation

---

## 📋 Purpose

**Problem:**
Manual labeling in Excel/text files is slow, error-prone, and lacks validation:
- 10-15 minutes per verse (slow)
- Typos in meter names (inconsistent)
- No auto-suggestion (reinventing the wheel)
- No progress tracking (demotivating)

**Solution:**
Build a lightweight **Streamlit web app** for efficient, validated, and semi-automated labeling.

**Expected Outcome:**
- Labeling speed: 5-8 min/verse (2x faster)
- Quality: Auto-suggest + manual verify (fewer errors)
- Consistency: Dropdown selection (no typos)
- Progress: Visual tracker (motivation)

---

## 🎯 Core Features

### 1. Verse Input & Display
- Text area for pasting Arabic verse
- RTL support for proper Arabic rendering
- Character counter (10-500 characters)
- Clear/reset button

### 2. Auto-Suggestion (Self-Training)
- Run your prosody engine on input verse
- Display top 3 meter suggestions with confidence scores
- User can accept suggestion or override manually

### 3. Manual Labeling Fields
- **Meter:** Dropdown (16 classical meters) + "أخرى" (other)
- **Era:** Radio buttons (كلاسيكي / حديث / معاصر)
- **Taqti3:** Text area (optional, for detailed pattern)
- **Source:** Text input (e.g., "المعلقات", "ديوان المتنبي")
- **Poet:** Text input (e.g., "امرؤ القيس")
- **Notes:** Text area (optional, for special cases)

### 4. Validation & Export
- Validation: Ensure required fields filled
- Preview: Show labeled data before saving
- Export: Append to JSONL file
- Progress: Show total verses labeled (with count)

### 5. Dataset Management
- Load existing dataset (to continue labeling)
- View statistics (verses per meter)
- Delete last entry (undo)
- Export full dataset as JSONL

---

## 🖥️ UI Design

### Layout Structure

```
┌─────────────────────────────────────────────────────────────┐
│  🏷️ BAHR Dataset Labeling Tool                    [v1.0]   │
├─────────────────────────────────────────────────────────────┤
│  Progress: 23/100 verses labeled  ███████░░░░ 23%          │
├─────────────────────────────────────────────────────────────┤
│  📝 Verse Input                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ قِفا نَبْكِ مِنْ ذِكْرى حَبيبٍ وَمَنزِلِ              │  │
│  │ بِسِقطِ اللِوى بَينَ الدَخولِ فَحَومَلِ              │  │
│  └───────────────────────────────────────────────────────┘  │
│  Characters: 78 | [Clear]                                  │
│                                                              │
│  🤖 Auto-Suggestions (Click to Accept)                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 1. الطويل ✅ (Confidence: 95%) [Accept]            │   │
│  │ 2. المديد (Confidence: 12%)                         │   │
│  │ 3. البسيط (Confidence: 8%)                          │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  📋 Manual Labels                                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Meter: [الطويل ▼]                                   │   │
│  │ Era: ○ كلاسيكي  ○ حديث  ○ معاصر                   │   │
│  │ Source: [المعلقات]                                  │   │
│  │ Poet: [امرؤ القيس]                                  │   │
│  │ Taqti3 (optional):                                  │   │
│  │ [فعولن مفاعيلن فعولن مفاعلن...]                    │   │
│  │ Notes (optional): [First verse of Mu'allaqat]       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  [💾 Save & Next]  [👁️ Preview]  [🗑️ Undo Last]         │
├─────────────────────────────────────────────────────────────┤
│  📊 Dataset Statistics                                      │
│  الطويل: 5 | الكامل: 4 | الوافر: 3 | ...                  │
│  Total: 23 verses across 8 meters                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technical Implementation

### Stack
- **Framework:** Streamlit (lightweight, Python-native)
- **Backend:** Your prosody engine (for auto-suggest)
- **Storage:** JSONL file (append-only, easy to version control)
- **Styling:** Streamlit native (no custom CSS needed for MVP)

### Dependencies
```toml
# pyproject.toml
[tool.poetry.dev-dependencies]
streamlit = "^1.28.0"
```

### File Structure
```
tools/
├── dataset_labeler.py      # Main Streamlit app
├── config.py               # Meter lists, default values
└── data/
    └── labeled_verses.jsonl  # Output file
```

---

## 💻 Implementation Code

### Main App (dataset_labeler.py)

```python
# tools/dataset_labeler.py

import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import sys

# Import your prosody engine (adjust path as needed)
sys.path.append('../backend')
from app.core.prosody.analyzer import ProsodyAnalyzer

# Configuration
METERS = [
    "الطويل", "المديد", "البسيط", "الوافر", "الكامل",
    "الهزج", "الرجز", "الرمل", "السريع", "المنسرح",
    "الخفيف", "المضارع", "المقتضب", "المجتث", "المتقارب", "المتدارك",
    "أخرى"
]

ERAS = ["كلاسيكي", "حديث", "معاصر"]

OUTPUT_FILE = Path("data/labeled_verses.jsonl")


def init_session_state():
    """Initialize Streamlit session state"""
    if 'labeled_count' not in st.session_state:
        st.session_state.labeled_count = count_labeled_verses()
    if 'last_suggestion' not in st.session_state:
        st.session_state.last_suggestion = None


def count_labeled_verses() -> int:
    """Count existing labeled verses in JSONL file"""
    if not OUTPUT_FILE.exists():
        return 0
    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        return sum(1 for line in f if line.strip())


def get_auto_suggestions(text: str) -> list:
    """Run prosody engine to get meter suggestions"""
    try:
        analyzer = ProsodyAnalyzer()
        result = analyzer.analyze(text)

        suggestions = [
            {
                "meter": result.detected_meter,
                "confidence": result.confidence
            }
        ]

        # Add alternatives
        for alt in result.alternative_meters[:2]:
            suggestions.append({
                "meter": alt['name'],
                "confidence": alt['confidence']
            })

        return suggestions

    except Exception as e:
        st.warning(f"Auto-suggestion failed: {e}")
        return []


def save_verse(data: dict):
    """Append labeled verse to JSONL file"""
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
        f.write('\n')

    st.session_state.labeled_count += 1


def load_dataset_stats() -> dict:
    """Load dataset and compute statistics"""
    if not OUTPUT_FILE.exists():
        return {}

    stats = {}
    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data = json.loads(line)
                meter = data.get('meter', 'Unknown')
                stats[meter] = stats.get(meter, 0) + 1

    return stats


def undo_last():
    """Remove last labeled verse"""
    if not OUTPUT_FILE.exists():
        return

    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if lines:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.writelines(lines[:-1])
        st.session_state.labeled_count -= 1
        st.success("✅ Last entry deleted")


# ============================================
# Main Streamlit App
# ============================================

def main():
    st.set_page_config(
        page_title="BAHR Dataset Labeler",
        page_icon="🏷️",
        layout="wide"
    )

    init_session_state()

    # Header
    st.title("🏷️ BAHR Dataset Labeling Tool")
    st.caption("Efficient verse annotation with auto-suggestions")

    # Progress bar
    target = 100
    progress = st.session_state.labeled_count / target
    st.progress(progress, text=f"Progress: {st.session_state.labeled_count}/{target} verses labeled ({progress*100:.0f}%)")

    st.divider()

    # ========================================
    # Verse Input
    # ========================================
    st.subheader("📝 Verse Input")

    verse_text = st.text_area(
        "Enter Arabic verse:",
        height=100,
        placeholder="قِفا نَبْكِ مِنْ ذِكْرى حَبيبٍ وَمَنزِلِ",
        help="Paste the verse you want to label (10-500 characters)"
    )

    char_count = len(verse_text.strip())
    col1, col2 = st.columns([3, 1])
    with col1:
        st.caption(f"Characters: {char_count}")
    with col2:
        if st.button("🗑️ Clear"):
            st.rerun()

    # Validate input length
    if verse_text and (char_count < 10 or char_count > 500):
        st.error("⚠️ Verse must be 10-500 characters")
        return

    # ========================================
    # Auto-Suggestions
    # ========================================
    if verse_text and len(verse_text.strip()) >= 10:
        st.subheader("🤖 Auto-Suggestions")

        with st.spinner("Analyzing verse..."):
            suggestions = get_auto_suggestions(verse_text)

        if suggestions:
            for i, sug in enumerate(suggestions, 1):
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.write(f"{i}. **{sug['meter']}**")
                with col2:
                    conf_color = "🟢" if sug['confidence'] > 0.85 else "🟡" if sug['confidence'] > 0.70 else "🔴"
                    st.write(f"{conf_color} {sug['confidence']*100:.0f}%")
                with col3:
                    if i == 1 and st.button("✅ Accept", key=f"accept_{i}"):
                        st.session_state.last_suggestion = sug['meter']

    st.divider()

    # ========================================
    # Manual Labeling
    # ========================================
    st.subheader("📋 Manual Labels")

    # Pre-fill with suggestion if accepted
    default_meter_idx = 0
    if st.session_state.last_suggestion in METERS:
        default_meter_idx = METERS.index(st.session_state.last_suggestion)

    meter = st.selectbox(
        "Meter (البحر) *",
        METERS,
        index=default_meter_idx
    )

    era = st.radio(
        "Era (العصر) *",
        ERAS,
        horizontal=True
    )

    col1, col2 = st.columns(2)
    with col1:
        source = st.text_input(
            "Source (المصدر) *",
            placeholder="المعلقات، ديوان المتنبي، ..."
        )
    with col2:
        poet = st.text_input(
            "Poet (الشاعر)",
            placeholder="امرؤ القيس، المتنبي، ..."
        )

    taqti3 = st.text_area(
        "Taqti3 (التقطيع) - Optional",
        placeholder="فعولن مفاعيلن فعولن مفاعلن",
        height=60
    )

    notes = st.text_area(
        "Notes (ملاحظات) - Optional",
        placeholder="Additional context or special cases",
        height=60
    )

    st.divider()

    # ========================================
    # Actions
    # ========================================
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💾 Save & Next", type="primary", use_container_width=True):
            # Validation
            if not verse_text or not meter or not era or not source:
                st.error("⚠️ Please fill all required fields (*)")
            else:
                # Prepare data
                data = {
                    "text": verse_text.strip(),
                    "meter": meter,
                    "era": era,
                    "source": source,
                    "poet": poet or "",
                    "taqti3": taqti3 or "",
                    "notes": notes or "",
                    "labeled_at": datetime.now().isoformat(),
                    "labeled_by": "dataset_labeler_v1"
                }

                # Save
                save_verse(data)
                st.success(f"✅ Verse #{st.session_state.labeled_count} saved!")
                st.balloons()

                # Reset form
                st.session_state.last_suggestion = None
                st.rerun()

    with col2:
        if st.button("👁️ Preview", use_container_width=True):
            preview_data = {
                "text": verse_text,
                "meter": meter,
                "era": era,
                "source": source,
                "poet": poet,
                "taqti3": taqti3,
                "notes": notes
            }
            st.json(preview_data)

    with col3:
        if st.button("🗑️ Undo Last", use_container_width=True):
            undo_last()

    st.divider()

    # ========================================
    # Dataset Statistics
    # ========================================
    st.subheader("📊 Dataset Statistics")

    stats = load_dataset_stats()

    if stats:
        # Display as columns
        cols = st.columns(4)
        for i, (meter, count) in enumerate(sorted(stats.items(), key=lambda x: x[1], reverse=True)):
            with cols[i % 4]:
                st.metric(meter, count)

        st.caption(f"**Total:** {sum(stats.values())} verses across {len(stats)} meters")

        # Download button
        if st.button("💾 Download Dataset"):
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                st.download_button(
                    label="Download JSONL",
                    data=f.read(),
                    file_name=f"bahr_dataset_{datetime.now().strftime('%Y%m%d')}.jsonl",
                    mime="application/json"
                )
    else:
        st.info("No verses labeled yet. Start labeling above! 👆")


if __name__ == "__main__":
    main()
```

---

## 🚀 Usage Instructions

### Installation
```bash
# Install Streamlit
pip install streamlit

# Or add to pyproject.toml
poetry add --dev streamlit
```

### Running the App
```bash
# From project root
cd tools
streamlit run dataset_labeler.py

# Browser opens automatically at http://localhost:8501
```

### Labeling Workflow
1. **Paste verse** into text area
2. **Review auto-suggestions** (top 3 meters)
3. **Accept suggestion** or select manually from dropdown
4. **Fill required fields:** Era, Source
5. **Add optional fields:** Poet, Taqti3, Notes
6. **Preview** before saving (optional)
7. **Click "Save & Next"** → verse appended to JSONL
8. **Repeat** for next verse

### Output Format (JSONL)
```json
{"text": "قفا نبك من ذكرى حبيب ومنزل", "meter": "الطويل", "era": "كلاسيكي", "source": "المعلقات", "poet": "امرؤ القيس", "taqti3": "فعولن مفاعيلن فعولن مفاعلن", "notes": "First verse", "labeled_at": "2025-11-08T10:30:00", "labeled_by": "dataset_labeler_v1"}
{"text": "أَلا في سَبيلِ المَجدِ ما أَنا فاعِلُ", "meter": "الرجز", "era": "كلاسيكي", "source": "ديوان الشعر", "poet": "المتنبي", "taqti3": "", "notes": "", "labeled_at": "2025-11-08T10:35:00", "labeled_by": "dataset_labeler_v1"}
```

---

## 📊 Expected Impact

### Time Savings

| Task | Before (Manual) | After (Tool) | Savings |
|------|----------------|--------------|---------|
| Input verse | 1 min | 30 sec | 50% |
| Determine meter | 5-8 min | 1-2 min (auto-suggest) | 70% |
| Type meter name | 30 sec | 5 sec (dropdown) | 80% |
| Add metadata | 2 min | 1 min | 50% |
| Save to file | 1 min | 5 sec (one click) | 90% |
| **Total per verse** | **10-15 min** | **5-8 min** | **50%** |

**For 100 verses:**
- Manual: 16-25 hours
- With tool: 8-13 hours
- **Saved:** 8-12 hours 🎉

### Quality Improvements
- ✅ No typos in meter names (dropdown)
- ✅ Consistent formatting (JSON schema)
- ✅ Auto-suggestions reduce errors (verify vs create)
- ✅ Progress tracking (motivation)

---

## 🔧 Week 1 Friday Implementation Schedule

**Total Time:** 2-3 hours

**Hour 1: Core Functionality**
- Create `dataset_labeler.py` file
- Implement verse input + manual labeling form
- Basic JSONL saving (no auto-suggest yet)
- Test with 2-3 sample verses

**Hour 2: Auto-Suggestion Integration**
- Import prosody analyzer
- Add suggestion display
- Add "Accept" button logic
- Test accuracy of suggestions

**Hour 3: Polish & Validation**
- Add progress bar
- Add dataset statistics
- Add undo function
- Add input validation
- Test full workflow

**Acceptance Criteria:**
- ✅ Can label 5 verses in < 30 minutes
- ✅ Auto-suggestions work (even if not perfect)
- ✅ JSONL output validates correctly
- ✅ UI is intuitive (no instruction needed)

---

## 🎯 Success Metrics

**You've succeeded when:**
- Labeling 100 verses takes < 13 hours (not 20+ hours)
- Auto-suggestions accepted > 50% of the time
- Zero typos in meter names (dropdown enforcement)
- Dataset statistics motivate continued labeling

**ROI:**
- 2-3 hours invested
- 8-12 hours saved
- **4-6x return on investment** 📈

---

## 🔮 Future Enhancements (Optional)

### Phase 2 Additions (Post-MVP):
1. **Batch Import:** Upload CSV/Excel → convert to JSONL
2. **Collaboration:** Multi-user labeling with conflict resolution
3. **Quality Checks:** Flag low-confidence suggestions for review
4. **Export Formats:** Support CSV, Excel, SQL for flexibility
5. **Annotation History:** Track changes, allow edits
6. **Inter-annotator Agreement:** Compare labels from multiple users

### Advanced Features:
- Image OCR: Extract verses from scanned books
- Audio transcription: Label recited poetry
- API integration: Fetch verses from Arabic poetry databases

---

## ✅ Acceptance Criteria

**Feature is complete when:**

1. ✅ Streamlit app runs locally without errors
2. ✅ Can label verses with all required fields
3. ✅ Auto-suggestions display correctly
4. ✅ JSONL file appends properly (no corruption)
5. ✅ Progress bar updates in real-time
6. ✅ Statistics refresh after each save
7. ✅ Undo function works correctly
8. ✅ UI is RTL-friendly for Arabic text
9. ✅ Tool saves 50%+ time vs manual labeling
10. ✅ Documentation (this file) explains usage clearly

---

## 📝 Testing Checklist

```yaml
Manual Testing (30 minutes):
  - □ Label 5 verses (varied meters)
  - □ Test auto-suggestions (accept/reject)
  - □ Test undo function
  - □ Verify JSONL output format
  - □ Check statistics accuracy
  - □ Test with very long verse (edge case)
  - □ Test with empty inputs (validation)
  - □ Test progress bar updates

Edge Cases:
  - □ Special characters (?, !, ...)
  - □ Mixed Arabic/English text
  - □ Very short verse (< 10 chars)
  - □ Very long verse (> 500 chars)
  - □ Restart app (data persists)
```

---

**Specification Status:** ✅ **APPROVED FOR IMPLEMENTATION**

**Implementation Target:** Week 1 Friday (2-3 hours)
**Priority:** HIGH (enables efficient dataset collection)
**Success Metric:** 50%+ time savings vs manual labeling

---

**Last Updated:** November 8, 2025
**Author:** Senior Technical Documentation Specialist
**Review After:** Week 1 Friday (post-implementation usability test)
