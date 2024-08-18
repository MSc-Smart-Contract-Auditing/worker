import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import json
from src.utils import WorkingDirectory

WORK_DIR = WorkingDirectory.get()

with open(WORK_DIR / "src/analysis/model.config.json") as f:
    config = json.load(f)


class Model:
    def __init__(self, model_path):
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            trust_remote_code=True,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_path, trust_remote_code=True
        )

    def generate(self, prompt, max_length=50):
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt")
        output = self.model.generate(input_ids, max_length=max_length)
        return self.tokenizer.decode(output[0], skip_special_tokens=True)

    def __call__(self, prompt, max_length=50):
        return self.generate(prompt, max_length)

    def __str__(self):
        return f"{self.model.__class__.__name__}"


MODEL = Model(config["model"])
