import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from promptuner import Prompt
from promptuner.decorators import BaseDecorator
from config import MODEL_NAME
import importlib
import os

router = APIRouter()

class DecoratorConfig(BaseModel):
    name: str
    params: Optional[Dict] = {}

class PromptRequest(BaseModel):
    task: str
    variables: List[str]
    decorators: List[DecoratorConfig]
    modelName: Optional[str] = None
    apiToken: Optional[str] = None

class PromptResponse(BaseModel):
    prompt: str
    token_count: int

def load_decorator(decorator_config: DecoratorConfig) -> BaseDecorator:
    module = importlib.import_module('promptuner.decorators')
    decorator_class = getattr(module, decorator_config.name)
    return decorator_class(**decorator_config.params)

@router.post("/generate_prompt", response_model=PromptResponse)
async def generate_prompt(request: PromptRequest):
    try:
        model_name = request.modelName or MODEL_NAME
        api_key = request.apiToken or os.getenv("ANTHROPIC_API_KEY")
        
        # Initialize the Prompt
        prompt = Prompt(request.task, variables=request.variables, model_name=model_name, api_key=api_key)
        
        # Load and apply decorators
        decorators = [load_decorator(dec_config) for dec_config in request.decorators]
        prompt.apply_decorator(decorators)
        
        # Train the prompt
        prompt.train()
        
        return PromptResponse(prompt=prompt.prompt, token_count=prompt.token_count)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/config")
async def get_config():
    return {
        "model_name": os.getenv("MODEL_NAME"),
        "api_key": os.getenv("ANTHROPIC_API_KEY")[:5] + "..." if os.getenv("ANTHROPIC_API_KEY") else None
    }