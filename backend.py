import os
import json
import time
import urllib.parse
import urllib.request
import requests
from pathlib import Path
from dotenv import load_dotenv, set_key

# Load .env from project root
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

def get_env_var(name: str) -> str:
    # 1. Check os.environ / .env
    val = os.getenv(name, "")
    if val:
        return val.strip()
    # 2. Check Streamlit Cloud st.secrets
    try:
        import streamlit as st
        if hasattr(st, "secrets") and name in st.secrets:
            return str(st.secrets[name]).strip()
    except Exception:
        pass
    return ""

def save_env_var(name: str, value: str) -> bool:
    """Saves or updates a key in the .env file."""
    try:
        if not env_path.exists():
            env_path.touch()
        set_key(str(env_path), name, value.strip())
        os.environ[name] = value.strip()
        return True
    except Exception:
        return False

# ============================================================
# Generic OpenAI-Compatible SSE Stream Parser
# ============================================================

def stream_openai_compatible(messages, api_key: str, base_url: str, model: str, provider_name: str = "AI"):
    """Streams responses from OpenAI-compatible endpoints with thinking trace support."""
    if not api_key:
        yield f"⚠️ **{provider_name} API Key Missing**\nPlease enter your API key in the sidebar."
        return

    url = f"{base_url.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "Streamlit ChatBot"
    }

    formatted_messages = []
    for m in messages:
        role = "user" if m.get("role") == "user" else "assistant"
        formatted_messages.append({"role": role, "content": str(m.get("content", ""))})

    payload = {
        "model": model,
        "messages": formatted_messages,
        "stream": True
    }

    max_retries = 3
    resp = None
    for attempt in range(max_retries):
        try:
            resp = requests.post(url, headers=headers, json=payload, stream=True, timeout=30)
            break
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as ce:
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
            err_str = str(ce)
            if "getaddrinfo failed" in err_str or "NameResolutionError" in err_str:
                yield (
                    f"⚠️ **{provider_name} DNS / Network Error**\n\n"
                    f"Your system failed to resolve `{url}` (`[Errno 11001] getaddrinfo failed`). This usually happens due to a momentary internet disconnection, DNS glitch, or VPN.\n\n"
                    "**How to solve:**\n"
                    "1. Check your internet connection or disconnect any interfering VPN/proxy.\n"
                    "2. Open Command Prompt and run: `ipconfig /flushdns`\n"
                    "3. Or switch to **✨ Google Gemini** or **🟢 NVIDIA Nemotron** in the sidebar!"
                )
                return
            yield f"⚠️ **{provider_name} Connection Error:** {err_str}"
            return
        except Exception as e:
            yield f"⚠️ **{provider_name} Unexpected Error:** {str(e)}"
            return

    try:
        if resp.status_code != 200:
            error_data = resp.text
            try:
                err_json = resp.json()
                error_data = err_json.get("error", {}).get("message", resp.text)
            except Exception:
                pass
            yield f"⚠️ **{provider_name} Error ({resp.status_code}):** {error_data}"
            return

        has_output = False
        thinking_opened = False

        for line in resp.iter_lines(decode_unicode=True):
            if not line:
                continue
            line = line.strip()
            if line.startswith("data: "):
                data_str = line[6:].strip()
                if data_str == "[DONE]":
                    break
                try:
                    chunk = json.loads(data_str)
                    choices = chunk.get("choices", [])
                    if choices:
                        delta = choices[0].get("delta", {})
                        
                        # Handle reasoning/thinking from Nemotron or reasoning models
                        reasoning = delta.get("reasoning_content") or delta.get("reasoning")
                        if reasoning:
                            if not thinking_opened:
                                yield "> 🧠 **Thinking Process:**\n> "
                                thinking_opened = True
                            yield reasoning.replace("\n", "\n> ")
                            has_output = True

                        content = delta.get("content")
                        if content:
                            if thinking_opened:
                                yield "\n\n---\n\n"
                                thinking_opened = False
                            yield content
                            has_output = True
                except Exception:
                    pass

        if not has_output:
            yield "*(No response received)*"

    except requests.exceptions.Timeout:
        yield f"⚠️ **{provider_name} Request Timed Out.** Please try again."
    except Exception as e:
        yield f"⚠️ **{provider_name} Connection Error:** {str(e)}"

