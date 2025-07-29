from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_PATH = "/storage/ice-shared/vip-vvk/llm_storage/meta-llama/Llama-3.3-70B-Instruct"

print("Starting model test...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH,
    trust_remote_code=True,
    local_files_only=True
)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    device_map="auto",
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    local_files_only=True
)

print("Model loaded. Generating...")

prompt = "Q: What is 2 + 2?\nA:"
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

with torch.no_grad():
    outputs = model.generate(**inputs, max_new_tokens=10, do_sample=False)

response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(f"Model output:\n{response}")
