from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
from gemmaGenerator import generate
import torch

app = FastAPI()



class PromptRequest(BaseModel):
    input: str

@app.post("/generate")
def generate(request: PromptRequest):
    return generate(request.input)