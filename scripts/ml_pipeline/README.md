# BAHR ML Pipeline - Phase 5→8 Implementation

**Status**: 🚧 In Progress  
**Version**: 1.0  
**Date**: 2025-11-13

## Overview

This directory contains the machine learning pipeline implementation following the expert technical review roadmap. The pipeline transforms BAHR from a rule-based system (100% accuracy) to a production-grade hybrid system with ML models achieving 95%+ accuracy.

## Architecture

```
ml_pipeline/
├── feature_optimization.py      # Phase 5.1: RFE + SHAP analysis
├── hyperparameter_search.py     # Phase 5.2: Grid search for RF/XGBoost/LightGBM
├── ensemble_trainer.py          # Phase 5.3: Weighted voting ensemble
├── sequence_dataset_builder.py  # Phase 6.1: Letter-level sequence data
├── lstm_crf_model.py           # Phase 6.2: BiLSTM-CRF implementation
├── augmentation_pipeline.py     # Phase 6.3: Scale to 5K verses
├── arabert_finetuner.py        # Phase 7: Transfer learning
├── evaluation_suite.py          # Comprehensive metrics
├── Makefile                     # Reproducible pipeline
└── results/                     # Output directory
    ├── feature_analysis.json
    ├── best_params.json
    ├── evaluation_report.json
    └── figures/
```

## Quick Start

### Prerequisites

```bash
# Install base dependencies
pip install -r requirements/ml.txt

# Install ML libraries (optional: XGBoost, LightGBM, PyTorch)
make install-ml-libs
```

### Phase 5: Feature Optimization & Ensemble Training (Quick Path)

Run the complete Phase 5 pipeline in one command:

```bash
make phase5-quick
```

This will:
1. ✅ Extract and optimize features (71 → 45 features)
2. ✅ Tune RandomForest hyperparameters
3. ✅ Train ensemble model
4. ✅ Generate comprehensive evaluation report

**Expected runtime**: ~30-60 minutes (depending on hardware)

### Phase 5: Full Pipeline (All Hyperparameter Tuning)

For complete hyperparameter search across all models:

```bash
make phase5-full
```

**Expected runtime**: ~4-8 hours (includes XGBoost and LightGBM tuning)

## Pipeline Steps (Manual Execution)

### Step 1: Feature Extraction

Extract features from the golden dataset:

```bash
# Using existing training script
python train_baseline_models.py --extract-only

# Or manually
make extract-features
```

**Output**: `data/ml/X_train.npy`, `data/ml/y_train.npy`

### Step 2: Feature Optimization

Run RFE + SHAP analysis to reduce feature count:

```bash
python ml_pipeline/feature_optimization.py \
    --input-X data/ml/X_train.npy \
    --input-y data/ml/y_train.npy \
    --output ml_pipeline/results/feature_analysis.json \
    --target-features 45
```

**Output**:
- `ml_pipeline/results/feature_analysis.json` - Analysis results
- `ml_pipeline/results/optimized_feature_indices.npy` - Selected features
- `ml_pipeline/results/figures/` - Visualizations

**Validation**:
```bash
# Check feature analysis
cat ml_pipeline/results/feature_analysis.json | jq '.optimized_feature_set'
```

### Step 3: Hyperparameter Tuning

#### Quick (RandomForest only):
```bash
python ml_pipeline/hyperparameter_search.py \
    --features data/ml/X_train.npy \
    --targets data/ml/y_train.npy \
    --feature-indices ml_pipeline/results/optimized_feature_indices.npy \
    --output ml_pipeline/results/best_params.json \
    --models rf
```

#### Full (All models):
```bash
python ml_pipeline/hyperparameter_search.py --models all
```

**Output**: `ml_pipeline/results/best_params.json`

### Step 4: Ensemble Training

Train weighted voting ensemble:

```bash
python ml_pipeline/ensemble_trainer.py \
    --features data/ml/X_train.npy \
    --targets data/ml/y_train.npy \
    --feature-indices ml_pipeline/results/optimized_feature_indices.npy \
    --params ml_pipeline/results/best_params.json \
    --output models/ensemble_v1
```

**Output**:
- `models/ensemble_v1/random_forest_model.pkl`
- `models/ensemble_v1/xgboost_model.pkl` (if installed)
- `models/ensemble_v1/lightgbm_model.pkl` (if installed)
- `models/ensemble_v1/ensemble_metadata.json`

### Step 5: Comprehensive Evaluation

Evaluate ensemble with advanced metrics:

```bash
python ml_pipeline/evaluation_suite.py \
    --model models/ensemble_v1 \
    --test-data dataset/evaluation/golden_set_v1_3_with_sari.jsonl \
    --output ml_pipeline/results/evaluation_report.json
```

**Output**:
- `ml_pipeline/results/evaluation_report.json` - Full evaluation metrics
- `ml_pipeline/results/figures/` - Confusion matrices, calibration curves

**Metrics Included**:
- ✅ Top-1, Top-3, Top-5 accuracy
- ✅ Mean Reciprocal Rank (MRR)
- ✅ Expected Calibration Error (ECE)
- ✅ Per-meter Precision/Recall/F1
- ✅ Confidence-accuracy correlation
- ✅ Error taxonomy
- ✅ Confusion matrices

