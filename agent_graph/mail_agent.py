import smtplib

from langchain_core.messages import AIMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from pydantic.v1 import BaseModel, Field

from configs import set_env, deepseek_api_key, bot_mail_id, bot_mail_password
from langchain_core.tools import tool

set_env()


@tool
def send_mail(content: str, receiver_id: str):
    '''
    Sends an email containing the content to the provided receiver id
    :param content: the content to send within the mail
    :param receiver_id: the id of the receiver
    :return:
    '''
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(bot_mail_id, bot_mail_password)
    message = content
    s.sendmail(bot_mail_id, receiver_id, message)
    s.quit()


tools = [send_mail]
tool_node = ToolNode(tools)

mail_llm = ChatOpenAI(
    model='deepseek-chat',
    openai_api_key=deepseek_api_key,
    openai_api_base='https://api.deepseek.com/v1',
    temperature=1.0,
    # max_tokens=8192,
    timeout=None,
    max_retries=2,
    api_key=deepseek_api_key
).bind_tools(tools)


class MailResponse(BaseModel):
    content_summary: str = Field(description="A message summarizing the content sent in the mail")


mail_parser = PydanticOutputParser(pydantic_object=MailResponse)

mail_prompt = PromptTemplate(
    template=(
        "You are an AI system assisting Sarthak Kakkar in professional communication with a potential employer. "
        "Your task is to generate a polished summary of the following conversation for an email. "
        "Please adhere strictly to the provided formatting guidelines and address the summary to "
        "sarthakkakkar2021@gmail.com.\n\n"
        "Make sure to add Employer Name: {employer_name} and Employer Email: {employer_email} in the mail.\n"
        "Conversation Details:\n{messages_as_strings}\n\n"
        "Formatting Instructions:\n{format_instructions}\n"
    ),
    input_variables=['messages_as_strings', 'employer_name', 'employer_email'],
    partial_variables={"format_instructions": mail_parser.get_format_instructions()}
)


mail_chain = mail_prompt | mail_llm | mail_parser


