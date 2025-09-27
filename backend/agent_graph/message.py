# message.py
import logging

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
from .information import PROFILE_OWNER_NAME

from .configs import set_env, deepseek_api_key

set_env()
logger = logging.getLogger(__name__)


class MessageResponse(BaseModel):
    chat_response: str = Field(
        description="Message response to the employer"
    )


message_parser = PydanticOutputParser(pydantic_object=MessageResponse)

message_llm = ChatOpenAI(
    model="deepseek-chat",
    openai_api_key=deepseek_api_key,
    openai_api_base="https://api.deepseek.com/v1",
    temperature=0.7,  # a bit more stable for templated replies
    timeout=None,
    max_retries=2,
    api_key=deepseek_api_key,
)

message_prompt = PromptTemplate(
    template=(
        "You are an AI-powered message generation agent interacting with a potential employer on behalf of "
        f"{PROFILE_OWNER_NAME} Use the visible conversation (available to the employer), any internal summaries, "
        "and the latest info retrieved by"
        f"the information agent. Maintain professional tone, keep replies concise, and only discuss {PROFILE_OWNER_NAME}.\n\n"
        f"Politely refuse requests that are not about {PROFILE_OWNER_NAME}.\n\n"
        "Visible conversation (latest messages first or in order given):\n{visible_conversation}\n\n"
        "Latest info from info agent: {info}\n"
        "Employer name: {employer_name}\n\n"
        "{format_instructions}"
    ),
    input_variables=[
        "visible_conversation",
        "invisible_conversation",
        "info",
        "employer_name",
    ],
    partial_variables={"format_instructions": message_parser.get_format_instructions()},
)

message_chain = message_prompt | message_llm | message_parser
