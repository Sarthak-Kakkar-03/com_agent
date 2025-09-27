# info_agent.py
import logging
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from .information import PROFILE_TEXT

from .configs import deepseek_api_key, set_env
from langchain_core.pydantic_v1 import BaseModel, Field

set_env()
logger = logging.getLogger(__name__)


info_llm = ChatOpenAI(
    model="deepseek-chat",
    openai_api_key=deepseek_api_key,
    openai_api_base="https://api.deepseek.com/beta",
    temperature=0.7,
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
        "If the information isn't present in the profile above, return exactly: Not available\n\n"
        "Request: {query}\n\n"
        "{format_instructions}"
    ),
    input_variables=["query"],
    partial_variables={
        "format_instructions": info_parser.get_format_instructions(),
        "profile": PROFILE_TEXT,
    },
)

info_chain = info_prompt | info_llm | info_parser

