# mail_agent.py
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from pydantic.v1 import BaseModel, Field
from langchain_core.tools import tool
from .information import PROFILE_OWNER_EMAIL, PROFILE_OWNER_NAME
from .settings import settings

settings.export_to_environ()
deepseek_api_key = settings.DEEPSEEK_API_KEY
bot_mail_id = settings.BOT_MAIL_ID
bot_mail_password = settings.BOT_MAIL_PASSWORD
logger = logging.getLogger(__name__)


def _smtp_send_plaintext(
    content: str,
    receiver_email: str,
    subject: Optional[str] = None,
    sender_email: Optional[str] = None,
) -> str:
    """
    Internal helper to send a plaintext email via Gmail SMTP with TLS.
    Returns a short status string.
    """
    sender = sender_email or bot_mail_id
    try:
        # Create message
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = receiver_email
        msg["Subject"] = subject or "Notification"

        msg.attach(MIMEText(content, "plain"))

        # Send via Gmail SMTP
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(sender, bot_mail_password)
        s.sendmail(sender, receiver_email, msg.as_string())
        s.quit()
        return "Email sent"
    except Exception as e:
        logger.exception("Failed to send email")
        return f"Failed to send email: {e}"


@tool
def send_mail(content: str, receiver_id: str) -> str:
    """
    Tool: Send an email with the given content to receiver_id.
    Returns a short status string.
    """
    return _smtp_send_plaintext(content=content, receiver_email=receiver_id, subject="Requested Email")


def send_direct_mail(content: str, receiver_id: str) -> str:
    """
    Direct helper (non-tool) to send a structured 'Mail generated' notification.
    Returns a short status string.
    """
    return _smtp_send_plaintext(
        content=content,
        receiver_email=receiver_id,
        subject="Mail generated notification",
    )


# Expose a ToolNode for LangGraph tool execution (if you want to wire it directly)
tools = [send_mail]
tool_node = ToolNode(tools)


class MailResponse(BaseModel):
    content_summary: str = Field(
        description="Summary of the mail you sent and its content"
    )


mail_parser = PydanticOutputParser(pydantic_object=MailResponse)

mail_prompt = PromptTemplate(
    template=(
        f"You are an AI system assisting {PROFILE_OWNER_NAME} in professional communication with a potential employer.\n"
        "Your task is to draft a clear, professional email based on the following instruction:\n"
        "{supervisor_instruction}\n\n"
        "Compose the email as an AI entity acting on the employer's request to you.\n"
        f"Address the summary to {PROFILE_OWNER_EMAIL}.\n\n"
        "Include:\n"
        "- Employer Name: {employer_name}\n"
        "- Employer Email: {employer_email}\n\n"
        "Conversation log so far:\n{visible_messages}\n"
    ),
    input_variables=[
        "visible_messages",
        "employer_name",
        "employer_email",
        "supervisor_instruction",
    ],
    # Keeping parser handy if you later choose to parse; for now chain returns text
    partial_variables={"format_instructions": mail_parser.get_format_instructions()},
)

mail_llm = ChatOpenAI(
    model="deepseek-chat",
    openai_api_key=deepseek_api_key,
    openai_api_base="https://api.deepseek.com",
    temperature=1.0,
    timeout=None,
    max_retries=2,
    api_key=deepseek_api_key,
).bind_tools(tools, tool_choice="send_mail")

# The LLM will emit a tool call (send_mail) when appropriate.
mail_chain = mail_prompt | mail_llm


