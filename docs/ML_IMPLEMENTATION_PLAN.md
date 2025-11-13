# BAHR Phase 3: Machine Learning Implementation Plan

**Date**: 2025-11-13
**Project**: BAHR (بحر) Arabic Prosody Engine
**Plan Version**: 1.0
**Prerequisites**: ML Readiness Assessment completed (see `ML_READINESS_REPORT.md`)

---

## Executive Summary

**Goal**: Achieve 80-85% Top-1 accuracy on Arabic meter detection using hybrid rule-based + ML approach

**Current Baseline**: 41.19% (hybrid detector) / 50.3% (empirical baseline)
**Target**: 80-85% (+39-44 percentage points from current, +30-35 from empirical)
**Timeline**: 5.5-6.5 weeks total (1.5-2 weeks gap closure + 4 weeks ML implementation)
**Approach**: Gradient Boosting (XGBoost) with prosodic rule features + data augmentation

---

## Phase 0: Gap Closure (1.5-2 weeks)

**Status**: ⚠️ CRITICAL - Must complete before ML work

### Week 0.1: Critical Fixes (Days 1-5)

#### Day 1: Environment Setup (P0)

**Task 1.1: Install ML Libraries**
- **Duration**: 10 minutes
- **Owner**: DevOps/ML Engineer
- **Actions**:
  ```bash
  pip install scikit-learn pandas numpy matplotlib jupyter xgboost lightgbm
  ```
- **Verification**:
  ```python
  import sklearn, pandas, numpy, matplotlib, jupyter, xgboost
  print(f"scikit-learn: {sklearn.__version__}")
  print(f"pandas: {pandas.__version__}")
  print(f"xgboost: {xgboost.__version__}")
  ```
- **Success Criteria**: All libraries import successfully

**Task 1.2: Create ML Directory Structure**
- **Duration**: 10 minutes
- **Actions**:
  ```bash
  mkdir -p backend/app/ml
  mkdir -p backend/app/models
  mkdir -p notebooks
  mkdir -p dataset/ml
  mkdir -p docs/ml
  touch backend/app/ml/__init__.py
  touch backend/app/ml/feature_extractor.py
  touch backend/app/ml/trainer.py
  ```
- **Deliverable**: Clean directory structure for ML work

---

#### Days 2-3: Debug Performance Regression (P0)

**Task 2.1: Investigate Hybrid Detector Regression**
- **Duration**: 1-2 days
- **Owner**: Prosody Engineer
- **Problem**: Hybrid detector (41.19%) worse than empirical baseline (50.3%)
- **Actions**:
  1. **Review hybrid detector code**:
     - Check `backend/app/core/prosody/detector_v2.py`
     - Verify fuzzy matching logic
     - Check meter label format consistency

  2. **Analyze validation results**:
     - Load `hybrid_validation_results.json`
     - Identify which meters regressed (السريع: 0% vs 76.5%)
     - Check confusion matrix

  3. **Debug meter confusion**:
     ```python
     # For each meter with 0% accuracy:
     - السريع: 0/34 (was 76.5% - major regression)
     - المديد: 0/20 (was 75.0% - major regression)
     - المجتث: 0/20 (was 100.0% - critical regression)
     - المضارع: 0/25 (was 92.0% - critical regression)
     - المقتضب: 0/30 (was 15.4% - maintained bad performance)
     ```

  4. **Check meter label format**:
     - Verify golden dataset uses exact meter names
     - Check for Unicode normalization issues
     - Verify no extra spaces or diacritics in labels

  5. **Run comparative test**:
     ```python
     # Test same verse with:
     # - Old empirical detector (50.3%)
     # - New hybrid detector (41.19%)
     # - Identify where logic differs
     ```

- **Hypotheses to Test**:
  - H1: Fuzzy matching threshold too high (rejecting good matches)
  - H2: Meter label format mismatch (e.g., "السريع" vs "السريع (مفعولات)")
  - H3: Pattern normalization breaking similarity calculation
  - H4: Empirical patterns not loading correctly

- **Deliverable**: Root cause analysis document + fix implemented

**Task 2.2: Fix Regression and Re-validate**
- **Duration**: 0.5-1 day
- **Actions**:
  1. Implement fix based on root cause
  2. Re-run validation on 471 verses
  3. Confirm accuracy ≥50.3% (matching or beating empirical)
  4. Generate new validation report

- **Success Criteria**:
  - ✅ Hybrid detector achieves ≥50.3% Top-1 accuracy
  - ✅ No meter with 0% accuracy (all meters ≥10%)
  - ✅ Validation report generated with per-meter breakdown

---

#### Days 3-5: Implement Feature Extractor (P0)

**Task 3.1: Design Feature Extraction Pipeline**
- **Duration**: 0.5 day
- **Owner**: ML Engineer
- **Actions**:
  1. Define feature schema (50 features, see detailed design below)
  2. Create `backend/app/ml/feature_extractor.py`
  3. Define `BAHRFeatureExtractor` class interface

**Feature Schema** (50 features total):

