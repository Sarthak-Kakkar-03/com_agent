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
    :return: Returns True if mail sent successfully, otherwise False
    '''
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(bot_mail_id, bot_mail_password)
        message = content
        s.sendmail(bot_mail_id, receiver_id, message)
        s.quit()
        return "Email sent"
    except Exception as e:
        print(f"Failed to send email: {e}")
        return "Failed to send email"


tools = [send_mail]
tool_node = ToolNode(tools)

mail_llm = ChatOpenAI(
    model='deepseek-chat',
    openai_api_key=deepseek_api_key,
    openai_api_base='https://api.deepseek.com',
    temperature=1.0,
    # max_tokens=8192,
    timeout=None,
    max_retries=2,
    api_key=deepseek_api_key
).bind_tools(tools, tool_choice='send_mail')


class MailResponse(BaseModel):
    content_summary: str = Field(description="Summary of the mail you sent and its content")


mail_parser = PydanticOutputParser(pydantic_object=MailResponse)

mail_prompt = PromptTemplate(
    template=(
        "You are an AI system assisting Sarthak Kakkar in professional communication with a potential employer. "
        "Your task is to draft a polished email based on the following instruction:\n {supervisor_instruction}\n\n "
        "Compose the email as an AI entity, assuming it was the employers request to you."
        "Please adhere strictly to the provided formatting guidelines and address the summary to "
        "sarthakkakkar2021@gmail.com.\n\n"
        "Make sure to add Employer Name: {employer_name} and Employer Email: {employer_email} in the mail.\n"
        "Conversation Log until now:\n{visible_messages}\n\n"
        # "Formatting Instructions:\n{format_instructions}\n"
    ),
    input_variables=['visible_messages', 'employer_name', 'employer_email', 'supervisor_instruction'],
    partial_variables={"format_instructions": mail_parser.get_format_instructions()}
)


mail_chain = mail_prompt | mail_llm

if __name__ == '__main__':
    result = mail_chain.invoke({
        'visible_messages': 'tell sarthak to reach out to me',
        'employer_name': 'Holdman',
        'employer_email': 'holdman@gmail.com',
        'supervisor_instruction': '''
        Prepare an email to Sarthak Kakkar with the employer's request for him to reach out, and include a summary of the conversation so far.'''
    })
    print(result)


