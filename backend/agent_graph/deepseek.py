from typing import Any

from langchain_openai import ChatOpenAI

from .settings import settings

settings.export_to_environ()


DEEPSEEK_NON_THINKING = {"thinking": {"type": "disabled"}}


def deepseek_chat(
    *,
    temperature: float,
    max_tokens: int | None = None,
    json_mode: bool = False,
    **kwargs: Any,
) -> ChatOpenAI:
    model_kwargs: dict[str, Any] = {
        "extra_body": DEEPSEEK_NON_THINKING,
    }
    if json_mode:
        model_kwargs["response_format"] = {"type": "json_object"}

    return ChatOpenAI(
        model=settings.DEEPSEEK_MODEL,
        openai_api_key=settings.DEEPSEEK_API_KEY,
        api_key=settings.DEEPSEEK_API_KEY,
        openai_api_base=settings.DEEPSEEK_BASE_URL,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=None,
        max_retries=2,
        model_kwargs=model_kwargs,
        **kwargs,
    )
