import logging

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
import requests

from .settings import settings

settings.export_to_environ()
deepseek_api_key = settings.DEEPSEEK_API_KEY
logger = logging.getLogger(__name__)


info_llm = ChatOpenAI(
    model="deepseek-chat",
    openai_api_key=deepseek_api_key,
    openai_api_base="https://api.deepseek.com/v1",
    temperature=0.2,
    timeout=None,
    max_retries=2,
    api_key=deepseek_api_key,
)


class InfoResponse(BaseModel):
    info_message: str = Field(description="Concise answer to the employer's info request.")
    message: str = Field(
        description="Internal note to the downstream message agent, using the information you provided."
    )


info_parser = PydanticOutputParser(pydantic_object=InfoResponse)

info_prompt = PromptTemplate(
    template=(
        "{profile}\n\n"
        "Based on the following request, provide only the information asked.\n"
        "Supervisor instruction: {supervisor_instruction}\n\n"
        "If the information isn't present in the profile above, return exactly: Not available\n\n"
        "Request: {query}\n\n"
        "{format_instructions}"
    ),
    input_variables=["query", "profile", "supervisor_instruction"],
    partial_variables={"format_instructions": info_parser.get_format_instructions()},
)


def _fetch_profile(query: str, supervisor_instruction: str) -> str:
    if not settings.RETRIEVAL_ENDPOINT:
        return ""

    retrieval_query = query
    if supervisor_instruction:
        retrieval_query = f"{query}\n\nSupervisor instruction: {supervisor_instruction}"

    headers = {
        "Authorization": f"Bearer {settings.RETRIEVAL_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            settings.RETRIEVAL_ENDPOINT,
            headers=headers,
            json={"query": retrieval_query, "top_k": 5},
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()
    except Exception:
        logger.exception("Failed to retrieve profile context")
        return ""

    results = data.get("results", [])
    chunks = [item.get("text", "").strip() for item in results if isinstance(item, dict) and item.get("text")]
    return "\n".join(chunks)


class InfoChain:
    def invoke(self, inputs: dict) -> InfoResponse:
        query = str(inputs.get("query", "")).strip()
        supervisor_instruction = str(inputs.get("supervisor_instruction", "")).strip()
        profile = _fetch_profile(query, supervisor_instruction)
        if not profile:
            return InfoResponse(info_message="Not available", message="Not available")
        return (info_prompt | info_llm | info_parser).invoke(
            {
                "query": query,
                "profile": profile,
                "supervisor_instruction": supervisor_instruction,
            }
        )


info_chain = InfoChain()
