# BAHR ML Pipeline - Makefile
# Reproducible pipeline for model training and evaluation

.PHONY: all install clean train evaluate deploy help

# Default target
all: help

## help: Show this help message
help:
	@echo "BAHR ML Pipeline - Available targets:"
	@echo ""
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ':' |  sed -e 's/^/ /'

## install: Install all dependencies
install:
	pip install --upgrade pip
	pip install -r requirements/ml.txt
	@echo "✅ Dependencies installed"

## install-ml-libs: Install ML-specific libraries (XGBoost, LightGBM, PyTorch)
install-ml-libs:
	pip install xgboost lightgbm
	pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
	pip install torchcrf transformers
	@echo "✅ ML libraries installed"

## extract-features: Extract features from golden dataset
extract-features:
	@echo "Extracting features from golden dataset..."
	python train_baseline_models.py --extract-only
	@echo "✅ Features extracted to data/ml/"

## optimize-features: Run feature optimization (RFE + SHAP)
optimize-features:
	@echo "Running feature optimization..."
	python ml_pipeline/feature_optimization.py \
		--input-X data/ml/X_train.npy \
		--input-y data/ml/y_train.npy \
		--output ml_pipeline/results/feature_analysis.json \
		--target-features 45
	@echo "✅ Feature optimization complete"

## tune-hyperparameters: Run hyperparameter tuning for all models
tune-hyperparameters:
	@echo "Running hyperparameter tuning (this may take several hours)..."
	python ml_pipeline/hyperparameter_search.py \
		--features data/ml/X_train.npy \
		--targets data/ml/y_train.npy \
		--feature-indices ml_pipeline/results/optimized_feature_indices.npy \
		--output ml_pipeline/results/best_params.json \
		--models all
	@echo "✅ Hyperparameter tuning complete"

## tune-rf-only: Quick hyperparameter tuning (RandomForest only)
tune-rf-only:
	@echo "Tuning RandomForest hyperparameters..."
	python ml_pipeline/hyperparameter_search.py \
		--features data/ml/X_train.npy \
		--targets data/ml/y_train.npy \
		--feature-indices ml_pipeline/results/optimized_feature_indices.npy \
		--output ml_pipeline/results/best_params.json \
		--models rf
	@echo "✅ RandomForest tuning complete"

## train-ensemble: Train ensemble model with optimized parameters
train-ensemble:
	@echo "Training ensemble model..."
	python ml_pipeline/ensemble_trainer.py \
		--features data/ml/X_train.npy \
		--targets data/ml/y_train.npy \
		--feature-indices ml_pipeline/results/optimized_feature_indices.npy \
		--params ml_pipeline/results/best_params.json \
		--output models/ensemble_v1
	@echo "✅ Ensemble training complete"

## evaluate-ensemble: Evaluate ensemble on test set
evaluate-ensemble:
	@echo "Running comprehensive evaluation..."
	python ml_pipeline/evaluation_suite.py \
		--model models/ensemble_v1 \
		--test-data dataset/evaluation/golden_set_v1_3_with_sari.jsonl \
		--output ml_pipeline/results/evaluation_report.json
	@echo "✅ Evaluation complete"

## phase5-quick: Quick Phase 5 pipeline (feature optimization + RF tuning + ensemble training)
phase5-quick: optimize-features tune-rf-only train-ensemble evaluate-ensemble
	@echo ""
	@echo "=================================================="
	@echo "✅ Phase 5 Quick Pipeline Complete!"
	@echo "=================================================="
	@echo "Results:"
	@echo "  - Feature analysis: ml_pipeline/results/feature_analysis.json"
	@echo "  - Best parameters: ml_pipeline/results/best_params.json"
	@echo "  - Trained models: models/ensemble_v1/"
	@echo "  - Evaluation: ml_pipeline/results/evaluation_report.json"
	@echo "  - Visualizations: ml_pipeline/results/figures/"
	@echo ""

