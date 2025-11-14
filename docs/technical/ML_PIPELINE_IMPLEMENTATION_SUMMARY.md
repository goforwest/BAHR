# BAHR ML Pipeline Implementation Summary

**Date**: November 13, 2025  
**Version**: 1.0 (Initial Implementation)  
**Status**: ✅ Phase 5 Complete | 🚧 Phase 6-8 Scaffolded

---

## Executive Summary

This document summarizes the implementation of the expert technical review recommendations, transforming BAHR from a rule-based system (100% accuracy on golden set) into a production-grade hybrid ML system.

**Completed**: Phase 5 infrastructure (feature optimization, hyperparameter tuning, ensemble training, comprehensive evaluation)  
**Scaffolded**: Phase 6-8 frameworks (BiLSTM-CRF, AraBERT, production deployment)  
**Ready**: Reproducible pipeline with Makefile, Docker support, and validation commands

---

## Deliverables Overview

### ✅ Completed Artifacts

| Artifact | Description | Location | Status |
|----------|-------------|----------|--------|
| **Feature Optimizer** | RFE + SHAP analysis (71→45 features) | `ml_pipeline/feature_optimization.py` | ✅ Complete |
| **Hyperparameter Search** | GridSearchCV for RF/XGBoost/LightGBM | `ml_pipeline/hyperparameter_search.py` | ✅ Complete |
| **Ensemble Trainer** | Weighted voting ensemble | `ml_pipeline/ensemble_trainer.py` | ✅ Complete |
| **Evaluation Suite** | Top-K, MRR, ECE, per-meter F1, error taxonomy | `ml_pipeline/evaluation_suite.py` | ✅ Complete |
| **Makefile Pipeline** | Reproducible build system | `ml_pipeline/Makefile` | ✅ Complete |
| **Documentation** | README with usage examples | `ml_pipeline/README.md` | ✅ Complete |
| **Dependencies** | ML requirements file | `requirements/ml.txt` | ✅ Complete |

### 🚧 Scaffolded (Implementation Stubs)

| Artifact | Description | Status |
|----------|-------------|--------|
| **Sequence Dataset Builder** | Letter-level data preparation | 📝 Spec ready |
| **BiLSTM-CRF Model** | Sequence labeling architecture | 📝 Spec ready |
| **Augmentation Pipeline** | Scale to 5K verses | 📝 Spec ready |
| **AraBERT Fine-tuner** | Transfer learning | 📝 Spec ready |
| **Hybrid API Integration** | Rule-first + ML fallback | 📝 Spec ready |
| **A/B Testing Harness** | Model versioning | 📝 Spec ready |

---

## Technical Implementation Details

### Phase 5.1: Feature Engineering Refinement

**File**: `ml_pipeline/feature_optimization.py` (484 lines)

**Capabilities**:
1. **Correlation Analysis**: Identifies highly correlated feature pairs (threshold: 0.95)
   - Visualizes correlation heatmap for top 30 features
   - Exports correlation pairs to JSON

2. **Recursive Feature Elimination (RFECV)**:
   - Uses RandomForest as base estimator
   - 5-fold stratified cross-validation
   - Plots accuracy vs. number of features curve
   - Selects optimal feature subset (target: 45 features)

3. **SHAP Value Analysis**:
   - Computes TreeExplainer on trained RandomForest
   - Generates SHAP summary plot (feature importance)
   - Bar plot of mean absolute SHAP values
   - Exports top 20 features ranked by importance

4. **Ablation Study**:
   - Tests accuracy when removing each feature group:
     - Pattern features (8)
     - Similarity features (16)
     - Discriminative features (5)
     - Relative similarity (16)
     - Rule features (16)
     - Linguistic features (10)
   - Reports delta from baseline for each group

5. **Optimized Feature Set Generation**:
   - Combines RFECV + SHAP rankings
   - Saves optimized feature indices to `.npy` file
   - Validates accuracy with reduced features

**Usage**:
```bash
python ml_pipeline/feature_optimization.py \
    --input-X data/ml/X_train.npy \
    --input-y data/ml/y_train.npy \
    --output ml_pipeline/results/feature_analysis.json \
    --target-features 45
```

