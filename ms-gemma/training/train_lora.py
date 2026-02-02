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
from trl import SFTTrainer
from dotenv import load_dotenv

load_dotenv("../../.env")

# Configuration
MODEL_NAME = "google/gemma-3-1b-it"
OUTPUT_DIR = "../models/gemma_lora_output"
DATASET_FILE = "./data/train.jsonl"

def load_jsonl_dataset(file_path):
    """Carga dataset desde archivo JSONL"""
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            data.append(json.loads(line))
    return Dataset.from_list(data)

def formatting_prompts_func(examples):
    """
    Formatea los ejemplos al formato de chat de Gemma.
    Esta función debe devolver una lista de strings.
    """
    texts = []
    for i in range(len(examples["input"])):
        text = f"<start_of_turn>user\n{examples['input'][i]}<end_of_turn>\n<start_of_turn>model\n{examples['output'][i]}<end_of_turn>"
        texts.append(text)
    return texts

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
    
    # Cargar tokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, token=token)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    # Cargar modelo
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        quantization_config=bnb_config,
        device_map="auto",
        token=token,
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

    # Argumentos de entrenamiento
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=3,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        fp16=True,
        logging_steps=10,
        optim="paged_adamw_32bit",
        save_strategy="epoch",
        warmup_steps=10,
    )

    # Crear trainer
    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        peft_config=peft_config,
        formatting_func=formatting_prompts_func,
        max_seq_length=1024,
    )

    print("Starting training...")
    trainer.train()
    
    print(f"Saving model to {OUTPUT_DIR}...")
    trainer.save_model()
    tokenizer.save_pretrained(OUTPUT_DIR)
    
    print("Training complete!")

if __name__ == "__main__":
    train()