```python
class BAHRFeatureExtractor:
    """
    Extracts 50 features from Arabic verse for ML meter classification
    """

    FEATURE_CATEGORIES = {
        'pattern_based': 8,      # Pattern structure features
        'similarity': 16,        # Similarity to each meter
        'rule_based': 16,        # Prosodic transformation features
        'linguistic': 10         # Arabic linguistic features
    }

    def extract_features(self, verse_text: str) -> np.ndarray:
        """
        Extract all features from verse

        Returns:
            np.ndarray: (50,) feature vector
        """
        features = []

        # 1. Extract phonetic pattern
        pattern = text_to_phonetic_pattern(verse_text)

        # 2. Pattern-based features (8)
        features.extend(self._extract_pattern_features(pattern))

        # 3. Similarity features (16)
        features.extend(self._extract_similarity_features(pattern))

        # 4. Rule-based features (16)
        features.extend(self._extract_rule_features(verse_text, pattern))

        # 5. Linguistic features (10)
        features.extend(self._extract_linguistic_features(verse_text))

        return np.array(features)

    def _extract_pattern_features(self, pattern: str) -> List[float]:
        """
        Extract 8 pattern-based features

        Returns:
            [
                pattern_length,           # int (0-50)
                o_count,                  # int (0-30)
                slash_count,              # int (0-40)
                o_ratio,                  # float (0-1)
                slash_ratio,              # float (0-1)
                avg_segment_length,       # float (1-10)
                pattern_entropy,          # float (0-1)
                pattern_variance          # float (0-10)
            ]
        """
        # Implementation details...

    def _extract_similarity_features(self, pattern: str) -> List[float]:
        """
        Extract 16 similarity features (one per meter)

        Returns:
            [
                similarity_to_tawil,      # float (0-1)
                similarity_to_basit,      # float (0-1)
                similarity_to_wafir,      # float (0-1)
                ...                       # 13 more meters
            ]
        """
        # Use pattern_similarity module
        from app.core.prosody.pattern_similarity import calculate_pattern_similarity

        meters = [
            'الطويل', 'البسيط', 'الوافر', 'الكامل', 'الرمل',
            'الخفيف', 'الرجز', 'المتقارب', 'المتدارك', 'الهزج',
            'المديد', 'المنسرح', 'المجتث', 'المقتضب', 'المضارع', 'السريع'
        ]

        similarities = []
        for meter in meters:
            representative_pattern = self._get_meter_pattern(meter)
            sim = calculate_pattern_similarity(pattern, representative_pattern)
            similarities.append(sim)

        return similarities

    def _extract_rule_features(self, text: str, pattern: str) -> List[float]:
        """
        Extract 16 rule-based prosodic features

        Returns:
            [
                # Transformation detection (10 binary features)
                has_qabd,                 # 0/1
                has_khabn,                # 0/1
                has_idmar,                # 0/1
                has_tayy,                 # 0/1
                has_kaff,                 # 0/1
                has_hadhf,                # 0/1
                has_qat,                  # 0/1
                has_qasr,                 # 0/1
                has_kashf,                # 0/1
                has_batr,                 # 0/1

                # Transformation counts (2 features)
                transformation_count,     # int (0-5)
                unique_transformations,   # int (0-10)

                # Match quality (4 features)
                has_empirical_match,      # 0/1
                empirical_confidence,     # float (0-1)
                theoretical_confidence,   # float (0-1)
                rule_consistency_score    # float (0-1)
            ]
        """
        # Implementation using zihafat/ilal modules

    def _extract_linguistic_features(self, text: str) -> List[float]:
        """
        Extract 10 linguistic features

        Returns:
            [
                verse_length_chars,       # int (0-200)
                word_count,               # int (0-20)
                avg_word_length,          # float (1-15)
                has_tanwin,               # 0/1 (تنوين)
                has_shadda,               # 0/1 (شدة)
                has_madd,                 # 0/1 (مد)
                diacritic_ratio,          # float (0-1)
                unique_chars,             # int (10-28)
                alif_count,               # int (0-20)
                waw_count                 # int (0-20)
            ]
        """
        # Implementation using Arabic NLP
```

**Task 3.2: Implement Feature Extractor**
- **Duration**: 2 days
- **File**: `backend/app/ml/feature_extractor.py`
- **Actions**:
  1. Implement `BAHRFeatureExtractor` class (see design above)
  2. Implement each feature category method
  3. Add input validation and error handling
  4. Add feature name documentation

**Task 3.3: Test Feature Extractor**
- **Duration**: 1 day
- **File**: `backend/tests/ml/test_feature_extractor.py`
- **Actions**:
  1. Write unit tests (20+ tests)
  2. Test each feature category independently
  3. Test edge cases (empty text, malformed input)
  4. Test on real verses from golden dataset
  5. Verify feature ranges and data types

- **Success Criteria**:
  - ✅ All 20+ tests passing
  - ✅ Can extract 50 features from any verse
  - ✅ Feature extraction time <100ms per verse
  - ✅ No NaN or Inf values in features

---

### Week 0.2: Data Augmentation (Days 6-10)

**Task 4.1: Design Data Augmentation Strategy**
- **Duration**: 0.5 day
- **Owner**: Prosody + ML Engineer
- **Approach**: Apply valid prosodic transformations to existing verses

**Augmentation Techniques**:

1. **Transformation-based augmentation**:
   - Apply QABD to verses (where valid)
   - Apply KHABN to verses (where valid)
   - Apply IḌMĀR to verses (where valid)
   - Each augmentation preserves meter identity
   - Multiplier: 1.5-2x (471 → ~700-900 verses)

2. **Pattern variation augmentation**:
   - Generate hemistich vs full-verse variations
   - Generate slightly different phonetic realizations
   - Multiplier: 1.2x

3. **Noise injection** (optional):
   - Add small phonetic perturbations (±1 character)
   - Simulate OCR or transcription errors
   - Multiplier: 1.1x

**Total Augmentation**: 471 → ~900 verses (conservative 2x target)