## phase5-full: Full Phase 5 pipeline (all hyperparameter tuning)
phase5-full: optimize-features tune-hyperparameters train-ensemble evaluate-ensemble
	@echo ""
	@echo "=================================================="
	@echo "✅ Phase 5 Full Pipeline Complete!"
	@echo "=================================================="

## augment-data: Run large-scale data augmentation (target: 5,000 verses)
augment-data:
	@echo "Running large-scale data augmentation..."
	python ml_pipeline/augmentation_pipeline.py \
		--input dataset/evaluation/golden_set_v1_3_with_sari.jsonl \
		--output dataset/ml/augmented_5k.jsonl \
		--target-size 5000
	@echo "✅ Data augmentation complete"

## train-lstm: Train BiLSTM-CRF sequence model
train-lstm:
	@echo "Training BiLSTM-CRF model..."
	python ml_pipeline/lstm_crf_trainer.py \
		--data dataset/ml/augmented_5k.jsonl \
		--output models/lstm_crf_v1 \
		--epochs 50
	@echo "✅ BiLSTM-CRF training complete"

## train-arabert: Fine-tune AraBERT for meter classification
train-arabert:
	@echo "Fine-tuning AraBERT..."
	python ml_pipeline/arabert_finetuner.py \
		--data dataset/ml/augmented_5k.jsonl \
		--output models/arabert_v1 \
		--epochs 10 \
		--freeze-layers 8
	@echo "✅ AraBERT fine-tuning complete"

## clean: Clean generated files
clean:
	rm -rf ml_pipeline/results/figures/*.png
	rm -rf models/ensemble_v1/*
	@echo "✅ Cleaned generated files"

## clean-all: Clean all generated files including data
clean-all: clean
	rm -rf data/ml/*.npy
	rm -rf ml_pipeline/results/*.json
	rm -rf dataset/ml/augmented_*.jsonl
	@echo "✅ Cleaned all generated files"

## test: Run ML pipeline tests
test:
	pytest backend/tests/ml/ -v
	@echo "✅ Tests passed"

## docker-build: Build Docker image for ML pipeline
docker-build:
	docker build -t bahr-ml:latest -f ml_pipeline/Dockerfile .
	@echo "✅ Docker image built"

## docker-run: Run ML pipeline in Docker container
docker-run:
	docker run -v $(PWD)/data:/app/data \
	           -v $(PWD)/models:/app/models \
	           -v $(PWD)/ml_pipeline/results:/app/ml_pipeline/results \
	           bahr-ml:latest make phase5-quick
	@echo "✅ Pipeline run in Docker"

## status: Show pipeline status
status:
	@echo "BAHR ML Pipeline Status"
	@echo "======================="
	@echo ""
	@echo "Data:"
	@if [ -f data/ml/X_train.npy ]; then \
		echo "  ✅ Features extracted"; \
	else \
		echo "  ❌ Features not extracted (run: make extract-features)"; \
	fi
	@echo ""
	@echo "Optimization:"
	@if [ -f ml_pipeline/results/feature_analysis.json ]; then \
		echo "  ✅ Feature optimization complete"; \
	else \
		echo "  ❌ Feature optimization pending (run: make optimize-features)"; \
	fi
	@if [ -f ml_pipeline/results/best_params.json ]; then \
		echo "  ✅ Hyperparameter tuning complete"; \
	else \
		echo "  ❌ Hyperparameter tuning pending (run: make tune-hyperparameters)"; \
	fi
	@echo ""
	@echo "Models:"
	@if [ -d models/ensemble_v1 ] && [ -f models/ensemble_v1/ensemble_metadata.json ]; then \
		echo "  ✅ Ensemble model trained"; \
	else \
		echo "  ❌ Ensemble model not trained (run: make train-ensemble)"; \
	fi
	@echo ""
	@echo "Evaluation:"
	@if [ -f ml_pipeline/results/evaluation_report.json ]; then \
		echo "  ✅ Evaluation complete"; \
	else \
		echo "  ❌ Evaluation pending (run: make evaluate-ensemble)"; \
	fi
	@echo ""