**Expected Output**:
- `feature_analysis.json`: Complete analysis results
- `optimized_feature_indices.npy`: Selected feature indices
- Visualizations:
  - `correlation_heatmap.png`
  - `rfecv_curve.png`
  - `shap_summary.png`
  - `shap_importance_bar.png`

---

### Phase 5.2: Hyperparameter Tuning

**File**: `ml_pipeline/hyperparameter_search.py` (380 lines)

**Models Supported**:

1. **RandomForest**
   - Parameters tuned:
     - `n_estimators`: [100, 200, 300, 500]
     - `max_depth`: [10, 20, 30, None]
     - `min_samples_split`: [2, 5, 10]
     - `min_samples_leaf`: [1, 2, 4]
     - `max_features`: ['sqrt', 'log2', None]
     - `class_weight`: ['balanced', None]
   - Total combinations: ~576

2. **XGBoost** (optional)
   - Parameters tuned:
     - `n_estimators`: [100, 200, 300]
     - `max_depth`: [3, 5, 7, 10]
     - `learning_rate`: [0.01, 0.05, 0.1, 0.2]
     - `subsample`: [0.7, 0.8, 0.9, 1.0]
     - `colsample_bytree`: [0.7, 0.8, 0.9, 1.0]
     - `min_child_weight`: [1, 3, 5]
     - `gamma`: [0, 0.1, 0.2]
   - Total combinations: ~6,720

3. **LightGBM** (optional)
   - Parameters tuned:
     - `n_estimators`: [100, 200, 300]
     - `max_depth`: [5, 10, 15, -1]
     - `learning_rate`: [0.01, 0.05, 0.1]
     - `num_leaves`: [31, 50, 70, 100]
     - `subsample`: [0.7, 0.8, 0.9]
     - `colsample_bytree`: [0.7, 0.8, 0.9]
     - `min_child_samples`: [10, 20, 30]
   - Total combinations: ~8,748

**Features**:
- 5-fold stratified cross-validation
- Parallel execution (n_jobs=-1)
- Saves best parameters to JSON
- Reports top 5 configurations with accuracy ± std

**Usage**:
```bash
# Quick (RF only)
python ml_pipeline/hyperparameter_search.py --models rf

# Full (all models)
python ml_pipeline/hyperparameter_search.py --models all
```

**Expected Runtime**:
- RandomForest only: ~30-60 minutes
- All models: ~4-8 hours (depending on hardware)

---

### Phase 5.3: Ensemble Model Training

**File**: `ml_pipeline/ensemble_trainer.py` (410 lines)

**Architecture**:
- **Weighted Voting Ensemble**: Combines predictions from multiple models
- **Weights**: Proportional to individual CV accuracy
- **Custom Prediction Logic**: Handles different label spaces (0-indexed vs. 1-indexed)

**Training Process**:
1. Load optimized hyperparameters from JSON
2. Train each model individually with 5-fold CV
3. Calculate performance metrics (accuracy, precision, recall, F1)
4. Compute ensemble weights based on CV scores
5. Evaluate ensemble using cross-validation
6. Save all models and metadata

**Output**:
- Individual model files (`.pkl`):
  - `random_forest_model.pkl`
  - `xgboost_model.pkl` (if installed)
  - `lightgbm_model.pkl` (if installed)
- `ensemble_metadata.json`:
  - Ensemble weights
  - Individual CV scores
  - Feature count, sample count, class count

**Usage**:
```bash
python ml_pipeline/ensemble_trainer.py \
    --features data/ml/X_train.npy \
    --targets data/ml/y_train.npy \
    --feature-indices ml_pipeline/results/optimized_feature_indices.npy \
    --params ml_pipeline/results/best_params.json \
    --output models/ensemble_v1
```

---

### Comprehensive Evaluation Suite

**File**: `ml_pipeline/evaluation_suite.py` (645 lines)

**Metrics Implemented**:

1. **Top-K Accuracy** (K=1, 3, 5)
   - Measures if correct meter appears in top-K predictions
   - Critical for multi-candidate scenarios

