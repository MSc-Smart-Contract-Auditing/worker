import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from src.utils import WorkingDirectory
from typing import List

WORKING_DIR = WorkingDirectory.get()

with open(WORKING_DIR / "src/analysis/model.config.json") as f:
    model_config = json.load(f)

with open(WORKING_DIR / "src/analysis/prompts/analyze.txt") as f:
    analyze_prompt = f.read()

with open(WORKING_DIR / "src/analysis/prompts/merge.txt") as f:
    merge_prompt = f.read()

MODEL_PATH = model_config["model_path"]


class Model:
    def __init__(self, model_path=MODEL_PATH):
        self.model_path = model_path

    def load(self):

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_path, trust_remote_code=True
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            trust_remote_code=True,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )

    def analyze(self, codeblocks: str) -> str:
        messages = [{"role": "user", "content": analyze_prompt.format(codeblocks)}]
        inputs = self.tokenizer.apply_chat_template(
            messages, add_generation_prompt=True, return_tensors="pt"
        ).to(self.model.device)

        outputs = self.model.generate(
            inputs,
            max_new_tokens=512,
            do_sample=True,
            top_k=1,
            top_p=0.95,
            num_return_sequences=1,
            eos_token_id=self.tokenizer.eos_token_id,
        )
        return self.tokenizer.decode(
            outputs[0][len(inputs[0]) :], skip_special_tokens=True
        )

    def merge(self, audits: List[str]) -> str:
        messages = [
            {"role": "user", "content": merge_prompt.format("\n\n".join(audits))}
        ]
        inputs = self.tokenizer.apply_chat_template(
            messages, add_generation_prompt=True, return_tensors="pt"
        ).to(self.model.device)

        outputs = self.model.generate(
            inputs,
            max_new_tokens=512,
            do_sample=True,
            top_k=1,
            top_p=0.95,
            num_return_sequences=1,
            eos_token_id=self.tokenizer.eos_token_id,
        )
        return self.tokenizer.decode(
            outputs[0][len(inputs[0]) :], skip_special_tokens=True
        )


MODEL = Model(MODEL_PATH)
