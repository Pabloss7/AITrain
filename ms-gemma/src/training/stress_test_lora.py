import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel
from dotenv import load_dotenv

load_dotenv("../../.env")

# Configuration
MODEL_NAME = "google/gemma-2-2b-it"
ADAPTER_PATH = "../models/gemma_lora_output"

def get_model():
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
    return model, tokenizer

def run_test(model, tokenizer, scenario_name, input_text):
    print(f"\n>>> TESTING SCENARIO: {scenario_name}")
    full_prompt = f"<start_of_turn>user\n{input_text}<end_of_turn>\n<start_of_turn>model\n"
    inputs = tokenizer(full_prompt, return_tensors="pt").to("cuda")
    
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
    print("\nRESULT:")
    print(response.split("model\n")[-1])
    print("-" * 50)

def stress_test():
    model, tokenizer = get_model()

    scenarios = [
        {
            "name": "Generalization (Unseen Value/Role Combination)",
            "input": """You are an expert League of Legends coach.
Your task is to transform a technical performance analysis into clear and actionable gameplay advice.

ANALYSIS DATA:
Player analyzed:
- Role: JUNGLE

In-game aspects with negative impact detected:
- Pathing Efficiency: Capacity to clear camps optimally (value: -0.85, SHAP impact: -1.2)
- Counter-Ganking: Reacting to enemy jungle pressure (value: 0.1, SHAP impact: -0.5)"""
        },
        {
            "name": "Role Consistency (TOP with unique issues)",
            "input": """You are an expert League of Legends coach.
Your task is to transform a technical performance analysis into clear and actionable gameplay advice.

ANALYSIS DATA:
Player analyzed:
- Role: TOP

In-game aspects with negative impact detected:
- Split Push Pressure: Capacity to draw pressure to side lanes (value: -0.9, SHAP impact: -1.5)
- TP Usage: Effective use of Teleport for teamplay (value: -0.4, SHAP impact: -0.8)"""
        },
        {
            "name": "Extreme Negative (Many issues)",
            "input": """You are an expert League of Legends coach.
Your task is to transform a technical performance analysis into clear and actionable gameplay advice.

ANALYSIS DATA:
Player analyzed:
- Role: ADC

In-game aspects with negative impact detected:
- Positioning: Safety in fights (value: -0.95, SHAP impact: -2.0)
- Resource Management: Mana and health upkeep (value: -0.8, SHAP impact: -1.1)
- Map Awareness: Dodging ganks (value: -0.7, SHAP impact: -0.9)"""
        },
        {
            "name": "Low Impact Scenario",
            "input": """You are an expert League of Legends coach.
Your task is to transform a technical performance analysis into clear and actionable gameplay advice.

ANALYSIS DATA:
Player analyzed:
- Role: SUPPORT

In-game aspects with negative impact detected:
- Warding: Vision placement (value: -0.1, SHAP impact: -0.15)"""
        },
        {
            "name": "Hallucination Check (Random Data)",
            "input": """You are an expert League of Legends coach.
Your task is to transform a technical performance analysis into clear and actionable gameplay advice.

ANALYSIS DATA:
Player analyzed:
- Role: MID

In-game aspects with negative impact detected:
- Cooking Skills: Efficiency with biscuits (value: -1.0, SHAP impact: -5.0)"""
        }
    ]

    for scenario in scenarios:
        run_test(model, tokenizer, scenario["name"], scenario["input"])

if __name__ == "__main__":
    stress_test()
