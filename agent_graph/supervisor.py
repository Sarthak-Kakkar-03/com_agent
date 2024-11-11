from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from configs import deepseek_api_key, set_env
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

set_env()

# LLM initialization for the supervisor

supervisor_llm = ChatOpenAI(
    model='deepseek-chat',
    openai_api_key=deepseek_api_key,
    openai_api_base='https://api.deepseek.com/v1',
    temperature=1.0,
    # max_tokens=8192,
    timeout=None,
    max_retries=2,
    api_key=deepseek_api_key
)


class SupervisorResponse(BaseModel):
    # Class to hold supervisor response
    supervisor_message: str = Field(description="Detailed instruction about the message/task to send to the next agent")
    next: str = Field(description="enum: MAIL, INFO, or MESSAGE")
    display_message: str = Field(description="Short/Concise message to display the employer in the conversation, detailing which agent you delegated the action to and why")


supervisor_parser = PydanticOutputParser(pydantic_object=SupervisorResponse)

supervisor_prompt = PromptTemplate(
    template=(
        "You are an AI-powered conversation manager tasked with making decisions to support Sarthak Kakkar's representation to potential employers. You are speaking to the employer themselves."
        "Your goal is to choose the best next step based on the conversation state. You have three options:\n"
        "1. Select 'MAIL' only if the employer explicitly says they want to reach out to Sarthak or notify him about "
        "anything, ensure to always"
        "attach a summary of the conversation till now too.\n"
        "2. Select 'INFO' if any information about Sarthak is requested\n"
        "3. Select 'MESSAGE' if the information requested is not about Sarthak Kakkar or an email request, so a message has to be sent back to the employer\n\n"
        "Based on the following conversation context, select the most appropriate action:\n\n"
        "Messages: {messages_as_string}\n"
        "Latest Messages Shown to Employer: {visible_messages}\n\n"
        "Please provide the next task and specify the appropriate agent.\n"
        "These are the format instructions:\n"
        "{format_instructions}"
    ),
    input_variables=['messages_as_string', 'visible_messages'],
    partial_variables={"format_instructions": supervisor_parser.get_format_instructions()}
)


supervisor_chain = supervisor_prompt | supervisor_llm | supervisor_parser

if __name__ == '__main__':
    set_env()
    result = supervisor_chain.invoke(
        {'messages_as_string': ['is sarthak good at python'],
         'name': 'ABC',
         'email': 'test@mail',
         'visible_messages': [''''''],
         'latest_info': 'sarthak knows python'}
    )
    print(result.next)
    print(result.display_message)
    print(result.supervisor_message)