**Task 4.2: Implement Augmentation Pipeline**
- **Duration**: 2 days
- **File**: `backend/app/ml/data_augmenter.py`
- **Actions**:
  ```python
  class DataAugmenter:
      def augment_dataset(self, verses: List[dict], multiplier: float = 2.0) -> List[dict]:
          """
          Augment dataset by applying prosodic transformations

          Args:
              verses: List of verse dicts with 'text' and 'meter'
              multiplier: Target dataset size multiplier

          Returns:
              Augmented dataset (original + synthetic)
          """
          augmented = verses.copy()

          for verse in verses:
              # Try each transformation
              for transform in [apply_qabd, apply_khabn, apply_idmar]:
                  try:
                      new_verse = transform(verse)
                      if is_valid_augmentation(new_verse, verse):
                          augmented.append(new_verse)
                  except:
                      continue

              if len(augmented) >= len(verses) * multiplier:
                  break

          return augmented
  ```

**Task 4.3: Validate Augmented Data**
- **Duration**: 1 day
- **Actions**:
  1. Generate augmented dataset
  2. Manually review 50 random augmented verses
  3. Verify meter labels are correct
  4. Verify phonetic patterns are valid
  5. Check for duplicates or near-duplicates

**Task 4.4: Create Train/Test Split**
- **Duration**: 0.5 day
- **Actions**:
  1. Split original 471 verses: 377 train (80%), 94 test (20%)
  2. Apply augmentation ONLY to train set: 377 → ~720 verses
  3. Keep test set pure (no augmentation): 94 verses
  4. Save splits:
     - `dataset/ml/train.jsonl` (720 verses)
     - `dataset/ml/test.jsonl` (94 verses)

- **Success Criteria**:
  - ✅ Train set: ~720 verses (augmented)
  - ✅ Test set: 94 verses (pure, unseen)
  - ✅ No data leakage (test verses not in train)
  - ✅ Meter distribution similar in train/test

---

### Week 0.2: Fix Transformation Bugs (Days 6-8, PARALLEL with augmentation)

**Task 5.1: Fix QABD Pattern Bugs**
- **Duration**: 1 day
- **Owner**: Prosody Engineer
- **Files**: `backend/app/core/prosody/zihafat.py`, tests
- **Issues**: 4 failing tests with pattern mismatches
- **Actions**:
  1. Debug why `/oo/o` becomes `//o/o/o` (madd representation)
  2. Standardize phonetic pattern generation
  3. Fix QABD transformation logic
  4. Re-run tests, confirm all passing

**Task 5.2: Fix KHABN Pattern Bugs**
- **Duration**: 0.5 day
- **Issues**: 3 failing tests with extra "/" characters
- **Actions**:
  1. Debug pattern normalization
  2. Fix KHABN transformation logic
  3. Re-run tests

**Task 5.3: Fix IḌMĀR Pattern Bugs**
- **Duration**: 0.5 day
- **Issues**: 3 failing tests with pattern length mismatches
- **Actions**:
  1. Debug ḥaraka removal logic
  2. Fix IḌMĀR transformation
  3. Re-run tests

- **Success Criteria**:
  - ✅ All 39 ziḥāfāt tests passing (100%)
  - ✅ Pattern representation consistent across all transformations
  - ✅ No regressions in other test suites

---

### Gap Closure Checkpoint (End of Week 0.2)

**Expected State**:
- ✅ ML libraries installed and verified
- ✅ Hybrid detector achieving ≥50% accuracy (baseline restored)
- ✅ Feature extractor implemented and tested (50 features)
- ✅ Training data: 720 augmented verses
- ✅ Test data: 94 pure verses
- ✅ All transformation tests passing (100%)

**Decision Point**: ✅ **READY to proceed to ML implementation**

---

## Phase 1: ML Implementation (4 weeks)

### Week 1: Baseline Models & Feature Engineering (Days 1-7)

#### Day 1-2: Feature Generation

**Task 1.1: Generate Feature Matrix for Training Data**
- **Duration**: 1 day
- **Actions**:
  ```python
  from app.ml.feature_extractor import BAHRFeatureExtractor
  import pandas as pd

  # Load training data
  verses = load_jsonl('dataset/ml/train.jsonl')  # 720 verses

  # Extract features
  extractor = BAHRFeatureExtractor()
  X = []
  y = []

  for verse in verses:
      features = extractor.extract_features(verse['text'])
      X.append(features)
      y.append(verse['meter'])

  # Save feature matrix
  df = pd.DataFrame(X, columns=extractor.feature_names)
  df['meter'] = y
  df.to_csv('dataset/ml/train_features.csv', index=False)
  ```

- **Deliverable**: `dataset/ml/train_features.csv` (720 rows × 51 columns)

**Task 1.2: Generate Feature Matrix for Test Data**
- **Duration**: 0.5 day
- **Actions**: Same as above for test set (94 verses)
- **Deliverable**: `dataset/ml/test_features.csv` (94 rows × 51 columns)

**Task 1.3: Feature Analysis**
- **Duration**: 0.5 day
- **Notebook**: `notebooks/01_feature_analysis.ipynb`
- **Actions**:
  1. Load feature matrices
  2. Compute feature statistics (mean, std, min, max)
  3. Plot feature distributions (histograms)
  4. Compute feature correlations (correlation matrix)
  5. Identify highly correlated features (>0.9)
  6. Check for constant or near-constant features

- **Deliverable**: Feature analysis report with recommendations for feature selection

---

#### Day 3-4: Baseline Models