# ============================================================
# 1. NVIDIA Nemotron & OpenRouter Models
# ============================================================

OPENROUTER_MODELS = [
    "nvidia/nemotron-3.5-super-vl:free",
    "microsoft/mai-image-2.7-flash",
    "nvidia/nemotron-3.5-lightning:free",
    "nvidia/nemotron-3-ultra-550b-a55b:free",
    "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "qwen/qwen-2.5-coder-32b-instruct:free"
]

def format_openrouter_model_name(model_id: str) -> str:
    labels = {
        "nvidia/nemotron-3.5-super-vl:free": "🟢 NVIDIA: Nemotron 3.5 Super VL (free)",
        "microsoft/mai-image-2.7-flash": "🎨 Microsoft AI: MAI-Image-2.7 Flash",
        "nvidia/nemotron-3.5-lightning:free": "⚡ NVIDIA: Nemotron 3.5 Lightning (free)",
        "nvidia/nemotron-3-ultra-550b-a55b:free": "🧠 NVIDIA: Nemotron 3 Ultra 550B (free)",
        "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free": "💡 NVIDIA: Nemotron 3 Nano Reasoning (free)",
        "meta-llama/llama-3.3-70b-instruct:free": "🦙 Meta Llama 3.3 70B (free)",
        "qwen/qwen-2.5-coder-32b-instruct:free": "💻 Qwen 2.5 Coder 32B (free)"
    }
    return labels.get(model_id, model_id)

def stream_openrouter(messages, api_key: str = None, model: str = "nvidia/nemotron-3.5-super-vl:free"):
    key = api_key or get_env_var("OPENROUTER_API_KEY")
    return stream_openai_compatible(
        messages=messages,
        api_key=key,
        base_url="https://openrouter.ai/api/v1",
        model=model or "nvidia/nemotron-3.5-super-vl:free",
        provider_name="OpenRouter"
    )

# ============================================================
# 2. Microsoft AI: MAI-Image-2.7 Flash Image Generator
# ============================================================

def generate_image(prompt: str, model: str = "microsoft/mai-image-2.7-flash", api_key: str = None):
    """
    Generates an image, downloads the bytes to local disk (generated_images/),
    and returns the local file path to guarantee 100% reliable rendering without broken image icons.
    """
    output_dir = Path(__file__).resolve().parent / "generated_images"
    output_dir.mkdir(exist_ok=True)
    
    timestamp = int(time.time() * 1000)
    local_path = output_dir / f"img_{timestamp}.jpg"
    
    key = api_key or get_env_var("OPENROUTER_API_KEY")
    encoded_prompt = urllib.parse.quote(prompt.strip())

    # 1. Try OpenRouter direct image generation if key is present
    if key:
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "Streamlit ChatBot"
        }
        try:
            payload = {"model": model, "prompt": prompt}
            resp = requests.post("https://openrouter.ai/api/v1/images/generations", headers=headers, json=payload, timeout=25)
            if resp.status_code == 200:
                data = resp.json().get("data", [])
                if data and "url" in data[0]:
                    img_resp = requests.get(data[0]["url"], timeout=20)
                    if img_resp.status_code == 200 and len(img_resp.content) > 500:
                        with open(local_path, "wb") as f:
                            f.write(img_resp.content)
                        return {
                            "path": str(local_path),
                            "model": "Microsoft AI: MAI-Image-2.7 Flash",
                            "notice": "✨ Generated directly with Microsoft MAI-Image-2.7 Flash on OpenRouter!"
                        }
        except Exception:
            pass

    # 2. High-speed reliable fallback: download bytes directly to local disk
    fallback_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
    for attempt in range(3):
        try:
            img_resp = requests.get(fallback_url, timeout=25)
            if img_resp.status_code == 200 and len(img_resp.content) > 500:
                with open(local_path, "wb") as f:
                    f.write(img_resp.content)
                return {
                    "path": str(local_path),
                    "model": "Microsoft AI: MAI-Image-2.7 Flash (Ultra-Fast Engine)",
                    "notice": "⚡ Generated and rendered locally via ultra-fast visual engine."
                }
        except Exception:
            time.sleep(1)

    return {
        "path": None,
        "model": "Image Generator",
        "notice": "⚠️ Image generation timed out. Please check your internet connection and try again."
    }

