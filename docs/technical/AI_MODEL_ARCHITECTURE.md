# 🤖 AI Poetry Generation Model - Architecture Specification
## Phase 2: Deferred Post-MVP (6+ Months)

---

## ⚠️ CRITICAL NOTE

**This document is for PHASE 2 planning only. DO NOT implement during MVP (Weeks 1-14).**

The MVP (Phase 1) focuses exclusively on **rule-based prosody analysis**. AI-powered poetry generation is deferred to Phase 2 (Month 6+) after:
- Proven market demand
- Stable user base (1000+ MAU)
- Revenue stream established
- Dataset of 10,000+ verses collected

See: `docs/planning/DEFERRED_FEATURES.md` for rationale.

---

## 📋 Overview

This document specifies the technical architecture for the **AI Poetry Generation Model** that will power the "الشاعر الذكي" (AI Poet) feature in Phase 2.

**Purpose:** Generate authentic Arabic poetry that follows:
1. Prosodic meter (بحر) constraints
2. Rhyme patterns (قافية)
3. Semantic coherence
4. Stylistic authenticity (classical/modern/dialect)

---

## 🎯 Model Requirements

### Functional Requirements:
```yaml
Input:
  - Bahr (meter) selection: one of 16 classical meters
  - Theme/topic: keyword or brief description
  - Style: classical | modern | dialect
  - Length: 2-30 verses
  - Optional persona: "write like المتنبي"
  - Optional first verse: for continuation

Output:
  - Generated verse(s) in specified meter
  - Confidence score (0.0-1.0)
  - Prosody validation report
  - Alternative generations (top 3)
```

### Non-Functional Requirements:
```yaml
Performance:
  - Generation time: < 5 seconds per verse
  - Throughput: 20 requests/minute
  - Cold start: < 10 seconds

Quality:
  - Meter accuracy: > 85%
  - Human evaluation: > 7/10 for meaning
  - Diversity: distinct n-grams > 70%
  - No plagiarism: BLEU score < 0.3 vs training data

Resource Constraints:
  - GPU memory: < 8GB for inference
  - Model size: < 3GB (quantized)
  - CPU fallback: yes (slower, but functional)
```

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                   User Request                          │
│  {bahr: "الطويل", theme: "الشجاعة", length: 4}        │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              Request Preprocessing                      │
│  - Validate bahr exists                                 │
│  - Expand theme to prompt template                      │
│  - Prepare prosody constraints                          │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│            Base LLM (Fine-Tuned)                        │
│  Model: Jais-13B or AraGPT2-Mega                        │
│  Fine-tuned on 100k+ verses                             │
│  Task: Conditional text generation                      │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│         Prosody-Constrained Decoding                    │
│  - Guided beam search                                   │
│  - Token-level meter validation                         │
│  - Prosody scoring layer                                │
│  - Reject invalid continuations                         │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│           Post-Generation Validation                    │
│  - Full prosody analysis (reuse MVP analyzer)           │
│  - Rhyme consistency check                              │
│  - Semantic coherence check                             │
│  - Plagiarism detection                                 │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              Response to User                           │
│  - Generated verse(s)                                   │
│  - Confidence scores                                    │
│  - Prosody report                                       │
│  - Alternatives (if requested)                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🔬 Model Selection Decision Tree

### Option 1: Jais-13B (Recommended)
```yaml
Pros:
  - State-of-the-art Arabic LLM (Core42, 2023)
  - Pre-trained on 1.3 trillion Arabic tokens
  - Strong performance on generation tasks
  - Open-source (Apache 2.0 license)
  - Active community support

Cons:
  - Large model (13B parameters)
  - Requires GPU for inference (8GB+ VRAM)
  - Slower generation vs smaller models

Inference:
  - Quantization: 4-bit (< 4GB VRAM)
  - Framework: vLLM or HuggingFace Accelerate
  - Hardware: NVIDIA T4/A10 (cloud) or M1 Max (local)

Expected Performance:
  - Generation: 2-4 seconds/verse (A10)
  - Meter accuracy (post fine-tune): 85-90%
  - Semantic quality: 8/10 human eval
```