**Task 2.1: Train Logistic Regression Baseline**
- **Duration**: 0.5 day
- **Notebook**: `notebooks/02_baseline_models.ipynb`
- **Actions**:
  ```python
  from sklearn.linear_model import LogisticRegression
  from sklearn.preprocessing import StandardScaler
  from sklearn.metrics import accuracy_score, classification_report

  # Load data
  X_train, y_train = load_features('dataset/ml/train_features.csv')
  X_test, y_test = load_features('dataset/ml/test_features.csv')

  # Standardize features
  scaler = StandardScaler()
  X_train_scaled = scaler.fit_transform(X_train)
  X_test_scaled = scaler.transform(X_test)

  # Train model
  model = LogisticRegression(max_iter=1000, multi_class='multinomial')
  model.fit(X_train_scaled, y_train)

  # Evaluate
  y_pred = model.predict(X_test_scaled)
  accuracy = accuracy_score(y_test, y_pred)
  print(f"Logistic Regression Accuracy: {accuracy:.2%}")
  ```

- **Expected Performance**: 55-65% (simple baseline)

**Task 2.2: Train Random Forest**
- **Duration**: 0.5 day
- **Actions**:
  ```python
  from sklearn.ensemble import RandomForestClassifier

  model = RandomForestClassifier(
      n_estimators=100,
      max_depth=10,
      min_samples_split=10,
      random_state=42
  )
  model.fit(X_train, y_train)

  y_pred = model.predict(X_test)
  accuracy = accuracy_score(y_test, y_pred)
  print(f"Random Forest Accuracy: {accuracy:.2%}")
  ```

- **Expected Performance**: 65-75%

**Task 2.3: Analyze Baseline Results**
- **Duration**: 0.5 day
- **Actions**:
  1. Compare LogReg vs Random Forest
  2. Generate confusion matrices
  3. Identify which meters are easiest/hardest
  4. Per-meter accuracy breakdown
  5. Feature importance analysis (from Random Forest)

- **Deliverable**: Baseline model comparison report

---

#### Day 5-7: Advanced Models (XGBoost)

**Task 3.1: Train XGBoost Classifier**
- **Duration**: 1 day
- **Notebook**: `notebooks/03_xgboost_model.ipynb`
- **Actions**:
  ```python
  import xgboost as xgb
  from sklearn.preprocessing import LabelEncoder

  # Encode meter labels
  le = LabelEncoder()
  y_train_encoded = le.fit_transform(y_train)
  y_test_encoded = le.transform(y_test)

  # Train XGBoost
  model = xgb.XGBClassifier(
      n_estimators=200,
      max_depth=6,
      learning_rate=0.1,
      subsample=0.8,
      colsample_bytree=0.8,
      objective='multi:softmax',
      num_class=16,
      eval_metric='mlogloss',
      random_state=42
  )

  model.fit(
      X_train, y_train_encoded,
      eval_set=[(X_test, y_test_encoded)],
      early_stopping_rounds=20,
      verbose=True
  )

  # Predict
  y_pred_encoded = model.predict(X_test)
  y_pred = le.inverse_transform(y_pred_encoded)

  accuracy = accuracy_score(y_test, y_pred)
  print(f"XGBoost Accuracy: {accuracy:.2%}")
  ```

- **Expected Performance**: 75-85%

**Task 3.2: Hyperparameter Tuning**
- **Duration**: 1 day
- **Actions**:
  ```python
  from sklearn.model_selection import GridSearchCV

  param_grid = {
      'max_depth': [4, 6, 8],
      'learning_rate': [0.05, 0.1, 0.2],
      'n_estimators': [100, 200, 300],
      'subsample': [0.7, 0.8, 0.9],
      'colsample_bytree': [0.7, 0.8, 0.9]
  }

  grid_search = GridSearchCV(
      xgb.XGBClassifier(objective='multi:softmax', num_class=16),
      param_grid,
      cv=5,
      scoring='accuracy',
      n_jobs=-1,
      verbose=2
  )

  grid_search.fit(X_train, y_train_encoded)

  print(f"Best params: {grid_search.best_params_}")
  print(f"Best CV accuracy: {grid_search.best_score_:.2%}")
  ```

- **Deliverable**: Best hyperparameters + tuned model

**Task 3.3: 5-Fold Cross-Validation**
- **Duration**: 0.5 day
- **Actions**:
  ```python
  from sklearn.model_selection import cross_val_score

  scores = cross_val_score(
      model, X_train, y_train_encoded,
      cv=5,
      scoring='accuracy',
      n_jobs=-1
  )

  print(f"Cross-validation accuracy: {scores.mean():.2%} ± {scores.std():.2%}")
  ```

- **Success Criteria**: Std <5% (stable model)

---

### Week 2: Model Evaluation & Refinement (Days 8-14)

#### Day 8-9: Comprehensive Evaluation

**Task 4.1: Detailed Performance Analysis**
- **Duration**: 1 day
- **Notebook**: `notebooks/04_model_evaluation.ipynb`
- **Actions**:
  1. **Confusion Matrix**:
     ```python
     from sklearn.metrics import confusion_matrix
     import seaborn as sns

     cm = confusion_matrix(y_test, y_pred)
     sns.heatmap(cm, annot=True, fmt='d',
                 xticklabels=le.classes_,
                 yticklabels=le.classes_)
     plt.title('Confusion Matrix')
     plt.savefig('docs/ml/confusion_matrix.png')
     ```

  2. **Per-Meter Accuracy**:
     ```python
     from sklearn.metrics import classification_report

     report = classification_report(y_test, y_pred,
                                    target_names=le.classes_,
                                    output_dict=True)

     # Sort by F1-score
     sorted_meters = sorted(report.items(),
                           key=lambda x: x[1].get('f1-score', 0),
                           reverse=True)
     ```

  3. **Top-3 Accuracy**:
     ```python
     # Get top-3 predictions
     y_proba = model.predict_proba(X_test)
     top3_preds = np.argsort(y_proba, axis=1)[:, -3:]

     # Check if true label in top-3
     top3_correct = 0
     for i, true_label in enumerate(y_test_encoded):
         if true_label in top3_preds[i]:
             top3_correct += 1

     top3_accuracy = top3_correct / len(y_test)
     print(f"Top-3 Accuracy: {top3_accuracy:.2%}")
     ```

