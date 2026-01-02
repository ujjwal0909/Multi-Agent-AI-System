import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:3b"  # recommended for ~8GB RAM

def call_llm(system_prompt: str, user_prompt: str) -> str:
    prompt = f"SYSTEM:\n{system_prompt}\n\nUSER:\n{user_prompt}\n\nASSISTANT:\n"
    payload = {"model": MODEL, "prompt": prompt, "stream": False, "options": {"temperature": 0.3}}

    r = requests.post(OLLAMA_URL, json=payload, timeout=600)
    if r.status_code != 200:
        raise RuntimeError(f"Ollama HTTP {r.status_code}: {r.text}")

    data = r.json()
    if "response" not in data:
        raise RuntimeError(f"Unexpected Ollama JSON: {data}")

    return data["response"].strip()
