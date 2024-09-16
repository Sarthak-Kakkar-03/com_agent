from langchain_openai import ChatOpenAI
from configs import set_env, deepseek_api_key


set_env()

mail_llm = ChatOpenAI(
    model='deepseek-chat',
    openai_api_key=deepseek_api_key,
    openai_api_base='https://api.deepseek.com/v1',
    temperature=1.0,
    # max_tokens=8192,
    timeout=None,
    max_retries=2,
    api_key=deepseek_api_key
)