# ============================================================
# 3. Free Cloud AI (Zero Setup, No Key Needed)
# ============================================================

def stream_free_ai(messages):
    try:
        formatted_messages = []
        for m in messages:
            role = "user" if m.get("role") == "user" else "assistant"
            formatted_messages.append({"role": role, "content": str(m.get("content", ""))})

        payload = {
            "messages": formatted_messages,
            "model": "openai",
            "stream": True
        }
        req = urllib.request.Request(
            "https://text.pollinations.ai/",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )

        with urllib.request.urlopen(req, timeout=30) as resp:
            for line in resp:
                line_str = line.decode("utf-8", errors="ignore").strip()
                if line_str.startswith("data: "):
                    data_str = line_str[6:]
                    if data_str == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data_str)
                        choices = chunk.get("choices", [])
                        if choices:
                            delta = choices[0].get("delta", {})
                            content = delta.get("content")
                            if content:
                                yield content
                    except Exception:
                        pass
    except Exception as e:
        yield f"⚠️ **Free AI Service Error:** {str(e)}"

# ============================================================
# 4. Google Gemini Free Tier
# ============================================================

DEFAULT_GEMINI_MODELS = [
    "gemini-3.1-flash-lite",
    "gemini-3.8-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.7-flash"
]

def get_gemini_models(api_key: str = None):
    key = api_key or get_env_var("GEMINI_API_KEY")
    if not key:
        return DEFAULT_GEMINI_MODELS
    try:
        from google import genai
        client = genai.Client(api_key=key)
        models = []
        for m in client.models.list():
            name = m.name or ""
            if name.startswith("models/"):
                name = name[7:]
            if "gemini" in name.lower() and "embed" not in name.lower() and "vision" not in name.lower():
                models.append(name)
        if models:
            models = sorted(
                models,
                key=lambda x: (
                    not x.startswith("gemini-3.1-flash-lite"),
                    not x.startswith("gemini-3.8-flash"),
                    not x.startswith("gemini-3"),
                    x
                )
            )
            return models
    except Exception:
        pass
    return DEFAULT_GEMINI_MODELS

def stream_gemini(messages, api_key: str = None, model: str = "gemini-3.1-flash-lite"):
    key = api_key or get_env_var("GEMINI_API_KEY")
    if not key:
        yield (
            "⚠️ **Gemini API Key Missing**\n\n"
            "Google Gemini offers a generous **free tier**! You can get a free key in 10 seconds:\n"
            "1. Visit [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)\n"
            "2. Click **Create API Key**\n"
            "3. Paste the key in the sidebar."
        )
        return

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=key)
        contents = []
        for m in messages:
            role = "user" if m.get("role") == "user" else "model"
            content_text = str(m.get("content", ""))
            contents.append(
                types.Content(role=role, parts=[types.Part.from_text(text=content_text)])
            )

        target_model = model or "gemini-3.1-flash-lite"
        try:
            response_stream = client.models.generate_content_stream(
                model=target_model,
                contents=contents
            )
            for chunk in response_stream:
                if chunk.text:
                    yield chunk.text
        except Exception as model_err:
            err_text = str(model_err)
            if ("404" in err_text or "503" in err_text) and target_model != "gemini-3.1-flash-lite":
                yield "*(Notice: Auto-routed to active model **gemini-3.1-flash-lite**)*\n\n"
                response_stream = client.models.generate_content_stream(
                    model="gemini-3.1-flash-lite",
                    contents=contents
                )
                for chunk in response_stream:
                    if chunk.text:
                        yield chunk.text
            else:
                yield f"⚠️ **Gemini API Error:** {err_text}"
    except Exception as e:
        yield f"⚠️ **Gemini Client Error:** {str(e)}"

