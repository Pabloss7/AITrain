# Gemma-2-2B-IT Fine-Tuning & Testing Report

This document outlines the complete process of fine-tuning the `google/gemma-2-2b-it` model for League of Legends coaching, including the challenges faced and the verification steps.

## 1. Preparation
### Dataset
- **Format**: JSONL (`train.jsonl`)
- **Structure**: Each entry contains an `input` (Technical LoL analysis) and an `output` (Actionable coaching advice).
- **Format Technique**: Uses specific prompt tokens: `<start_of_turn>user\n{input}<end_of_turn>\n<start_of_turn>model\n{output}<end_of_turn>`.

### Environment
- **Hardware**: NVIDIA GPU (RTX series recommended for BF16).
- **Environment**: Python Virtual Environment (`.venv`) with `torch`, `transformers`, `peft`, `trl`, and `bitsandbytes`.

## 2. Training Configuration
The training was conducted using the following techniques:
- **4-Bit Quantization**: Using `BitsAndBytesConfig` (NF4) to reduce VRAM usage.
- **LoRA (Low-Rank Adaptation)**: Efficiently fine-tuning only a small subset of parameters (Targets: `q_proj`, `k_proj`, `v_proj`, etc.).
- **SFT (Supervised Fine-Tuning)**: Using `SFTTrainer` for instruction-based learning.

### Precision Fix
During initial runs, a `NotImplementedError` occurred because the trainer was configured for `fp16=True`. Since Gemma models natively use **BFloat16**, attemptings to apply `GradScaler` (required for FP16) to BF16 tensors caused a crash.
- **Solution**: Updated `train_lora.py` to use `bf16=True` and `torch.bfloat16`.

## 3. Training Results
The model was trained for **3 epochs**. Highlights from `trainingResults.md`:
- **Total Runtime**: ~297 seconds (approx. 5 minutes).
- **Final Training Loss**: ~0.506.
- **Mean Token Accuracy**: 93.03%.
- **Final Validation Result**: Training completed successfully with no further technical issues.

| Metric | Value |
| :--- | :--- |
| Train Loss | 0.5062 |
| Epochs | 3 |
| Mean Accuracy | 0.9303 |
| Runtime | 296.9s |

## 4. Testing & Verification
A dedicated inference script `test_lora.py` was used to verify the adapter.

### Inference Setup
- Loads the base `google/gemma-2-2b-it` model in 4-bit.
- Attaches the LoRA weights from `../models/gemma_lora_output`.
- Generates a response based on a sample MID-role analysis.

### Performance Outcome
- **Input**: Analysis of MID role with poor lane scaling and objective pressure.
- **Output**:
  > "As a MID, you are missing easy last-hits under pressure Also, you are not helping to secure vision around objectives.
  > 
  > To improve your gameplay: Don't roam unless your wave is crashed into the enemy tower. Look to cross-map (take tower) if you cannot contest the objective."

The model successfully adopted the coaching persona and formatting expected from the fine-tuning.
