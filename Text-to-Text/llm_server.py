## To run server: python llm_server.py
## To run client: python post_text.py

# pip install fastapi uvicorn
# pip install accelerate

from fastapi import FastAPI, Request
from fastapi.responses import Response
import uvicorn

from pydantic import BaseModel

import torch
import transformers
from transformers import AutoModelForCausalLM , AutoTokenizer

### https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard
#model_name = "Q-bert/Mamba-130M"
#model_name = "Q-bert/Mamba-370M"
#model_name = "Q-bert/Mamba-790M"
#model_name = "Q-bert/Mamba-1B"
#model_name = "Q-bert/Mamba-3B"
#model_name = "Q-bert/Mamba-3B-slimpj"
#model_name = "microsoft/phi-2"
#model_name = "microsoft/Orca-2-7b"
#model_name = "google/gemma-1.1-2b-it"
#model_name = "google/gemma-1.1-7b-it"
#model_name = "mistralai/Mistral-7B-Instruct-v0.2"
#model_name = "openlm-research/open_llama_3b_v2"
#model_name = "openlm-research/open_llama_7b_v2"
#model_name = "meta-llama/Llama-2-7b-hf"
#model_name = "meta-llama/Llama-2-7b-chat-hf"
#model_name = "meta-llama/Meta-Llama-3-8B-Instruct"
#model_name = "lmsys/vicuna-7b-v1.5"
#model_name = "lmsys/vicuna-7b-v1.5-16k"
#model_name = "Nexusflow/Starling-LM-7B-beta"

#model_name = "ckip-joint/bloom-3b-zh" 
#model_name = "Qwen/Qwen1.5-7B-Chat" # 通义千问
#model_name = "01-ai/Yi-6B-Chat" # 零一万物
#model_name = "yentinglin/Taiwan-LLM-7B-v2.0.1-chat" # 台大
#model_name = "MediaTek-Research/Breeze-7B-Base-v1_1" # 達哥
#model_name = "MediaTek-Research/Breeze-7B-Instruct-v0_1" # 達哥
#model_name = "INX-TEXT/Bailong-instruct-7B" # 白龍
#model_name = "taide/TAIDE-LX-7B" # TAIDE
model_name = "taide/TAIDE-LX-7B-Chat" # TAIDE

print(model_name)

#LLM = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True, torch_dtype="auto", device_map="cuda") # for Mamba
LLM = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True, torch_dtype=torch.bfloat16, device_map="cuda")

tokenizer = AutoTokenizer.from_pretrained(model_name)

app = FastAPI()

class UserData(BaseModel):
    text: str

@app.get("/")
def root():
    return Response("Hello World!")

@app.post("/text")
def text(user_data: UserData):
    prompt = user_data.text
    print(prompt)

    input_ids = tokenizer.encode(prompt, return_tensors="pt").to("cuda")
    output = LLM.generate(input_ids, max_length=128, num_beams=5, no_repeat_ngram_size=2, pad_token_id=tokenizer.eos_token_id, do_sample=True)
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    print("LLM: "+generated_text) 
    return Response(generated_text)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