### Option 2: AraGPT2-Mega (Fallback)
```yaml
Pros:
  - Smaller (1.5B parameters)
  - Faster inference
  - Proven track record
  - Lower resource requirements

Cons:
  - Older architecture (2020)
  - Lower quality vs Jais
  - Limited recent updates

Use Case: CPU-only deployments, cost optimization
```

### Option 3: Custom Transformer (Advanced)
```yaml
Deferred to Phase 3:
  - Train from scratch on poetry corpus
  - Specialized architecture (e.g., prosody-aware attention)
  - Requires significant compute + data
  - Estimated cost: $10k+ GPU hours
```

**Decision:** Start with **Jais-13B fine-tuned**, evaluate, optimize as needed.

---

## 🧠 Fine-Tuning Strategy

### Dataset Preparation

```python
# Dataset Schema (training_data.jsonl)
{
  "text": "قفا نبك من ذكرى حبيب ومنزل",  # The verse
  "bahr": "الطويل",                          # Meter
  "era": "classical",                        # Era
  "poet": "امرؤ القيس",                      # Poet
  "theme": "وقوف على الأطلال",              # Theme
  "taqti3": "فعولن مفاعيلن فعولن مفاعلن",   # Prosody pattern
  "qafiyah": "ل",                            # Rhyme letter
  "quality_score": 0.95                      # Optional: quality rating
}
```

**Collection Strategy:**
- Classical poetry: 50,000 verses (Al-Diwan.net, Adab.com)
- Modern poetry: 30,000 verses (licensed from publishers)
- User-generated: 20,000 verses (with consent)
- Total: 100,000 verses

**Data Splits:**
- Train: 80,000 verses (80%)
- Validation: 10,000 verses (10%)
- Test (hold-out): 10,000 verses (10%)

**Stratification:**
- Ensure all 16 meters represented (min 500 verses/meter)
- Balance classical vs modern (60:40)
- Quality filtering (min score 0.7)

### Fine-Tuning Procedure

```python
# Pseudo-code for fine-tuning process

from transformers import AutoModelForCausalLM, Trainer, TrainingArguments
from peft import LoraConfig, get_peft_model  # Parameter-efficient fine-tuning

# 1. Load base model
base_model = AutoModelForCausalLM.from_pretrained(
    "core42/jais-13b",
    torch_dtype=torch.float16,
    device_map="auto"
)

# 2. Apply LoRA (efficient fine-tuning, 0.1% parameters)
lora_config = LoraConfig(
    r=16,  # Rank
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],  # Which layers to adapt
    lora_dropout=0.05,
    task_type="CAUSAL_LM"
)
model = get_peft_model(base_model, lora_config)

# 3. Prepare dataset
def format_prompt(example):
    """
    Convert dataset entry to training prompt.
    Format: <|bahr|>الطويل<|theme|>الشجاعة<|text|>{verse}<|endoftext|>
    """
    return f"<|bahr|>{example['bahr']}<|theme|>{example['theme']}<|text|>{example['text']}<|endoftext|>"

train_dataset = load_dataset("poetry_corpus.jsonl").map(format_prompt)

# 4. Training arguments
training_args = TrainingArguments(
    output_dir="./jais-poetry-model",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=8,  # Effective batch size: 32
    learning_rate=2e-5,
    num_train_epochs=3,
    warmup_steps=500,
    logging_steps=100,
    save_steps=1000,
    eval_steps=500,
    evaluation_strategy="steps",
    fp16=True,  # Mixed precision training
    report_to="wandb"  # Weights & Biases for tracking
)

# 5. Custom loss function (meter-aware)
class ProsodyAwareLoss:
    def __init__(self, prosody_analyzer, weight=0.2):
        self.analyzer = prosody_analyzer
        self.weight = weight

    def __call__(self, outputs, labels):
        # Standard language modeling loss
        lm_loss = cross_entropy(outputs.logits, labels)

        # Prosody constraint loss (penalize invalid meters)
        generated_text = tokenizer.decode(outputs.logits.argmax(dim=-1))
        prosody_score = self.analyzer.validate_meter(generated_text)
        prosody_loss = 1.0 - prosody_score  # Higher loss for invalid meter

        # Combined loss
        total_loss = lm_loss + (self.weight * prosody_loss)
        return total_loss

# 6. Train
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=compute_poetry_metrics  # Custom metrics
)

trainer.train()

# 7. Save fine-tuned model
model.save_pretrained("./jais-poetry-final")
```

