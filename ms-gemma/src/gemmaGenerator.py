import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os

def base_path():
    return os.path.dirname(__file__)

def load_model():
    model_name = os.path.join(base_path(), "models", "gemma_lora_output")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.bfloat16,
        device_map="auto"
    )
    return tokenizer, model

def generate(input):
    try:
        tokenizer, model = load_model()
        inputs = tokenizer(input, return_tensors="pt").to("cuda")
        outputs = model.generate(**inputs, max_new_tokens=200)
        return tokenizer.decode(outputs[0])
    except Exception as e:
        print("Error generating response:", e)
        return "Error generating response"