- **Expected Results**:
  - Top-1 accuracy: 75-85%
  - Top-3 accuracy: 90-95%
  - Per-meter: Most meters ≥70%

**Task 4.2: Error Analysis**
- **Duration**: 1 day
- **Actions**:
  1. Identify all misclassified verses (20-25% of test set)
  2. Manually review 20 random misclassifications
  3. Categorize errors:
     - Meter confusion (similar patterns)
     - Data quality issues (wrong labels?)
     - Feature gaps (missing important features?)
     - Model limitations
  4. Document error patterns

- **Deliverable**: Error analysis report with improvement recommendations

---

#### Day 10-12: Model Refinement

**Task 5.1: Feature Engineering Iteration**
- **Duration**: 1 day
- **Actions** (based on error analysis):
  1. Add new features if gaps identified
  2. Remove low-importance features
  3. Try feature transformations (log, polynomial)
  4. Re-train model with refined features
  5. Compare performance

**Task 5.2: Ensemble Methods**
- **Duration**: 1 day
- **Actions**:
  ```python
  from sklearn.ensemble import VotingClassifier

  # Ensemble: XGBoost + RandomForest + LogReg
  ensemble = VotingClassifier(
      estimators=[
          ('xgb', xgb_model),
          ('rf', rf_model),
          ('lr', lr_model)
      ],
      voting='soft'  # Use predicted probabilities
  )

  ensemble.fit(X_train_scaled, y_train)
  y_pred_ensemble = ensemble.predict(X_test_scaled)

  accuracy = accuracy_score(y_test, y_pred_ensemble)
  print(f"Ensemble Accuracy: {accuracy:.2%}")
  ```

- **Expected**: +2-5% improvement over single model

**Task 5.3: Confidence Calibration**
- **Duration**: 1 day
- **Actions**:
  ```python
  from sklearn.calibration import CalibratedClassifierCV

  # Calibrate probabilities
  calibrated = CalibratedClassifierCV(model, method='isotonic', cv=5)
  calibrated.fit(X_train, y_train_encoded)

  # Check calibration
  y_proba_calibrated = calibrated.predict_proba(X_test)

  # Reliability diagram
  from sklearn.calibration import calibration_curve

  for meter_idx in range(16):
      prob_true, prob_pred = calibration_curve(
          y_test_encoded == meter_idx,
          y_proba_calibrated[:, meter_idx],
          n_bins=10
      )
      plt.plot(prob_pred, prob_true, marker='o')

  plt.plot([0, 1], [0, 1], 'k--')  # Perfect calibration
  plt.xlabel('Predicted Probability')
  plt.ylabel('True Probability')
  plt.title('Calibration Curve')
  ```

---

#### Day 13-14: Model Selection & Documentation

**Task 6.1: Final Model Selection**
- **Duration**: 0.5 day
- **Actions**:
  1. Compare all models (LogReg, RF, XGBoost, Ensemble)
  2. Select best based on:
     - Top-1 accuracy (weight: 50%)
     - Top-3 accuracy (weight: 20%)
     - Per-meter balance (weight: 20%)
     - Inference speed (weight: 10%)
  3. Finalize hyperparameters

**Task 6.2: Model Documentation**
- **Duration**: 1 day
- **File**: `docs/ml/MODEL_CARD.md`
- **Content**:
  ```markdown
  # BAHR ML Model Card

  ## Model Details
  - Model Type: XGBoost Multi-class Classifier
  - Version: 1.0
  - Training Date: 2025-11-XX
  - Framework: XGBoost 1.7.x, scikit-learn 1.3.x

  ## Intended Use
  - Arabic poetry meter classification
  - 16-class classification (16 canonical meters)
  - Input: Arabic verse text (vocalized)
  - Output: Meter label + confidence score

  ## Training Data
  - Total: 720 verses (471 original + augmentation)
  - Test: 94 verses (held out)
  - Source: Golden dataset v1.3 with augmentation
  - Augmentation: Prosodic transformations (2x)

  ## Performance
  - Top-1 Accuracy: XX.X%
  - Top-3 Accuracy: XX.X%
  - Cross-validation: XX.X% ± X.X%
  - Per-meter accuracy: See detailed breakdown

  ## Hyperparameters
  - max_depth: X
  - learning_rate: X.XX
  - n_estimators: XXX
  - subsample: X.X
  - colsample_bytree: X.X

  ## Features
  - Total: 50 features
  - Categories: Pattern (8), Similarity (16), Rule (16), Linguistic (10)
  - See feature_extractor.py for details

  ## Limitations
  - Trained primarily on classical poetry
  - Performance may degrade on modern poetry
  - Requires vocalized text for best results
  - Limited by training data size (720 verses)

  ## Ethical Considerations
  - Academic/educational use
  - Not for cultural appropriation
  - Respects Arabic literary heritage
  ```

---

### Week 3: Integration & Deployment (Days 15-21)

#### Day 15-17: Hybrid Detector v3 Implementation