**Training Resources:**
- GPU: 1x NVIDIA A100 (40GB)
- Time: 24-36 hours
- Cost: ~$100-150 (cloud GPU rental)

### Prosody-Constrained Decoding

This is the **key innovation** that ensures generated verses follow meter constraints.

```python
class ProsodyConstrainedDecoder:
    """
    Custom decoder that rejects token candidates violating prosody constraints.
    """

    def __init__(self, model, tokenizer, prosody_analyzer, bahr):
        self.model = model
        self.tokenizer = tokenizer
        self.analyzer = prosody_analyzer
        self.target_bahr = bahr
        self.target_pattern = BAHR_PATTERNS[bahr]  # e.g., "فعولن مفاعيلن..."

    def generate_verse(self, prompt, max_length=50):
        """
        Generate a verse using constrained beam search.
        """
        # Tokenize prompt
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt")

        # Beam search with prosody validation
        beam_outputs = self.model.generate(
            input_ids,
            max_length=max_length,
            num_beams=5,  # Explore 5 alternatives
            num_return_sequences=3,  # Return top 3
            early_stopping=True,
            no_repeat_ngram_size=3,  # Avoid repetition
            temperature=0.8,  # Some randomness for creativity
            top_p=0.9,  # Nucleus sampling
            do_sample=True,
            # Custom constraint
            prefix_allowed_tokens_fn=self._prosody_filter
        )

        # Decode and validate
        candidates = []
        for beam in beam_outputs:
            text = self.tokenizer.decode(beam, skip_special_tokens=True)
            result = self.analyzer.analyze(text)

            if result.detected_meter == self.target_bahr:
                candidates.append({
                    "text": text,
                    "confidence": result.confidence,
                    "prosody_score": result.quality_score
                })

        # Sort by combined score (LM probability + prosody)
        candidates.sort(key=lambda x: x["confidence"] * x["prosody_score"], reverse=True)

        return candidates

    def _prosody_filter(self, batch_id, input_ids):
        """
        Called at each decoding step to filter valid next tokens.

        Returns: List of allowed token IDs
        """
        # Decode current partial generation
        current_text = self.tokenizer.decode(input_ids, skip_special_tokens=True)

        # For each candidate next token, check if it would break prosody
        allowed_tokens = []
        for token_id in range(self.tokenizer.vocab_size):
            candidate_text = current_text + self.tokenizer.decode(token_id)

            # Quick heuristic check (full analysis too slow)
            if self._is_prosody_compatible(candidate_text):
                allowed_tokens.append(token_id)

        return allowed_tokens

    def _is_prosody_compatible(self, partial_text):
        """
        Fast heuristic: check if partial text is compatible with target meter.

        Strategy:
        - Count syllables so far
        - Check if pattern prefix matches target bahr
        - Allow if still compatible (not definitively wrong)
        """
        syllables = self.analyzer.segment_syllables(partial_text)
        current_pattern = self.analyzer.syllables_to_pattern(syllables)

        # Check if current pattern is a valid prefix of target pattern
        return self.target_pattern.startswith(current_pattern)
```

**Trade-offs:**
- **Pros:** Guarantees meter compliance, higher quality
- **Cons:** Slower generation (~2x), may reduce creativity
- **Optimization:** Cache syllable counts, use approximate matching

---

## 📊 Evaluation Framework

### Automatic Metrics

