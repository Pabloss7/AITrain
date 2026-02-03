import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel
from dotenv import load_dotenv

load_dotenv("../../.env")

# Configuration
MODEL_NAME = "google/gemma-2-2b-it"
ADAPTER_PATH = "../models/gemma_lora_output"

def test_inference():
    print(f"Loading tokenizer and base model: {MODEL_NAME}...")
    token = os.getenv("HF_TOKEN")
    
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, token=token)
    
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )

    base_model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        quantization_config=bnb_config,
        device_map="auto",
        token=token,
        trust_remote_code=True
    )
    
    print(f"Loading adapter from {ADAPTER_PATH}...")
    model = PeftModel.from_pretrained(base_model, ADAPTER_PATH)
    model.eval()

    # Sample input from training data structure
    sample_input = """<start_of_turn>user
You are an expert League of Legends coach.

Your task is to transform a technical performance analysis into clear and actionable gameplay advice.

Use the information below to:
- Explain WHY each aspect negatively impacts the player's performance
- Provide concrete in-game advice
- Adapt recommendations to the player's role

Avoid generic tips. Be specific and practical.

ANALYSIS DATA:
Player analyzed:
- Role: MID

In-game aspects with negative impact detected:
- Lane Scaling: Capacity to scale through gold and experience (value: 0.35, SHAP impact: -0.165)
- Objective Pressure: Contribution in achieving objectives (value: -0.5, SHAP impact: -0.82)<end_of_turn>
<start_of_turn>model
"""

    inputs = tokenizer(sample_input, return_tensors="pt").to("cuda")
    
    print("Generating response...")
    with torch.no_grad():
        outputs = model.generate(
            **inputs, 
            max_new_tokens=150,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1
        )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    print("\n--- INFERENCE RESULT ---")
    print(response.split("model\n")[-1])

if __name__ == "__main__":
    test_inference()
