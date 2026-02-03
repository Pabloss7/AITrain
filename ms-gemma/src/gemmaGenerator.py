import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import os

class GemmaGenerator:
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.base_model_id = "google/gemma-2-2b-it"
        self.adapter_path = os.path.join(os.path.dirname(__file__), "models", "gemma_lora_output")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.load_model()

    def load_model(self):
        print(f"Loading tokenizer and base model: {self.base_model_id}...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.base_model_id)
        
        # Load base model in 4-bit or 8-bit to save VRAM if needed, 
        # but here we follow the previous bfloat16 setup
        base_model = AutoModelForCausalLM.from_pretrained(
            self.base_model_id,
            torch_dtype=torch.bfloat16,
            device_map="auto"
        )
        
        print(f"Loading adapter from {self.adapter_path}...")
        self.model = PeftModel.from_pretrained(base_model, self.adapter_path)
        self.model.to(self.device)
        self.model.eval()
        print("Model and adapter loaded successfully!")

    def generate_response(self, text_input, max_new_tokens=256):
        try:
            print(f"--- GENERATION START ---")
            print(f"Input text length: {len(text_input)}")
            inputs = self.tokenizer(text_input, return_tensors="pt").to(self.device)
            input_length = inputs.input_ids.shape[1]
            print(f"Input tokens: {input_length}")
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs, 
                    max_new_tokens=max_new_tokens,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9,
                    eos_token_id=self.tokenizer.eos_token_id,
                    pad_token_id=self.tokenizer.pad_token_id if self.tokenizer.pad_token_id else self.tokenizer.eos_token_id
                )
            
            # Decode the full output for debugging
            full_decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=False)
            print(f"Full decoded output length: {len(full_decoded)}")
            print(f"Full decoded output (first 200 chars): {full_decoded[:200]}...")
            
            # Decode only the generated part
            generated_tokens = outputs[0][input_length:]
            decoded_response = self.tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()
            
            # Clean up potential turn identifiers like 'model' at the start
            if decoded_response.lower().startswith("model"):
                decoded_response = decoded_response[5:].strip()
            
            print(f"Decoded response: '{decoded_response}'")
            print(f"--- GENERATION END ---")
            
            return decoded_response
        except Exception as e:
            print("Error generating response:", e)
            return f"Error generating response: {str(e)}"

# Singleton instance
generator = None

def get_generator():
    global generator
    if generator is None:
        generator = GemmaGenerator()
    return generator