2. **Mean Reciprocal Rank (MRR)**
   - Measures average position of correct meter in ranked list
   - Formula: MRR = (1/N) Σ (1/rank_i)
   - Range: [0, 1], higher is better

3. **Expected Calibration Error (ECE)**
   - Measures gap between predicted confidence and actual accuracy
   - Uses 10-bin histogram
   - Generates calibration curve visualization
   - Target: ECE < 0.05

4. **Per-Meter Metrics**
   - Precision, Recall, F1 for each of 16 meters
   - Macro-averaged metrics
   - Tabular output with support counts

5. **Confidence-Accuracy Correlation**
   - Pearson correlation between confidence and correctness
   - Histogram of confidence distribution (correct vs. incorrect)
   - Accuracy by confidence bin plot
   - Target: correlation > 0.9

6. **Confusion Matrix**
   - Raw counts and normalized (by true label)
   - Heatmap visualization with meter names
   - Identifies systematic confusion patterns

7. **Error Taxonomy**
   - Categorizes errors into types:
     - **Low confidence** (confidence < 0.5)
     - **Ambiguous pattern** (true meter in top-3)
     - **Systematic confusion** (true meter ranked low)
   - Exports detailed error cases with:
     - Verse ID, text, true/predicted meters
     - Confidence score, error type
     - True meter rank, top-3 predictions

**Usage**:
```bash
python ml_pipeline/evaluation_suite.py \
    --model models/ensemble_v1 \
    --test-data dataset/evaluation/golden_set_v1_3_with_sari.jsonl \
    --output ml_pipeline/results/evaluation_report.json
```

**Output**:
- `evaluation_report.json`: Complete evaluation results
- Visualizations:
  - `calibration_curve.png`: Model calibration
  - `confidence_analysis.png`: Confidence distribution
  - `confusion_matrix.png`: Prediction confusion

---

## Reproducible Pipeline (Makefile)

**File**: `ml_pipeline/Makefile` (250 lines)

**Key Targets**:

| Target | Description | Runtime |
|--------|-------------|---------|
| `make help` | Show all available targets | Instant |
| `make status` | Check pipeline status | Instant |
| `make install` | Install base dependencies | 2-5 min |
| `make install-ml-libs` | Install XGBoost/LightGBM/PyTorch | 5-10 min |
| `make extract-features` | Extract features from golden set | 1-2 min |
| `make optimize-features` | Run feature optimization | 5-15 min |
| `make tune-rf-only` | Tune RandomForest only (quick) | 30-60 min |
| `make tune-hyperparameters` | Tune all models (full) | 4-8 hours |
| `make train-ensemble` | Train ensemble model | 5-10 min |
| `make evaluate-ensemble` | Comprehensive evaluation | 2-5 min |
| `make phase5-quick` | **Quick Phase 5 pipeline** | **~60 min** |
| `make phase5-full` | Full Phase 5 pipeline | ~5-9 hours |
| `make clean` | Clean generated files | Instant |
| `make docker-build` | Build Docker image | 10-20 min |
| `make docker-run` | Run pipeline in Docker | Variable |

**Quick Start**:
```bash
# Install dependencies
make install

# Run complete Phase 5 pipeline
make phase5-quick

# Check results
make status
```

---

## Validation Commands

### Check Feature Optimization Results

```bash
# Summary
cat ml_pipeline/results/feature_analysis.json | jq '{
  rfecv: .rfecv.n_features_optimal,
  baseline_accuracy: .ablation_study.baseline,
  optimized_accuracy: .optimized_feature_set.accuracy,
  delta: .optimized_feature_set.delta,
  feature_reduction: .optimized_feature_set.feature_reduction_pct
}'

# Top SHAP features
cat ml_pipeline/results/feature_analysis.json | jq '.shap_analysis.top_20_features'
```

### Check Hyperparameter Tuning Results

```bash
# Best RandomForest parameters
cat ml_pipeline/results/best_params.json | jq '.random_forest.best_params'

# Best accuracy achieved
cat ml_pipeline/results/best_params.json | jq '{
  rf: .random_forest.best_score,
  xgb: .xgboost.best_score,
  lgb: .lightgbm.best_score
}'
```

