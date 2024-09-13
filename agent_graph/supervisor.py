from langchain_openai import ChatOpenAI
from configs import deepseek_api_key, set_env
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

if __name__ == '__main__':
    set_env()
    result = supervisor_llm.invoke("hello, who are you")
    print(result)