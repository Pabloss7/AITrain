from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from gemmaGenerator import get_generator
import uvicorn
import os

app = FastAPI(title="Gemma LoRA Inference Service")

class PromptRequest(BaseModel):
    input: str

print("Initializing model...")
try:
    generator = get_generator()
except Exception as e:
    print(f"Failed to initialize model: {e}")

@app.post("/generate")
async def generate(request: PromptRequest):
    if not request.input:
        raise HTTPException(status_code=400, detail="Input prompt cannot be empty")
    
    try:
        response = generator.generate_response(request.input)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy", "model_loaded": generator is not None}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)