```python
class PoetryEvaluator:
    """
    Comprehensive evaluation of generated poetry.
    """

    def evaluate(self, generated_verses, reference_verses=None):
        metrics = {}

        # 1. Meter Accuracy (most critical)
        meter_correct = 0
        for verse in generated_verses:
            analysis = prosody_analyzer.analyze(verse["text"])
            if analysis.detected_meter == verse["target_bahr"]:
                meter_correct += 1
        metrics["meter_accuracy"] = meter_correct / len(generated_verses)

        # 2. Perplexity (language model quality)
        metrics["perplexity"] = compute_perplexity(model, generated_verses)

        # 3. Diversity (avoid repetition)
        all_text = " ".join([v["text"] for v in generated_verses])
        unique_bigrams = len(set(nltk.bigrams(all_text.split())))
        total_bigrams = len(list(nltk.bigrams(all_text.split())))
        metrics["diversity_bigrams"] = unique_bigrams / total_bigrams

        # 4. Coherence (BERTScore)
        if reference_verses:
            from bert_score import score
            P, R, F1 = score(
                [v["text"] for v in generated_verses],
                [v["text"] for v in reference_verses],
                lang="ar"
            )
            metrics["bert_f1"] = F1.mean().item()

        # 5. Plagiarism Detection (BLEU vs training data)
        from nltk.translate.bleu_score import sentence_bleu
        bleu_scores = []
        for gen_verse in generated_verses:
            # Compare to 1000 random training verses
            sample_train = random.sample(training_data, 1000)
            max_bleu = max([
                sentence_bleu([train["text"]], gen_verse["text"])
                for train in sample_train
            ])
            bleu_scores.append(max_bleu)
        metrics["max_bleu_vs_train"] = max(bleu_scores)

        return metrics
```

**Success Criteria:**
```yaml
Meter Accuracy: > 85%
Perplexity: < 30
Diversity (unique bigrams): > 70%
BERTScore F1: > 0.7
Max BLEU vs Training: < 0.3 (not plagiarized)
```

### Human Evaluation Protocol

```yaml
Setup:
  - Recruit 10 Arabic literature experts
  - Each evaluator rates 50 generated verses
  - Compensation: $50/hour (5 hours total)

Rating Dimensions:
  1. Meter Correctness (binary: موزون/غير موزون)
     - "Is the verse correctly metered?"

  2. Semantic Coherence (1-5 scale)
     - 1: Nonsensical, random words
     - 3: Grammatical, but weak meaning
     - 5: Deep, meaningful, poetic

  3. Linguistic Beauty (1-5 scale)
     - 1: Ugly, awkward phrasing
     - 3: Acceptable, unremarkable
     - 5: Eloquent, evocative, beautiful

  4. Originality (1-5 scale)
     - 1: Cliché, derivative
     - 3: Somewhat original
     - 5: Highly original, creative

  5. Overall Quality (1-10 scale)
     - "Would you publish this in a literature magazine?"

Comparison:
  - Mix generated verses with real classical poetry
  - Evaluators don't know which is which (blind test)
  - Measure: Can AI verses pass as human-written?

Statistical Analysis:
  - Inter-rater reliability (Krippendorff's alpha > 0.7)
  - T-test: AI vs Human quality scores
  - Goal: No statistically significant difference
```

---

## 🚀 Deployment Architecture

### Inference Service

```yaml
Framework: vLLM (optimized LLM serving)
  - Continuous batching (higher throughput)
  - PagedAttention (efficient KV cache)
  - Quantization: 4-bit (via bitsandbytes)

Infrastructure:
  - GPU: NVIDIA A10G (24GB VRAM) - $1.50/hour AWS
  - Auto-scaling: 1-3 instances based on queue length
  - Load balancer: Distribute requests evenly

Cold Start Mitigation:
  - Keep 1 instance always warm
  - Pre-load model weights at startup (30s)
  - Health check: /health endpoint

API Design:
  Endpoint: POST /api/v1/generate
  Request:
    {
      "bahr": "الطويل",
      "theme": "الشجاعة",
      "style": "classical",
      "length": 4,
      "temperature": 0.8
    }
  Response:
    {
      "verses": [
        {"text": "...", "confidence": 0.92},
        {"text": "...", "confidence": 0.88},
        {"text": "...", "confidence": 0.85}
      ],
      "prosody_report": {...},
      "generation_time_ms": 3200
    }

Rate Limiting:
  - Free tier: 5 generations/day
  - Premium: 100 generations/day
  - Enterprise: Unlimited

Cost Estimation:
  - Per generation: $0.01 (GPU + compute)
  - 10,000 generations/month: $100
  - Revenue (Premium users): $4.99 × 100 users = $499
  - Net: $399/month (profitable at small scale)
```