**Task 7.1: Design BahrDetectorV3 Architecture**
- **Duration**: 0.5 day
- **File**: `backend/app/core/prosody/detector_v3.py`
- **Architecture**:
  ```
  Input: Arabic verse text
    ↓
  Stage 1: Rule-based filtering
    - Extract phonetic pattern
    - Generate top-3 meter candidates (rule-based)
    - Compute similarity scores
    - If similarity >95% → Return (high confidence)
    ↓
  Stage 2: ML disambiguation
    - Extract 50 features
    - Run XGBoost classifier
    - Get top-3 predictions + probabilities
    ↓
  Stage 3: Confidence fusion
    - Combine rule confidence + ML confidence
    - Final confidence = 0.6 * ML + 0.4 * Rule
    - Return final prediction
    ↓
  Output: {
    'meter': 'الطويل',
    'confidence': 0.89,
    'ml_confidence': 0.92,
    'rule_confidence': 0.85,
    'top_3': ['الطويل', 'البسيط', 'الكامل'],
    'explainability': {...}
  }
  ```

**Task 7.2: Implement BahrDetectorV3**
- **Duration**: 2 days
- **Actions**:
  ```python
  class BahrDetectorV3:
      def __init__(self, model_path: str):
          self.ml_model = joblib.load(model_path)
          self.feature_extractor = BAHRFeatureExtractor()
          self.rule_detector = BahrDetectorV2()  # Existing rule-based

      def detect(self, verse_text: str) -> dict:
          # Stage 1: Rule-based filtering
          rule_result = self.rule_detector.detect(verse_text)

          # High-confidence rule match → return early
          if rule_result['confidence'] > 0.95:
              return {
                  'meter': rule_result['meter'],
                  'confidence': rule_result['confidence'],
                  'method': 'rule_based',
                  'ml_confidence': None,
                  'rule_confidence': rule_result['confidence']
              }

          # Stage 2: ML classification
          features = self.feature_extractor.extract_features(verse_text)
          ml_proba = self.ml_model.predict_proba([features])[0]
          ml_pred = self.ml_model.predict([features])[0]

          # Get top-3 predictions
          top3_idx = np.argsort(ml_proba)[-3:][::-1]
          top3_meters = [self.ml_model.classes_[i] for i in top3_idx]
          top3_probs = [ml_proba[i] for i in top3_idx]

          # Stage 3: Confidence fusion
          ml_confidence = ml_proba[ml_pred]
          rule_confidence = rule_result.get('confidence', 0.5)
          final_confidence = 0.6 * ml_confidence + 0.4 * rule_confidence

          return {
              'meter': top3_meters[0],
              'confidence': final_confidence,
              'ml_confidence': ml_confidence,
              'rule_confidence': rule_confidence,
              'top_3': top3_meters,
              'top_3_probs': top3_probs,
              'method': 'hybrid_ml',
              'explainability': self._explain(verse_text, features, ml_pred)
          }

      def _explain(self, text: str, features: np.ndarray, prediction: int) -> dict:
          # Feature importance for this prediction
          feature_importance = self.ml_model.feature_importances_
          top_features_idx = np.argsort(feature_importance)[-10:][::-1]

          return {
              'top_features': [
                  (self.feature_extractor.feature_names[i],
                   features[i],
                   feature_importance[i])
                  for i in top_features_idx
              ],
              'transformations': self._detect_transformations(text),
              'pattern': text_to_phonetic_pattern(text)
          }
  ```

**Task 7.3: Write Tests for DetectorV3**
- **Duration**: 1 day
- **File**: `backend/tests/core/prosody/test_detector_v3.py`
- **Tests**:
  1. Test initialization (model loading)
  2. Test rule-based early return (high confidence)
  3. Test ML classification path
  4. Test confidence fusion
  5. Test top-3 predictions
  6. Test explainability
  7. Test edge cases (empty text, malformed input)
  8. Integration test with real verses

- **Success Criteria**: 20+ tests passing

---

#### Day 18-19: Model Deployment

**Task 8.1: Save Production Model**
- **Duration**: 0.5 day
- **Actions**:
  ```python
  import joblib
  from datetime import datetime

  # Save model
  model_info = {
      'model': best_model,
      'label_encoder': label_encoder,
      'scaler': scaler,
      'feature_extractor': feature_extractor,
      'metadata': {
          'version': '1.0',
          'train_date': datetime.now().isoformat(),
          'train_size': 720,
          'test_accuracy': test_accuracy,
          'hyperparameters': best_params
      }
  }

  joblib.dump(model_info, 'backend/app/models/bahr_ml_v1.pkl')
  ```

