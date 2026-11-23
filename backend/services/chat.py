"""
Chat service orchestrator.
Manages multi-turn conversation, streaming, reasoning traces, parameter bounds,
and database persistence with user data isolation.
"""
from typing import List, Dict, Any, Generator, Optional
from backend.providers.registry import registry
from backend.repositories.storage import add_message, log_usage
from backend.security import sanitize_text

def stream_chat_response(
    conversation_id: int,
    provider_name: str,
    model: str,
    messages: List[Dict[str, Any]],
    temperature: float = 0.7,
    max_tokens: int = 2048,
    system_prompt: Optional[str] = None,
    user_id: Optional[int] = None
) -> Generator[str, None, None]:
    """
    Streams response from the selected provider adapter, sanitizes output,
    and saves the completed message to the database.
    """
    # 1. Parameter Validation & Boundary Enforcement
    safe_temp = max(0.0, min(float(temperature), 2.0))
    safe_tokens = max(1, min(int(max_tokens), 8192))
    clean_prompt = system_prompt.strip() if system_prompt else None

    # 2. Provider Resolution
    provider = registry.get_provider(provider_name)
    if not provider:
        yield f"⚠️ Provider '{sanitize_text(provider_name)}' not found or configured."
        return

    full_content = []
    full_reasoning = []
    is_reasoning = False

    try:
        stream = provider.chat_stream(
            messages=messages,
            model=model,
            temperature=safe_temp,
            max_tokens=safe_tokens,
            system_prompt=clean_prompt
        )

        for chunk in stream:
            if "> 🧠 **Thinking Process:**" in chunk:
                is_reasoning = True
            elif "\n\n---\n\n" in chunk:
                is_reasoning = False

            if is_reasoning:
                full_reasoning.append(chunk)
            else:
                full_content.append(chunk)

            yield chunk

        # 3. Persist assistant message in DB with user isolation
        complete_text = "".join(full_content).replace("\n\n---\n\n", "").strip()
        complete_reasoning = "".join(full_reasoning).strip() if full_reasoning else None

        if complete_text or complete_reasoning:
            add_message(
                conversation_id=conversation_id,
                role="assistant",
                content=complete_text or complete_reasoning or "",
                reasoning=complete_reasoning,
                token_count=len((complete_text or "").split())
            )
            log_usage(
                provider=provider_name,
                model=model,
                operation="chat",
                input_tokens=sum(len(str(m.get("content", "")).split()) for m in messages),
                output_tokens=len((complete_text or "").split()),
                cost_estimate=0.0,
                user_id=user_id
            )

    except Exception as e:
        yield f"⚠️ **Service Exception:** {sanitize_text(str(e))}"