### Model Versioning

```yaml
Strategy: A/B Testing + Gradual Rollout

Version Naming: v{major}.{minor}.{patch}
  - v1.0.0: Initial release (Week 1)
  - v1.1.0: Improved meter accuracy (+5%)
  - v2.0.0: New base model (breaking changes)

Deployment Process:
  1. Train new model version
  2. Evaluate on hold-out test set
  3. If metrics improve:
     a. Deploy to 10% of traffic (canary)
     b. Monitor for 48 hours
     c. If stable, increase to 50%
     d. If still stable, 100% rollout
  4. If metrics regress, rollback instantly

Rollback Procedure:
  - Keep previous model loaded in memory
  - Feature flag: MODEL_VERSION=v1.0.0
  - Switch takes < 1 second (no downtime)

Experiment Tracking:
  - Tool: Weights & Biases
  - Track: Loss curves, metrics, hyperparameters
  - Compare: Model versions side-by-side
```

---

## 🧪 Testing Strategy

### Unit Tests
```python
def test_prosody_constrained_generation():
    """Verify generated verses match requested meter."""
    decoder = ProsodyConstrainedDecoder(model, tokenizer, analyzer, bahr="الطويل")
    result = decoder.generate_verse(prompt="اكتب بيتاً عن الشجاعة")

    assert len(result) > 0, "Should generate at least one candidate"

    for candidate in result:
        analysis = analyzer.analyze(candidate["text"])
        assert analysis.detected_meter == "الطويل", "Meter constraint violated"
        assert analysis.confidence > 0.7, "Low confidence generation"

def test_no_plagiarism():
    """Ensure generated verses are not copied from training data."""
    generated = generate_verse(bahr="الكامل", theme="الطبيعة")

    # Check against all training data (expensive, run nightly)
    for train_verse in training_dataset:
        similarity = compute_bleu(generated, train_verse)
        assert similarity < 0.5, f"Too similar to training data: {train_verse}"

def test_generation_timeout():
    """Ensure generation completes within time limit."""
    import time
    start = time.time()
    result = generate_verse(bahr="الوافر", theme="الحب")
    elapsed = time.time() - start

    assert elapsed < 5.0, f"Generation took too long: {elapsed:.2f}s"
```

### Integration Tests
```python
def test_end_to_end_generation_api():
    """Test full generation pipeline via API."""
    response = client.post("/api/v1/generate", json={
        "bahr": "الطويل",
        "theme": "الوطن",
        "length": 2
    })

    assert response.status_code == 200
    data = response.json()

    assert "verses" in data
    assert len(data["verses"]) == 2
    assert data["prosody_report"]["meter"] == "الطويل"
```

---

## 📈 Performance Optimization

### Quantization
```python
# Reduce model from 26GB (FP16) to 6.5GB (4-bit)
from transformers import BitsAndBytesConfig

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4"
)

model = AutoModelForCausalLM.from_pretrained(
    "jais-poetry-fine-tuned",
    quantization_config=quantization_config
)

# Trade-off: 5-10% quality degradation, but 4x memory savings
```

### Caching
```python
# Cache frequent requests (same bahr + theme)
@lru_cache(maxsize=1000)
def generate_verse_cached(bahr, theme, style):
    # Only cache deterministic generations (temperature=0)
    return generate_verse(bahr, theme, style, temperature=0.0)

# Expiration: 1 hour (Redis)
cache_key = f"gen:{bahr}:{theme}:{style}"
cached_result = redis.get(cache_key)
if cached_result:
    return json.loads(cached_result)
else:
    result = generate_verse(...)
    redis.setex(cache_key, 3600, json.dumps(result))
    return result
```

