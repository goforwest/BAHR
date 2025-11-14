# BAHR ML Pipeline - Quick Start Guide

**Get started in 5 minutes**

## Prerequisites

- Python 3.9+
- Virtual environment activated
- Git repository cloned

## Step 1: Validate Setup (1 minute)

```bash
python ml_pipeline/validate_setup.py
```

**Expected output**: ✅ All checks passed

If you see errors, install missing dependencies:

```bash
pip install -r requirements/ml.txt
```

## Step 2: Install Optional ML Libraries (Optional, 5-10 minutes)

For full ensemble capability (XGBoost + LightGBM):

```bash
pip install xgboost lightgbm
```

Skip if you only want RandomForest (faster, still good results).

## Step 3: Extract Features (1-2 minutes)

If you haven't already:

```bash
python train_baseline_models.py
```

This extracts 71 features from 471 verses and saves to `data/ml/`.

## Step 4: Run Quick Pipeline (30-60 minutes)

Execute complete Phase 5 pipeline:

```bash
cd ml_pipeline
make phase5-quick
```

**What it does:**
1. ✅ Feature optimization (71 → 45 features)
2. ✅ Hyperparameter tuning (RandomForest)
3. ✅ Ensemble training
4. ✅ Comprehensive evaluation

**Output directories:**
- `ml_pipeline/results/` - Analysis results and metrics
- `ml_pipeline/results/figures/` - Visualizations
- `models/ensemble_v1/` - Trained models

## Step 5: View Results (30 seconds)

### Check Status

```bash
make status
```

### View Evaluation Report

```bash
# Overall metrics
cat results/evaluation_report.json | jq '{
  accuracy: .overall_accuracy,
  top_3: .top_k_accuracy.top_3_accuracy,
  mrr: .mrr,
  ece: .ece
}'

# Per-meter F1 scores
cat results/evaluation_report.json | jq '.per_meter_metrics | to_entries[] | {meter: .key, f1: .value.f1}'
```

### View Visualizations

Open in browser or image viewer:

```bash
open results/figures/rfecv_curve.png
open results/figures/shap_importance_bar.png
open results/figures/calibration_curve.png
open results/figures/confusion_matrix.png
```

## Alternative: Manual Step-by-Step

If you prefer to run each step individually:

### 1. Feature Optimization

```bash
python feature_optimization.py \
    --input-X ../data/ml/X_train.npy \
    --input-y ../data/ml/y_train.npy \
    --output results/feature_analysis.json \
    --target-features 45
```

**Runtime**: ~5-15 minutes  
**Output**: `results/feature_analysis.json`, `results/optimized_feature_indices.npy`

### 2. Hyperparameter Tuning

```bash
python hyperparameter_search.py \
    --features ../data/ml/X_train.npy \
    --targets ../data/ml/y_train.npy \
    --feature-indices results/optimized_feature_indices.npy \
    --output results/best_params.json \
    --models rf
```

**Runtime**: ~30-60 minutes (RF only)  
**Output**: `results/best_params.json`

### 3. Ensemble Training

```bash
python ensemble_trainer.py \
    --features ../data/ml/X_train.npy \
    --targets ../data/ml/y_train.npy \
    --feature-indices results/optimized_feature_indices.npy \
    --params results/best_params.json \
    --output ../models/ensemble_v1
```

**Runtime**: ~5-10 minutes  
**Output**: `models/ensemble_v1/*.pkl`, `models/ensemble_v1/ensemble_metadata.json`

### 4. Evaluation

```bash
python evaluation_suite.py \
    --model ../models/ensemble_v1 \
    --test-data ../dataset/evaluation/golden_set_v1_3_with_sari.jsonl \
    --output results/evaluation_report.json
```

**Runtime**: ~2-5 minutes  
**Output**: `results/evaluation_report.json`, `results/figures/*.png`

## Troubleshooting

### Issue: "Module not found"

**Solution**: Ensure virtual environment is activated and dependencies installed:

```bash
source .venv/bin/activate  # or your venv path
pip install -r requirements/ml.txt
```

### Issue: "File not found: data/ml/X_train.npy"

**Solution**: Extract features first:

```bash
cd ..  # Go to repo root
python train_baseline_models.py
```

### Issue: "XGBoost not installed" during ensemble training

**Solution**: This is optional. Ensemble will skip XGBoost and use only RandomForest.

To install:
```bash
pip install xgboost lightgbm
```

### Issue: Out of memory during SHAP analysis

**Solution**: Reduce SHAP sample size:

```bash
python feature_optimization.py --shap-samples 200
```

## Next Steps

After running Phase 5:

1. **Review Results**: Check `results/evaluation_report.json` for accuracy metrics
2. **Inspect Errors**: Look at error taxonomy to understand misclassifications
3. **Compare to Baseline**: Current RF baseline is 93.6% - did ensemble improve?
4. **Production Integration**: If satisfied, integrate ensemble into API (see `ML_PIPELINE_IMPLEMENTATION_SUMMARY.md`)

## Performance Expectations

| Metric | Baseline (RF) | Expected (Ensemble) |
|--------|---------------|---------------------|
| Top-1 Accuracy | 93.6% | 94-95% |
| Top-3 Accuracy | ~98% | 99%+ |
| MRR | ~0.95 | 0.96-0.98 |
| ECE | Unknown | <0.05 |
| Inference Time | <50ms | <100ms |

## Support

- **Full Documentation**: `ml_pipeline/README.md`
- **Implementation Summary**: `ML_PIPELINE_IMPLEMENTATION_SUMMARY.md`
- **Expert Review**: See original technical review document
- **Issues**: GitHub Issues

---

**Last Updated**: 2025-11-13  
**Quick Start Version**: 1.0