**Task 8.2: Implement Model Loading**
- **Duration**: 0.5 day
- **Actions**:
  1. Lazy loading on first use
  2. Model caching (don't reload every request)
  3. Version checking
  4. Fallback to rule-based if model fails

**Task 8.3: Performance Benchmarking**
- **Duration**: 1 day
- **Actions**:
  ```python
  import time

  # Benchmark feature extraction
  times_extract = []
  for verse in test_verses:
      start = time.time()
      features = extractor.extract_features(verse['text'])
      times_extract.append(time.time() - start)

  print(f"Feature extraction: {np.mean(times_extract)*1000:.2f}ms ± {np.std(times_extract)*1000:.2f}ms")

  # Benchmark ML inference
  times_inference = []
  for features in feature_vectors:
      start = time.time()
      pred = model.predict([features])
      times_inference.append(time.time() - start)

  print(f"ML inference: {np.mean(times_inference)*1000:.2f}ms ± {np.std(times_inference)*1000:.2f}ms")

  # Total end-to-end
  total_time = np.mean(times_extract) + np.mean(times_inference)
  print(f"Total per verse: {total_time*1000:.2f}ms")
  ```

- **Target**: <150ms per verse (feature extraction + inference)

---

#### Day 20-21: Documentation & Validation

**Task 9.1: Write ML Training Guide**
- **Duration**: 1 day
- **File**: `docs/ml/ML_TRAINING_GUIDE.md`
- **Content**:
  ```markdown
  # BAHR ML Training Guide

  ## Prerequisites
  - Python 3.8+
  - Required packages: scikit-learn, pandas, numpy, xgboost
  - Training data: dataset/ml/train.jsonl

  ## Step 1: Feature Extraction
  ```bash
  python scripts/extract_features.py \
    --input dataset/ml/train.jsonl \
    --output dataset/ml/train_features.csv
  ```

  ## Step 2: Model Training
  ```bash
  python scripts/train_model.py \
    --features dataset/ml/train_features.csv \
    --output backend/app/models/bahr_ml_v1.pkl \
    --model xgboost \
    --cv 5
  ```

  ## Step 3: Evaluation
  ```bash
  python scripts/evaluate_model.py \
    --model backend/app/models/bahr_ml_v1.pkl \
    --test dataset/ml/test_features.csv \
    --output docs/ml/evaluation_report.md
  ```

  ## Hyperparameter Tuning
  Edit `config/ml_config.yaml`:
  ```yaml
  xgboost:
    max_depth: 6
    learning_rate: 0.1
    n_estimators: 200
    subsample: 0.8
    colsample_bytree: 0.8
  ```

  ## Retraining with New Data
  1. Add new verses to `dataset/ml/train.jsonl`
  2. Re-run feature extraction
  3. Re-train model
  4. Validate on test set
  5. If accuracy improves, deploy new model
  ```

**Task 9.2: Final Validation**
- **Duration**: 1 day
- **Actions**:
  1. Run DetectorV3 on full golden dataset (471 verses)
  2. Compare vs baselines:
     - Empirical: 50.3%
     - Theoretical: 6.6%
     - Hybrid (old): 41.19%
     - **DetectorV3 (new)**: Target ≥80%
  3. Generate final accuracy report
  4. Per-meter breakdown
  5. Confusion matrix
  6. Error analysis

- **Deliverable**: `docs/ml/FINAL_VALIDATION_REPORT.md`

---

### Week 4: Production Readiness & Refinement (Days 22-28)

#### Day 22-23: API Integration

**Task 10.1: Update API Endpoints**
- **Duration**: 1 day
- **File**: `backend/app/api/routes.py`
- **Actions**:
  1. Add `/api/v3/detect` endpoint for DetectorV3
  2. Keep `/api/v2/detect` for backward compatibility
  3. Add model info endpoint: `/api/ml/model_info`
  4. Add explainability endpoint: `/api/v3/explain`

**Task 10.2: API Testing**
- **Duration**: 1 day
- **Actions**:
  1. Test all endpoints with curl/Postman
  2. Test with various verse lengths
  3. Test error handling (malformed input)
  4. Load testing (100 requests/second)

---

#### Day 24-25: Explainability Enhancement

**Task 11.1: Implement SHAP Values (Optional)**
- **Duration**: 1 day
- **Actions**:
  ```python
  import shap

  # Create SHAP explainer
  explainer = shap.TreeExplainer(model)

  # Explain single prediction
  shap_values = explainer.shap_values(features)

  # Visualize
  shap.summary_plot(shap_values, features,
                    feature_names=feature_names)
  ```

- **Note**: Optional if time permits, provides per-prediction feature contributions

**Task 11.2: Rule-Based Explanation Integration**
- **Duration**: 1 day
- **Actions**:
  1. Show detected transformations (QABD, KHABN, etc.)
  2. Show similarity scores to all 16 meters
  3. Show top-3 alternative meters
  4. Format explanations for end users

---

#### Day 26-27: Performance Optimization

**Task 12.1: Profile and Optimize**
- **Duration**: 1 day
- **Actions**:
  1. Profile feature extraction (identify bottlenecks)
  2. Optimize slow features (caching, vectorization)
  3. Batch inference for multiple verses
  4. Model quantization (optional, for size reduction)

**Task 12.2: Caching Strategy**
- **Duration**: 1 day
- **Actions**:
  1. Cache phonetic pattern extraction
  2. Cache feature extraction (keyed by verse hash)
  3. Cache ML predictions (for repeated queries)
  4. LRU cache with 1000 entry limit

---

#### Day 28: Final Documentation & Completion

**Task 13.1: Write Completion Report**
- **Duration**: 1 day
- **File**: `docs/ml/ML_COMPLETION_REPORT.md`
- **Content**:
  ```markdown
  # BAHR Phase 3: ML Implementation Completion Report

  ## Summary
  - Start Date: YYYY-MM-DD
  - Completion Date: YYYY-MM-DD
  - Duration: 6.5 weeks (2 weeks gap closure + 4.5 weeks ML)

  ## Objectives
  - ✅ Achieve 80-85% Top-1 accuracy
  - ✅ Implement hybrid rule + ML detector
  - ✅ Create explainable predictions
  - ✅ Production-ready deployment

  ## Results
  - Final Top-1 Accuracy: XX.X%
  - Final Top-3 Accuracy: XX.X%
  - Improvement over baseline: +XX.X percentage points
  - Inference time: XXms per verse

  ## Deliverables
  - ✅ BahrDetectorV3 implemented and tested
  - ✅ ML model trained and deployed
  - ✅ Feature extractor (50 features)
  - ✅ Data augmentation pipeline
  - ✅ Comprehensive documentation
  - ✅ API endpoints updated

  ## Performance Comparison
  | Method | Top-1 | Top-3 | Notes |
  |--------|-------|-------|-------|
  | Empirical baseline | 50.3% | 63.5% | Phase 2 |
  | Theoretical | 6.6% | 22.5% | Phase 2 |
  | Hybrid (old) | 41.19% | N/A | Phase 3 Week 10 |
  | **DetectorV3 (ML)** | **XX.X%** | **XX.X%** | **Phase 3 Final** |

  ## Lessons Learned
  - Data augmentation crucial for small datasets
  - XGBoost outperformed simpler models
  - Feature engineering critical for prosodic tasks
  - Hybrid approach better than pure ML

  ## Future Work
  - Collect more training data (target: 2,000+ verses)
  - Experiment with deep learning (LSTM, Transformer)
  - Fine-tune on modern poetry
  - Multi-task learning (meter + rhyme + theme)

  ## Conclusion
  Successfully achieved XX.X% accuracy, exceeding empirical baseline by XX.X percentage points. Production-ready system deployed.
  ```

**Task 13.2: Update Phase 3 Specification**
- **Duration**: 0.5 day
- **File**: `docs/PHASE3_ML_FINAL.md`
- **Actions**:
  1. Mark all ML tasks as completed
  2. Update accuracy metrics
  3. Link to all deliverables

---

## Success Criteria

### Minimum Success (Must Have)

- ✅ Top-1 accuracy ≥80% on golden dataset test set
- ✅ Top-3 accuracy ≥90%
- ✅ All 16 meters have ≥60% accuracy
- ✅ DetectorV3 implemented and tested (20+ tests passing)
- ✅ Inference time <150ms per verse
- ✅ Explainability working (feature importance + rule explanations)

### Target Success (Should Have)

- ✅ Top-1 accuracy ≥85%
- ✅ Top-3 accuracy ≥95%
- ✅ All 16 meters have ≥70% accuracy
- ✅ Inference time <100ms per verse
- ✅ Model documented (training guide + model card)
- ✅ API endpoints updated and tested

### Stretch Goals (Nice to Have)

- ✅ Top-1 accuracy ≥90%
- ✅ SHAP values for per-prediction explanations
- ✅ Ensemble model outperforming single model
- ✅ Batch inference optimization
- ✅ Model versioning and A/B testing framework

---

## Risk Management

### High-Priority Risks

| Risk | Mitigation |
|------|------------|
| **Overfitting (720 verses still small)** | Strong regularization, 5-fold CV, early stopping |
| **Model doesn't beat 80% target** | Ensemble methods, feature engineering, collect more data |
| **Inference too slow (>150ms)** | Feature caching, model optimization, batch inference |

### Medium-Priority Risks

| Risk | Mitigation |
|------|------------|
| **Data augmentation quality** | Manual validation, prosody expert review |
| **Certain meters still <70%** | Class-specific models, weighted loss function |
| **Production deployment issues** | Extensive testing, gradual rollout, fallback to V2 |

---

## Timeline Summary

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| **Gap Closure** | 1.5-2 weeks | Libraries installed, regression fixed, features implemented, data augmented |
| **Week 1: Baseline** | 1 week | Feature matrices, baseline models (LogReg, RF, XGBoost) |
| **Week 2: Evaluation** | 1 week | Model tuning, evaluation, error analysis, refinement |
| **Week 3: Integration** | 1 week | DetectorV3, model deployment, testing |
| **Week 4: Production** | 1 week | API updates, optimization, documentation |

**Total**: 5.5-6.5 weeks from start to production deployment

---

## Appendix: Code Templates

### A1: Feature Extraction Script

```python
# scripts/extract_features.py
import argparse
import json
from pathlib import Path
import pandas as pd
import sys

sys.path.insert(0, 'backend')
from app.ml.feature_extractor import BAHRFeatureExtractor

def main(args):
    # Load verses
    verses = []
    with open(args.input, 'r') as f:
        for line in f:
            verses.append(json.loads(line))

    # Extract features
    extractor = BAHRFeatureExtractor()
    X = []
    y = []

    for verse in verses:
        features = extractor.extract_features(verse['text'])
        X.append(features)
        y.append(verse['meter'])

    # Save to CSV
    df = pd.DataFrame(X, columns=extractor.feature_names)
    df['meter'] = y
    df.to_csv(args.output, index=False)

    print(f"Extracted features for {len(verses)} verses")
    print(f"Saved to {args.output}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    main(args)
```

### A2: Model Training Script

```python
# scripts/train_model.py
import argparse
import pandas as pd
import joblib
import xgboost as xgb
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
import sys

sys.path.insert(0, 'backend')

def main(args):
    # Load data
    df = pd.read_csv(args.features)
    X = df.drop('meter', axis=1).values
    y = df['meter'].values

    # Encode labels
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    # Train model
    model = xgb.XGBClassifier(
        n_estimators=args.n_estimators,
        max_depth=args.max_depth,
        learning_rate=args.learning_rate,
        objective='multi:softmax',
        num_class=len(le.classes_),
        random_state=42
    )

    # Cross-validation
    if args.cv > 0:
        scores = cross_val_score(model, X, y_encoded, cv=args.cv)
        print(f"Cross-validation: {scores.mean():.4f} ± {scores.std():.4f}")

    # Train on full data
    model.fit(X, y_encoded)

    # Save model
    model_info = {
        'model': model,
        'label_encoder': le,
        'feature_names': df.drop('meter', axis=1).columns.tolist()
    }
    joblib.dump(model_info, args.output)
    print(f"Model saved to {args.output}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--features', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--n_estimators', type=int, default=200)
    parser.add_argument('--max_depth', type=int, default=6)
    parser.add_argument('--learning_rate', type=float, default=0.1)
    parser.add_argument('--cv', type=int, default=5)
    args = parser.parse_args()
    main(args)
```

---

**Plan Prepared By**: ML Engineering Team
**Date**: 2025-11-13
**Status**: Ready for execution after gap closure
**Next Review**: End of Week 1 (baseline models)
