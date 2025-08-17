from fastapi import FastAPI
from pydantic import BaseModel
from .llm import ask_llm
from .scorer import composite_score
from typing import List

app = FastAPI()

class OptimizeRequest(BaseModel):
    user_input: str
    expected_output: str
    product_name: str
    forbidden_words: List[str]
    custom_mutators: List[str] = []

class OptimizeResult(BaseModel):
    best_prompt: str
    best_output: str
    best_score: float
    all_trials: list

@app.post("/optimize-prompt", response_model=OptimizeResult)
def optimize_prompt(req: OptimizeRequest):
    prompts = [("base", "아래 질문에 답변해라.")]
    for mut in req.custom_mutators:
        prompts.append(("custom", mut.format(
            product_name=req.product_name,
            forbidden_words=", ".join(req.forbidden_words)
        )))
    best = None
    trials = []
    for name, prompt in prompts:
        output = ask_llm(prompt, req.user_input)
        if any(word in output for word in req.forbidden_words):
            score = 0.0
        else:
            score = composite_score(output, req.expected_output, [req.product_name])
        trials.append({"name": name, "prompt": prompt, "output": output, "score": score})
        if best is None or score > best["score"]:
            best = {"name": name, "prompt": prompt, "output": output, "score": score}
    return {
        "best_prompt": best["prompt"],
        "best_output": best["output"],
        "best_score": best["score"],
        "all_trials": trials
    }