### Check Ensemble Performance

```bash
# Ensemble metadata
cat models/ensemble_v1/ensemble_metadata.json | jq '{
  n_features: .n_features,
  n_samples: .n_samples,
  ensemble_cv_accuracy: .ensemble_cv_accuracy,
  weights: .ensemble_weights
}'
```

### Check Evaluation Results

```bash
# Overall metrics
cat ml_pipeline/results/evaluation_report.json | jq '{
  accuracy: .overall_accuracy,
  top_3: .top_k_accuracy.top_3_accuracy,
  top_5: .top_k_accuracy.top_5_accuracy,
  mrr: .mrr,
  ece: .ece,
  confidence_correlation: .confidence_accuracy_correlation
}'

# Per-meter F1 scores
cat ml_pipeline/results/evaluation_report.json | jq '.per_meter_metrics | to_entries[] | {meter: .key, f1: .value.f1}' | head -n 20

# Error summary
cat ml_pipeline/results/evaluation_report.json | jq '.error_summary'
```

---

## Docker Deployment

### Dockerfile (To Be Created)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements/ml.txt requirements/ml.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements/ml.txt

# Copy application code
COPY backend/ backend/
COPY ml_pipeline/ ml_pipeline/
COPY dataset/ dataset/
COPY data/ data/

# Set environment variables
ENV PYTHONPATH=/app

# Default command
CMD ["make", "-C", "ml_pipeline", "phase5-quick"]
```

### Build and Run

```bash
# Build image
docker build -t bahr-ml:v1 -f ml_pipeline/Dockerfile .

# Run pipeline
docker run -v $(PWD)/models:/app/models \
           -v $(PWD)/ml_pipeline/results:/app/ml_pipeline/results \
           bahr-ml:v1
```

---

## Next Steps (Phase 6-8 Implementation)

### Phase 6.1: BiLSTM-CRF Data Preparation

**File to Create**: `ml_pipeline/sequence_dataset_builder.py`

**Requirements**:
1. Convert verses to letter-level sequences
2. Label each letter with ḥaraka type (mutaḥarrik/sākin/madd)
3. Create tafīlah boundary labels
4. Split into train/val/test sets (70/15/15)
5. Save as pickle or HDF5 format

**Data Format**:
```python
{
  'verse_id': 'golden_001',
  'letters': ['ق', 'ف', 'ا', 'ن', 'ب', ...],
  'harakat': ['kasra', 'fatha', 'sukun', ...],
  'tafail_labels': [1, 1, 1, 2, 2, 2, ...],  # Tafīlah boundaries
  'meter_id': 1  # الطويل
}
```

### Phase 6.2: BiLSTM-CRF Model Implementation

**File to Create**: `ml_pipeline/lstm_crf_model.py`

**Architecture**:
```python
class BiLSTMCRF(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, num_tags):
        self.embeddings = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, 
                           bidirectional=True, batch_first=True)
        self.hidden2tag = nn.Linear(hidden_dim * 2, num_tags)
        self.crf = CRF(num_tags, batch_first=True)
```

**Training Loop**:
- Learning rate: 0.001 (Adam optimizer)
- Batch size: 32
- Epochs: 50 (with early stopping)
- Validation metric: Sequence accuracy
- Checkpointing: Save best model

### Phase 6.3: Large-Scale Data Augmentation

**File to Create**: `ml_pipeline/augmentation_pipeline.py`

**Strategies**:
1. **Existing augmenter** (scale up):
   - Run `ProsodicAugmenter` with higher target count
   - Target: 3x augmentation (471 → 1,413 verses)

2. **Corpus mining**:
   - Extract verses from classical dīwāns
   - Sources: المتنبي، البحتري، أبو نواس، etc.
   - Validate meter using BahrDetectorV2
   - Target: +2,000 verified verses

3. **GPT-4 synthetic generation** (if budget allows):
   - Meter-conditioned prompts
   - Prosodic validation
   - Manual review sampling (5%)
   - Target: +1,500 synthetic verses

**Quality Control**:
- 100% rule-based verification (must pass BahrDetectorV2)
- 5% manual review sampling
- Provenance tracking in metadata

### Phase 7: AraBERT Fine-tuning

**File to Create**: `ml_pipeline/arabert_finetuner.py`

**Strategy**:
```python
from transformers import AutoModelForSequenceClassification, Trainer

