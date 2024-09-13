from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from configs import deepseek_api_key, set_env
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

set_env()

supervisor_llm = ChatOpenAI(
    model='deepseek-chat',
    openai_api_key=deepseek_api_key,
    openai_api_base='https://api.deepseek.com/beta',
    temperature=1.0,
    max_tokens=8192,
    timeout=None,
    max_retries=2,
    api_key=deepseek_api_key
)


class SupervisorResponse(BaseModel):
    supervisor_message: str = Field(description="Detailed instruction about the message/task to send to the next agent")
    next: str = Field(description="enum: MAIL or INFO")
    display_message: str = Field(description="Message to display the employer in the conversation, corresponding to "
                                             "the current state")


supervisor_parser = PydanticOutputParser(pydantic_object=SupervisorResponse)

supervisor_prompt = PromptTemplate(
    template=(
        "You are an AI-powered conversation manager within a system that serves as a communication agent for Sarthak Kakkar. "
        "Your primary goal is to truthfully represent Sarthak Kakkar to potential employers while maintaining a positive outlook. "
        "Based on the current state of the conversation, decide on the best course of action. You have two options:\n\n"
        "1. Instruct the email agent to send a summary of the conversation to Sarthak (MAIL).\n"
        "2. Request the information agent to retrieve additional relevant information about Sarthak (INFO).\n\n"
        "Make your decision based on which action will best support Sarthak’s representation.\n"
        "Follow these instructions:\n"
        "{format_instructions}\n\n"
        "Current State Information:\n\n"
        "- Messages: {messages_as_string}\n"
        "- Name of Employer: {name}\n"
        "- Email of Employer: {email}\n"
        "- Latest 5 messages shown to employer: {display_messages}\n"
        "Based on the above information, provide the next task and specify which agent should perform it."

    ),
    input_variables=['messages_as_string', 'name', 'email', 'display_messages'],
    partial_variables={"format_instructions": supervisor_parser.get_format_instructions()}

)

supervisor_chain = supervisor_prompt | supervisor_llm | supervisor_parser

if __name__ == '__main__':
    set_env()
    result = supervisor_chain.invoke(
        {'messages_as_string': 'Tell me about Sarthak Kakkar',
         'name': 'ABC',
         'email': 'test@mail',
         'display_messages': ''}
    )
    print(result.next)
    print(result.display_message)
