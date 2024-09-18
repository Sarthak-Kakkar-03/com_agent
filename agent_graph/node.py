from typing import Literal

from info_agent import info_chain
from supervisor import supervisor_chain
from mail_agent import *
from message import message_chain
from langchain_core.messages import HumanMessage, ToolMessage
from state import OverallState
from configs import set_env


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
    state['visible_messages'].append("Bot_Message: " + response.display_message)
    supervisor_instruction = HumanMessage(content=response.supervisor_message)
    state['messages'].append(supervisor_instruction)
    state['next'] = response.next
    state['latest_info'] = 'No info collected'
    return state


def supervisor_choice(state: OverallState) -> Literal['mail', 'message', 'info']:
    '''

    :param state:
    :return:
    '''
    if state['next'] == 'MAIL':
        return 'mail'
    elif state['next'] == 'INFO':
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
    communication_message = HumanMessage(content=response.message)
    state['messages'].append(communication_message)
    state['latest_info'] = response.info_message
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
    print(last_message)
    if last_message.tool_calls:
        print('tool call found')
        message_content = '\n'.join(state['visible_messages'])
        message = f'''A mail was generated for mail id: {state['email']} and name: {state['name']}, 
        with the following conversation:
        {message_content}'''
        send_direct_mail(message, 'sarthakkakkar2021@gmail.com')
        return 'mail_tool'
    else:
        print('tool call not found')
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
        'invisible_conversation': invisible_conversation,
        'info': state['latest_info'],
        'employer_name': state['name']

    })
    state['visible_messages'].append("Bot_Message: " + response.chat_response)
    state['messages'].append(HumanMessage("Responded to the employer with the message:" + response.chat_response))
    return state
