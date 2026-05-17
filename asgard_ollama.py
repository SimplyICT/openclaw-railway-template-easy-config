import subprocess
import json
import sys

# Configuration for the Bruce-to-Ollama SDWAN Bridge
OLLAMA_URL = "http://100.117.41.63:11434/api/generate"
PROXY = "socks5h://127.0.0.1:1055"

def query_local(prompt, model="llama3.1:8b"):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    # Use subprocess curl to bypass internal python proxy library issues on Railway
    cmd = [
        "curl", "-s", "--socks5-hostname", "127.0.0.1:1055",
        "-X", "POST", OLLAMA_URL,
        "-d", json.dumps(payload),
        "-H", "Content-Type: application/json"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            return json.loads(result.stdout).get("response", "No response.")
        else:
            return f"Curl Error: {result.stderr}"
    except Exception as e:
        return f"System Error: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(query_local(" ".join(sys.argv[1:])))
    else:
        print("Usage: python3 asgard_ollama.py <prompt>")
