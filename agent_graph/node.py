from typing import Literal

from info_agent import info_chain
from supervisor import supervisor_chain
from mail_agent import mail_chain, send_mail
from message import message_chain
from langchain_core.messages import HumanMessage, ToolMessage
from state import OverallState
from configs import set_env


set_env()


def supervisor_node(state: OverallState) -> OverallState:
    '''

    :param state:
    :return:
    '''
    messages_as_string = []
    for _ in state['messages']:
        messages_as_string.append(_.content)
    response = supervisor_chain.invoke({'messages_as_string': messages_as_string,
                                        'visible_messages': state['visible_messages']})
    state['visible_messages'].append(response.display_message)
    supervisor_instruction = HumanMessage(content=response.supervisor_message)
    state['messages'].append(supervisor_instruction)
    state['next'] = response.next
    return state


def supervisor_choice(state: OverallState) -> Literal['mail', 'message', 'info']:
    '''

    :param state:
    :return:
    '''
    if state['next'] == 'MAIL':
        return 'mail'
    elif state['next'] == 'info':
        return 'info'
    else:
        return 'message'


def info_node(state: OverallState) -> OverallState:
    '''

    :param state:
    :return:
    '''
    query = state['messages'][-1].content
    employer_name = state['name']
    response = info_chain.invoke({
        'query': query,
        'employer_name': employer_name
    })
    query_response = HumanMessage(content= response.info_message)
    state['messages'].append(query_response)
    return state


def mail_node(state: OverallState) -> OverallState:
    '''

    :param state:
    :return:
    '''
    supervisor_instruction = state['messages'][-1].content
    response = mail_chain.invoke({
        'visible_messages': state['visible_messages'],
        'employer_name': state['name'],
        'employer_email': state['email'],
        'supervisor_instruction': supervisor_instruction
    })
    state['messages'].append(response)
    return state


def choose_tools_or_messages(state: OverallState) -> Literal['message', 'mail_tool']:
    '''

    :param state:
    :return:
    '''
    last_message = state['messages'][-1]
    if last_message.tool_calls:
        return 'mail_tool'
    else:
        state['messages'].append(HumanMessage(content='Mail node failed to call the mail tool'))
        return 'message'


def mail_tool_node(state: OverallState) -> OverallState:
    '''

    :param state:
    :return:
    '''
    for tool_call in state["messages"][-1].tool_calls:
        tool = send_mail
        observation = tool.invoke(tool_call["args"])
        tool_result = (ToolMessage(content=observation, tool_call_id=tool_call["id"]))
        state["messages"].append(tool_result)
    return state


def message_node(state: OverallState) -> OverallState:
    '''

    :param state:
    :return:
    '''
    invisible_conversation = []
    for _ in state['messages']:
        invisible_conversation.append(_.content)
    visible_conversation = state['visible_messages']
    response = message_chain.invoke({
        'visible_conversation': visible_conversation,
        'invisible_conversation': invisible_conversation

    })
    state['visible_messages'].append(response.chat_response)
    state['messages'].append(HumanMessage("Responded to the employer with the message:" + response.chat_response))
    return state