---

## 🎯 Success Metrics (Phase 2)

```yaml
Month 1 (Post-Launch):
  - Meter Accuracy: > 80%
  - Human Eval: > 6/10
  - Generations/day: > 100
  - User feedback: "interesting but needs work"

Month 3:
  - Meter Accuracy: > 85%
  - Human Eval: > 7/10
  - Generations/day: > 500
  - User feedback: "impressive, useful"

Month 6:
  - Meter Accuracy: > 90%
  - Human Eval: > 8/10
  - Generations/day: > 2000
  - User feedback: "indistinguishable from human"
  - Revenue: $500+/month from Premium users
```

---

## 🔒 Ethical Considerations

```yaml
Attribution:
  - All generated verses labeled as "AI-generated"
  - Users cannot claim AI verses as their own work
  - Academic use: Must cite BAHR platform

Plagiarism Prevention:
  - BLEU check vs training data (< 0.3)
  - If high similarity detected, regenerate
  - Log all generations for audit

Content Moderation:
  - Filter offensive themes (profanity, hate speech)
  - Refuse to generate political/religious extremism
  - Human review of flagged content

Data Privacy:
  - User prompts not used for model training (opt-in only)
  - Generations stored only with user consent
  - GDPR/CCPA compliance
```

---

## 📝 Open Questions (Pre-Phase 2)

```yaml
Q1: Which base model? Jais-13B or AraGPT2?
  - Decision by: End of Month 5 (after MVP evaluation)
  - Criteria: User demand + available budget

Q2: GPU vs CPU inference?
  - If < 100 requests/day: CPU acceptable (slower, cheaper)
  - If > 100 requests/day: GPU required (faster, expensive)

Q3: Training dataset size?
  - Minimum: 50k verses (feasible)
  - Ideal: 100k+ verses (requires licensing deals)

Q4: Fine-tuning budget?
  - Conservative: $100-200 (A100 for 24-48 hours)
  - Aggressive: $500+ (longer training, hyperparameter search)
```

---

## 🚀 Implementation Roadmap (Phase 2)

```yaml
Month 6: Preparation
  - Week 1-2: Dataset collection (license modern poetry)
  - Week 3: Data cleaning + annotation
  - Week 4: Baseline experiment (fine-tune AraGPT2 without constraints)

Month 7: Model Development
  - Week 1-2: Implement prosody-constrained decoding
  - Week 3: Fine-tune Jais-13B with LoRA
  - Week 4: Evaluation + hyperparameter tuning

Month 8: Integration & Testing
  - Week 1: API development + quantization
  - Week 2: Human evaluation study
  - Week 3: Beta testing with 50 users
  - Week 4: Bug fixes + optimizations

Month 9: Launch
  - Week 1: Soft launch (Premium users only)
  - Week 2: Monitor + iterate
  - Week 3: Public launch
  - Week 4: Marketing + user acquisition
```

---

## 📚 References

- [Jais Model Card](https://huggingface.co/core42/jais-13b)
- [Arabic Poetry Generation Survey (2023)](https://arxiv.org/abs/2304.xxxxx)
- [LoRA: Low-Rank Adaptation](https://arxiv.org/abs/2106.09685)
- [vLLM: Fast LLM Serving](https://vllm.ai/)
- [Arabic Prosody Computational Methods](https://scholar.google.com/scholar?q=arabic+prosody+computational)

---

**Last Updated:** November 8, 2025
**Status:** ✅ Specification Complete - Ready for Phase 2
**Priority:** DEFERRED (Month 6+)

**Next Steps:**
1. Complete MVP Phase 1 (meter detection)
2. Validate market demand (1000+ MAU)
3. Secure funding or revenue ($500+/month)
4. Revisit this spec in Month 5
5. Execute Phase 2 roadmap

**Remember:** Don't let "AI poetry generation" distract from MVP core value (prosody analysis). Ship the analyzer first, poetry generation second.
