"""
Backward compatibility facade for backend functions.
Redirects to the modern modular backend services and providers.
"""
from backend.config import get_config_var, save_config_var
from backend.services.images import generate_image_studio
from backend.services.chat import stream_chat_response
from backend.providers.registry import registry
from backend.providers.openrouter import OPENROUTER_MODELS, format_openrouter_model_name
from backend.providers.gemini import GeminiProvider
from backend.providers.groq import GroqProvider
from backend.providers.ollama import OllamaProvider

# Compatibility aliases
get_env_var = get_config_var
save_env_var = save_config_var

def stream_openrouter(messages, api_key=None, model="nvidia/nemotron-3.5-super-vl:free"):
    p = registry.get_provider("OpenRouter")
    if api_key:
        p.api_key = api_key
    return p.chat_stream(messages=messages, model=model)

def stream_gemini(messages, api_key=None, model="gemini-3.1-flash-lite"):
    p = registry.get_provider("Google Gemini")
    if api_key:
        p.api_key = api_key
    return p.chat_stream(messages=messages, model=model)

def stream_groq(messages, api_key=None, model="openai/gpt-oss-120b"):
    p = registry.get_provider("Groq")
    if api_key:
        p.api_key = api_key
    return p.chat_stream(messages=messages, model=model)

def stream_free_ai(messages):
    p = registry.get_provider("Free AI")
    return p.chat_stream(messages=messages, model="Free GPT-4o Mini")

def ask_ollama_stream(model, messages, host="http://localhost:11434", custom_api_key=None):
    p = OllamaProvider(host=host, api_key=custom_api_key)
    return p.chat_stream(messages=messages, model=model)

def generate_image(prompt: str, model: str = "microsoft/mai-image-2.7-flash", api_key: str = None):
    return generate_image_studio(prompt=prompt, model=model, api_key=api_key)

def get_gemini_models(api_key=None):
    p = GeminiProvider(api_key=api_key)
    return [m.id for m in p.list_models()]

def get_groq_models(api_key=None):
    p = GroqProvider(api_key=api_key)
    return [m.id for m in p.list_models()]

def get_available_models(host="http://localhost:11434", custom_api_key=None):
    p = OllamaProvider(host=host, api_key=custom_api_key)
    return [m.id for m in p.list_models()]

def get_api_key():
    return get_config_var("OPENROUTER_API_KEY")
