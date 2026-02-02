import os
import json
import torch
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
    TrainingArguments,
)
from peft import LoraConfig
from trl import SFTTrainer, SFTConfig
from dotenv import load_dotenv

load_dotenv("../../.env")

# Configuration
MODEL_NAME = "google/gemma-2-2b-it"  # Using Gemma 2 (text-only) instead of Gemma 3 (multimodal)
OUTPUT_DIR = "../models/gemma_lora_output"
DATASET_FILE = "./data/train.jsonl"

def load_jsonl_dataset(file_path):
    """Carga dataset desde archivo JSONL"""
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            data.append(json.loads(line))
    return Dataset.from_list(data)

def formatting_prompts_func(example):
    """
    Formatea un ejemplo individual al formato de chat de Gemma.
    SFTTrainer llama a esta función con batched=False, así que recibe un dict con valores únicos.
    """
    text = f"<start_of_turn>user\n{example['input']}<end_of_turn>\n<start_of_turn>model\n{example['output']}<end_of_turn>"
    return {"text": text}

def train():
    print(f"Loading dataset from {DATASET_FILE}...")
    dataset = load_jsonl_dataset(DATASET_FILE)
    
    print(f"Loading model {MODEL_NAME}...")
    
    # Configuración de cuantización 4-bit
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )

    # Token de Hugging Face
    token = os.getenv("HF_TOKEN")
    
    # Disable image processor warnings for text-only training
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    
    # Cargar tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME, 
        token=token,
        trust_remote_code=True
    )
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    # Cargar modelo (text-only, skip vision components)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        quantization_config=bnb_config,
        device_map="auto",
        token=token,
        trust_remote_code=True,
        attn_implementation="eager",  # Avoid flash attention issues
    )
    
    # Desactivar cache para entrenamiento
    model.config.use_cache = False

    # Configuración LoRA
    peft_config = LoraConfig(
        r=8,
        lora_alpha=16,
        lora_dropout=0.1,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    )

    # Configuración de SFT
    sft_config = SFTConfig(
        output_dir=OUTPUT_DIR,
        num_train_epochs=3,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        logging_steps=10,
        fp16=True,
        optim="paged_adamw_32bit",
        save_strategy="epoch",
        warmup_steps=10,
        packing=False,
    )

    # Crear trainer
    trainer = SFTTrainer(
        model=model,
        args=sft_config,
        train_dataset=dataset,
        peft_config=peft_config,
        formatting_func=formatting_prompts_func,
    )

    print("Starting training...")
    trainer.train()
    
    print(f"Saving model to {OUTPUT_DIR}...")
    trainer.save_model()
    tokenizer.save_pretrained(OUTPUT_DIR)
    
    print("Training complete!")

if __name__ == "__main__":
    train()