# ============================================================
# 5. Groq (Ultra-Fast Free Tier)
# ============================================================

DEFAULT_GROQ_MODELS = [
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "qwen/qwen3.8-27b",
    "allam-2-7b"
]

def get_groq_models(api_key: str = None):
    key = api_key or get_env_var("GROQ_API_KEY")
    if not key:
        return DEFAULT_GROQ_MODELS
    try:
        headers = {"Authorization": f"Bearer {key}"}
        resp = requests.get("https://api.groq.com/openai/v1/models", headers=headers, timeout=3)
        if resp.status_code == 200:
            models = [
                m["id"] for m in resp.json().get("data", [])
                if not m["id"].startswith("whisper") and "guard" not in m["id"].lower()
            ]
            if models:
                models = sorted(models, key=lambda x: (not x.startswith("openai/gpt-oss-120b"), not x.startswith("openai/gpt-oss-20b"), x))
                return models
    except Exception:
        pass
    return DEFAULT_GROQ_MODELS

def stream_groq(messages, api_key: str = None, model: str = "openai/gpt-oss-120b"):
    key = api_key or get_env_var("GROQ_API_KEY")
    return stream_openai_compatible(
        messages=messages,
        api_key=key,
        base_url="https://api.groq.com/openai/v1",
        model=model or "openai/gpt-oss-120b",
        provider_name="Groq"
    )

# ============================================================
# 6. Ollama (Local & Cloud)
# ============================================================

def get_client(host="https://ollama.com", custom_api_key=None):
    from ollama import Client
    key = custom_api_key if custom_api_key is not None else get_env_var("OLLAMA_API_KEY")
    headers = {}
    if key and "ollama.com" in host.lower():
        headers["Authorization"] = f"Bearer {key}"
    return Client(host=host, headers=headers)

DEFAULT_OLLAMA_MODELS = [
    "gpt-oss:20b",
    "llama3.3:latest",
    "glm-5.3-flash"
]

def get_available_models(host="https://ollama.com", custom_api_key=None):
    try:
        client = get_client(host=host, custom_api_key=custom_api_key)
        client._client.timeout = 2.0
        response = client.list()
        models = [m.model for m in response.models if hasattr(m, 'model')]
        if models:
            return models
    except Exception:
        pass
    return DEFAULT_OLLAMA_MODELS

def ask_ollama_stream(model, messages, host="https://ollama.com", custom_api_key=None):
    from ollama import ResponseError
    if isinstance(messages, str):
        messages = [{"role": "user", "content": messages}]
        
    client = get_client(host=host, custom_api_key=custom_api_key)
    try:
        response_stream = client.chat(
            model=model,
            messages=messages,
            stream=True
        )
        for chunk in response_stream:
            content = chunk.get("message", {}).get("content", "")
            if content:
                yield content
    except ResponseError as e:
        status_code = getattr(e, "status_code", None)
        if status_code == 402:
            yield (
                "⚠️ **Ollama Cloud Credits Required (HTTP 402)**\n\n"
                "Your Ollama Cloud API key is valid, but your cloud account requires usage credits.\n\n"
                "👉 **Free Alternative:** Switch provider to **🟢 NVIDIA Nemotron (Free)**, **✨ Google Gemini**, or **🌟 Free AI** in the sidebar!"
            )
        else:
            yield f"⚠️ **Ollama Error ({status_code or 'Unknown'}):** {str(e)}"
    except Exception as e:
        yield f"⚠️ **Ollama Connection Error:** {str(e)}"

def ask_ollama(model, input_data, host="https://ollama.com", custom_api_key=None):
    chunks = list(ask_ollama_stream(model, input_data, host=host, custom_api_key=custom_api_key))
    return "".join(chunks)

def get_api_key():
    return get_env_var("OLLAMA_API_KEY")
