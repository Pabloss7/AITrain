import os
import json
import torch
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    BitsAndBytesConfig,
)
from peft import LoraConfig, get_peft_model, TaskType
from trl import SFTTrainer

# Configuration
MODEL_NAME = "google/gemma-3-2b-it" 
OUTPUT_DIR = "./gemma_lora_output"
DATASET_FILE = "train.jsonl"
MAX_SEQ_LENGTH = 1024

def load_dataset(file_path):
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            data.append(json.loads(line))
    # Convert to HuggingFace Dataset
    dataset = Dataset.from_list(data)
    return dataset

def format_instruction(sample):
    # Standard Gemma chat template formatting
    return f"<start_of_turn>user\n{sample['input']}<end_of_turn>\n<start_of_turn>model\n{sample['output']}<end_of_turn>"

def train():
    print(f"Loading dataset from {DATASET_FILE}...")
    dataset = load_dataset(DATASET_FILE)
    
    print(f"Loading model {MODEL_NAME}...")
    
    # Quantization config for efficient training (4-bit)
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
    )

    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        tokenizer.padding_side = "right" # Fix for fp16

        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            quantization_config=bnb_config,
            device_map="auto"
        )
    except Exception as e:
        print(f"Error loading {MODEL_NAME}: {e}")
        print("Please check if the model name is correct and you have access to it.")
        return

    # LoRA Configuration
    peft_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        inference_mode=False,
        r=8,
        lora_alpha=16,
        lora_dropout=0.1,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj"], # Target attention layers
    )
    
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()

    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        logging_steps=10,
        num_train_epochs=3,
        save_strategy="epoch",
        fp16=True,
        optim="paged_adamw_32bit",
    )

    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        peft_config=peft_config,
        max_seq_length=MAX_SEQ_LENGTH,
        tokenizer=tokenizer,
        args=training_args,
        formatting_func=format_instruction,
    )

    print("Starting training...")
    trainer.train()
    
    print(f"Saving model to {OUTPUT_DIR}...")
    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print("Training complete!")

if __name__ == "__main__":
    train()
