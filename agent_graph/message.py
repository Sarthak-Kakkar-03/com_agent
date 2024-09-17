from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from configs import set_env, deepseek_api_key
from langchain_core.pydantic_v1 import BaseModel, Field

set_env()

message_llm = ChatOpenAI(
    model='deepseek-chat',
    openai_api_key=deepseek_api_key,
    openai_api_base='https://api.deepseek.com/v1',
    temperature=1.0,
    # max_tokens=8192,
    timeout=None,
    max_retries=2,
    api_key=deepseek_api_key
)


class MessageResponse(BaseModel):
    chat_response: str = Field(description="Message response to the employer")


message_parser = PydanticOutputParser(pydantic_object=MessageResponse)


message_prompt = PromptTemplate(
    template= (
        '''You are an AI-powered message generation agent, part of a system interacting with a potential employer on 
        behalf of Sarthak Kakkar. Your role is to analyze the visible conversation between Sarthak and the employer, 
        along with any internal information such as details provided by an information agent about Sarthak or 
        confirmation of actions (e.g., emails sent by a mailing agent). Based on this analysis, generate a message 
        that maintains the flow of the conversation while ensuring it aligns with Sarthak's professional objectives 
        and any relevant updates from the internal agents. Politely deny any requests that are not about Sarthak
         Kakkar or are an email request.\n
        These are the latest messages in the conversation with the employer:\n {visible_conversation}\n\n
        Internal conversation not visible to employer:\n {invisible_conversation}\n\n
        This is the latest received information from information retriever agent: {info}\n
        Following is the name of the person/employer you are conversing with: {employer_name}
        Follow the formatting instructions:\n {format_instructions}\n
        
        '''
    ),

    input_variables=['visible_conversation', 'invisible_conversation', 'info', 'employer_name'],
    partial_variables={"format_instructions": message_parser.get_format_instructions()}

)

message_chain = message_prompt | message_llm | message_parser