## Phase 6-8: Advanced Models (Future Work)

### Phase 6: BiLSTM-CRF Sequence Modeling

```bash
# Build sequence dataset
python ml_pipeline/sequence_dataset_builder.py \
    --input dataset/evaluation/golden_set_v1_3_with_sari.jsonl \
    --output dataset/ml/sequence_data.pkl

# Train BiLSTM-CRF
python ml_pipeline/lstm_crf_trainer.py \
    --data dataset/ml/sequence_data.pkl \
    --output models/lstm_crf_v1 \
    --epochs 50
```

### Phase 7: AraBERT Transfer Learning

```bash
python ml_pipeline/arabert_finetuner.py \
    --data dataset/ml/augmented_5k.jsonl \
    --output models/arabert_v1 \
    --epochs 10 \
    --freeze-layers 8
```

## Results Validation

### Check Pipeline Status

```bash
make status
```

### Inspect Results

```bash
# Feature analysis summary
cat ml_pipeline/results/feature_analysis.json | jq '.optimized_feature_set'

# Hyperparameter tuning results
cat ml_pipeline/results/best_params.json | jq '.'

# Evaluation summary
cat ml_pipeline/results/evaluation_report.json | jq '{
  accuracy: .overall_accuracy,
  top3: .top_k_accuracy.top_3_accuracy,
  mrr: .mrr,
  ece: .ece
}'

# Per-meter F1 scores
cat ml_pipeline/results/evaluation_report.json | jq '.per_meter_metrics'
```

### Visualizations

Check generated visualizations in `ml_pipeline/results/figures/`:

- `correlation_heatmap.png` - Feature correlation matrix
- `rfecv_curve.png` - Recursive feature elimination curve
- `shap_summary.png` - SHAP feature importance
- `shap_importance_bar.png` - SHAP importance bar chart
- `calibration_curve.png` - Model calibration
- `confidence_analysis.png` - Confidence distribution
- `confusion_matrix.png` - Prediction confusion matrix

## Docker Deployment

### Build Docker Image

```bash
make docker-build
```

### Run Pipeline in Docker

```bash
make docker-run
```

## Troubleshooting

### Issue: XGBoost/LightGBM not installed

**Solution**: These are optional. The pipeline will skip them if not available.

```bash
# Install optionally
pip install xgboost lightgbm
```

### Issue: Out of memory during SHAP analysis

**Solution**: Reduce `--shap-samples` parameter:

```bash
python ml_pipeline/feature_optimization.py --shap-samples 200
```

### Issue: Grid search taking too long

**Solution**: Use quick path or reduce grid size:

```bash
# Use RandomForest only
make tune-rf-only

# Or edit hyperparameter_search.py to reduce param_grid
```

## Performance Targets

| Metric | Baseline (RF) | Target (Ensemble) | Achieved |
|--------|---------------|-------------------|----------|
| Top-1 Accuracy | 93.6% | 95%+ | ⏳ TBD |
| Top-3 Accuracy | ~98% | 99%+ | ⏳ TBD |
| MRR | ~0.95 | 0.98+ | ⏳ TBD |
| ECE | Unknown | <0.05 | ⏳ TBD |
| Per-meter F1 (avg) | ~0.93 | 0.95+ | ⏳ TBD |

## Integration with BAHR API

### Hybrid Detection Strategy

```python
from app.core.prosody.detector_v2 import BahrDetectorV2
from ml_pipeline.ensemble_model import EnsembleDetector

class HybridMeterDetector:
    def __init__(self):
        self.rule_detector = BahrDetectorV2()
        self.ml_detector = EnsembleDetector('models/ensemble_v1')
        
    def detect(self, verse):
        # Step 1: Try rule-based detection
        rule_result = self.rule_detector.detect(verse)
        
        # Step 2: If high confidence, trust rules
        if rule_result.confidence >= 0.95:
            return rule_result
        
        # Step 3: Otherwise, use ML
        ml_result = self.ml_detector.predict(verse)
        
        # Step 4: Weighted fusion
        if rule_result.confidence > 0.7:
            # Trust rules more
            return rule_result if rule_result.confidence > ml_result['confidence'] else ml_result
        else:
            # Trust ML more
            return ml_result
```

## Citation

If you use this ML pipeline, please cite:

```bibtex
@software{bahr_ml_pipeline,
  title={BAHR Arabic Prosody Engine - ML Pipeline},
  author={BAHR Development Team},
  year={2025},
  url={https://github.com/goforwest/BAHR}
}
```

## License

MIT License - See LICENSE file for details

## Contributors

- Lead ML Engineer: [Your Name]
- Arabic Prosody Expert: [Expert Name]
- Software Architect: [Architect Name]

## Support

For issues or questions:
- GitHub Issues: https://github.com/goforwest/BAHR/issues
- Email: [contact email]

---

**Last Updated**: 2025-11-13  
**Pipeline Version**: 1.0  
**BAHR Version**: 0.1.0
