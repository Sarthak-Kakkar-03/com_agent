import logging

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
import requests

from .information import PROFILE_TEXT
from .deepseek import deepseek_chat
from .settings import settings

settings.export_to_environ()
logger = logging.getLogger(__name__)


info_llm = deepseek_chat(
    temperature=0,
    max_tokens=900,
    json_mode=True,
)


class InfoResponse(BaseModel):
    info_message: str = Field(description="Concise answer to the employer's info request.")
    message: str = Field(
        description="Internal note to the downstream message agent, using the information you provided."
    )


info_parser = PydanticOutputParser(pydantic_object=InfoResponse)

info_prompt = PromptTemplate(
    template=(
        "You are answering using retrieved database chunks about the profile owner.\n"
        "The context below is not a single profile object. It is a set of text chunks retrieved from a database.\n"
        "Use only the chunk text that is relevant to the request.\n\n"
        "Retrieved chunks:\n"
        "CHUNK: {chunks}\n\n"
        "Based on the following request, provide only the information asked.\n"
        "Supervisor instruction: {supervisor_instruction}\n\n"
        "If the information isn't present in the retrieved chunks, return exactly: Not available in both json fields.\n\n"
        "Request: {query}\n\n"
        "Return one valid json object and no markdown. Example json output:\n"
        '{{"info_message":"Sarthak has experience building AI systems.","message":"Use the retrieved AI systems detail in the employer-facing response."}}\n\n'
        "{format_instructions}"
    ),
    input_variables=["query", "chunks", "supervisor_instruction"],
    partial_variables={"format_instructions": info_parser.get_format_instructions()},
)


def _fetch_chunks(query: str, supervisor_instruction: str) -> str:
    if not settings.RETRIEVAL_ENDPOINT:
        return f"[Chunk 1]\n{PROFILE_TEXT}"

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
            timeout=50,
        )
        response.raise_for_status()
        data = response.json()
    except Exception:
        logger.exception("Failed to retrieve profile context, falling back to local profile")
        return f"[Chunk 1]\n{PROFILE_TEXT}"

    results = data.get("results", [])
    chunks = []
    for idx, item in enumerate(results, start=1):
        if not isinstance(item, dict):
            continue
        text = item.get("text", "").strip()
        if text:
            chunks.append(f"[Chunk {idx}]\n{text}")

    chunks_text = "\n\n".join(chunks)
    return chunks_text or f"[Chunk 1]\n{PROFILE_TEXT}"


class InfoChain:
    def invoke(self, inputs: dict) -> InfoResponse:
        query = str(inputs.get("query", "")).strip()
        supervisor_instruction = str(inputs.get("supervisor_instruction", "")).strip()
        chunks = _fetch_chunks(query, supervisor_instruction)
        if not chunks:
            return InfoResponse(info_message="Not available", message="Not available")
        return (info_prompt | info_llm | info_parser).invoke(
            {
                "query": query,
                "chunks": chunks,
                "supervisor_instruction": supervisor_instruction,
            }
        )


info_chain = InfoChain()
