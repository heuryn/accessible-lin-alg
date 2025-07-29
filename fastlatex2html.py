import os
import time
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_PATH = "/storage/ice-shared/vip-vvk/llm_storage/Qwen/Qwen2.5-7B-Instruct"
INPUT_DIR = "/home/hice1/hyu462/scratch/accessible-lin-alg/Math 1554 Lecture Slides for Distance Math/Chapter1"
OUTPUT_DIR = Path("chapter1")
OUTPUT_DIR.mkdir(exist_ok=True)

print("Loading tokenizer and model...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH, trust_remote_code=True, local_files_only=True
)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    device_map="auto",
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    local_files_only=True
)

print("Model loaded successfully.")

def convert(tex, filename):
    messages = [
        {"role": "system", "content": "You are a converter that transforms LaTeX Beamer slides into clean HTML. "
         "Use MathJax for math. Assume all \\includegraphics refer to images in the folder 'images'. "
         "Convert LaTeX to valid standalone HTML5. Output only valid HTML5. Do not explain anything."},
        {"role": "user", "content": tex}
    ]

    print(f"[{filename}] Applying chat template...")
    input_ids = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt"
    ).to(model.device)

    input_len = input_ids.shape[-1]
    print(f"[{filename}] Input tokens: {input_len}")

    max_out_tokens = 4096
    print(f"[{filename}] Generating with max_new_tokens={max_out_tokens}...")

    start = time.time()
    with torch.no_grad():
        outputs = model.generate(
            input_ids,
            max_new_tokens=max_out_tokens,
            do_sample=False
        )
    duration = time.time() - start
    print(f"[{filename}] Generation complete in {duration:.2f} seconds.")

    # Strip off the prompt from the output
    generated_ids = outputs[0][input_len:]
    html = tokenizer.decode(generated_ids, skip_special_tokens=True)

    if not html.strip():
        print(f"[{filename}] WARNING: Empty output.")
    else:
        print(f"[{filename}] Output length: {len(html)} characters")

    if "</html>" in html:
        html = html.split("</html>")[0] + "</html>"

    return html


# Optional: limit to 1 file for debug
# FILES = list(Path(INPUT_DIR).glob("*.tex"))
FILES = [Path("/home/hice1/hyu462/scratch/accessible-lin-alg/Math 1554 Lecture Slides for Distance Math/Chapter1/1_1_1.tex")]
print(f"Found {len(FILES)} .tex files")

for i, file in enumerate(FILES):
    print(f"\n[{i+1}/{len(FILES)}] Processing {file.name}")
    
    try:
        tex = file.read_text(encoding="utf-8")
        html = convert(tex, file.name)

        out_file = OUTPUT_DIR / (file.stem + ".html")
        out_file.write_text(html, encoding="utf-8")
        print(f"[{file.name}] → Saved to {out_file}")

        torch.cuda.empty_cache()  # free VRAM just in case

    except Exception as e:
        print(f"[{file.name}] ERROR: {e}")
        continue
