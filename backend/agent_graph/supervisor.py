
# supervisor.py
import logging
from typing import Literal

from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from .information import PROFILE_OWNER_NAME
from .settings import settings
settings.export_to_environ()
deepseek_api_key = settings.DEEPSEEK_API_KEY

logger = logging.getLogger(__name__)

class SupervisorResponse(BaseModel):
    supervisor_message: str = Field(
        description="Detailed instruction about the message/task to send to the next agent"
    )
    next: Literal["MAIL", "INFO", "MESSAGE"] = Field(
        description="enum: MAIL, INFO, or MESSAGE"
    )
    display_message: str = Field(
        description=(
            "Short/concise message to display to the employer, stating which agent you delegated to and why."
        )
    )

supervisor_parser = PydanticOutputParser(pydantic_object=SupervisorResponse)

supervisor_llm = ChatOpenAI(
    model="deepseek-chat",
    openai_api_key=deepseek_api_key,
    openai_api_base="https://api.deepseek.com/v1",
    temperature=0.3,  # more deterministic routing
    timeout=None,
    max_retries=2,
    api_key=deepseek_api_key,
)

supervisor_prompt = PromptTemplate(
    template=(
        "You are an AI conversation manager speaking directly with the employer. Your goal is to choose the next best "
        f"step to support {PROFILE_OWNER_NAME}.\n\n"
        "OPTIONS:\n"
        f"1. Choose 'MAIL' only if the employer explicitly wants to reach out to {PROFILE_OWNER_NAME} or asks you to notify him; "
        "   ALWAYS attach or summarize the conversation so far.\n"
        f"2. Choose 'INFO' if the employer asked for information about {PROFILE_OWNER_NAME}.\n"
        f"3. Choose 'MESSAGE' if the request is neither an email-send request nor information about {PROFILE_OWNER_NAME}.\n\n"
        "CONTEXT\n"
        "Latest conversation with the employer till this point: {visible_messages}\n\n"
        "Return strictly following the format instructions.\n"
        "{format_instructions}"
    ),
    input_variables=["visible_messages"],
    partial_variables={"format_instructions": supervisor_parser.get_format_instructions()},
)

supervisor_chain = supervisor_prompt | supervisor_llm | supervisor_parser