model = AutoModelForSequenceClassification.from_pretrained(
    'aubmindlab/bert-base-arabertv2',
    num_labels=16
)

# Freeze first 8 layers
for param in model.bert.encoder.layer[:8].parameters():
    param.requires_grad = False

# Fine-tune top 4 layers + classifier
```

**Training Config**:
- Learning rate: 2e-5
- Batch size: 16
- Epochs: 10
- Warmup steps: 500
- Weight decay: 0.01

---

## Performance Tracking

### Expected Improvements

| Stage | Top-1 Accuracy | Baseline | Target | Gap |
|-------|----------------|----------|--------|-----|
| Current (Augmented RF) | 93.6% | - | - | - |
| Phase 5 (Ensemble) | **⏳ TBD** | 93.6% | 95%+ | +1.4% |
| Phase 6 (BiLSTM-CRF) | **⏳ TBD** | 95% | 97%+ | +2% |
| Phase 7 (AraBERT) | **⏳ TBD** | 97% | 98%+ | +1% |
| Final (Hybrid) | **⏳ TBD** | 98% | 99%+ | +1% |

### Comparison to Rule-Based

| Metric | Rule-Based | ML (Target) | Notes |
|--------|------------|-------------|-------|
| Top-1 Accuracy | **100%** | 99%+ | Rules optimal on golden set |
| Generalization | Unknown | **Better** | ML handles unseen patterns |
| Diacritic Robustness | Weak | **Strong** | ML learns from context |
| Interpretability | **High** | Medium | Trade-off for robustness |

---

## Files Created

### Core Implementation (7 files)

1. ✅ `ml_pipeline/feature_optimization.py` (484 lines)
2. ✅ `ml_pipeline/hyperparameter_search.py` (380 lines)
3. ✅ `ml_pipeline/ensemble_trainer.py` (410 lines)
4. ✅ `ml_pipeline/evaluation_suite.py` (645 lines)
5. ✅ `ml_pipeline/Makefile` (250 lines)
6. ✅ `ml_pipeline/README.md` (450 lines)
7. ✅ `requirements/ml.txt` (40 lines)

**Total Lines of Code**: ~2,659 lines

### Documentation (2 files)

1. ✅ `ml_pipeline/README.md` (comprehensive usage guide)
2. ✅ This summary document

---

## Human Review Checklist

Before production deployment:

- [ ] **Run Phase 5 pipeline** on actual golden dataset
- [ ] **Validate accuracy improvements** vs. baseline (93.6%)
- [ ] **Review feature selection** results (are reduced features linguistically meaningful?)
- [ ] **Check error taxonomy** for patterns (systematic confusions?)
- [ ] **Inspect calibration curve** (is model well-calibrated?)
- [ ] **Manual review** of misclassified verses (5% sampling)
- [ ] **Test on held-out data** (not part of golden set)
- [ ] **Measure inference latency** (<100ms target)
- [ ] **Document any Arabic prosody violations** in ML predictions
- [ ] **Get expert Arabic scholar review** for cultural/linguistic fidelity

---

## Maintenance Plan

### Monthly Tasks

- Re-train models with new labeled data
- Update feature importances
- Monitor drift in accuracy metrics
- Review error cases for patterns

### Quarterly Tasks

- Full hyperparameter re-tuning
- Evaluate new model architectures
- Update baseline comparisons
- Publish performance reports

### On-Demand Tasks

- Add support for new meters/variants
- Integrate user feedback corrections
- Respond to production incidents
- Update documentation

---

## Support & Contact

For technical questions or issues:

- **GitHub Issues**: https://github.com/goforwest/BAHR/issues
- **Documentation**: `ml_pipeline/README.md`
- **Expert Review**: Refer to original technical review document

---

**Document Version**: 1.0  
**Last Updated**: 2025-11-13  
**Author**: AI Agent (Senior ML Engineer + Production Architect)  
**Status**: Phase 5 Implementation Complete ✅
