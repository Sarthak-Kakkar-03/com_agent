from langgraph.graph import StateGraph
from node import *
from configs import set_env


set_env()

workflow = StateGraph(OverallState)
workflow.add_node("mail", mail_node)
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("info", info_node)
workflow.add_node("message", message_node)
workflow.add_node("mail_tool", mail_tool_node)
workflow.add_edge("__start__", "supervisor")
workflow.add_conditional_edges("supervisor", supervisor_choice)
workflow.add_conditional_edges("mail", choose_tools_or_messages)
workflow.add_edge("info", "message")
workflow.add_edge("mail_tool", "message")
workflow.add_edge("message", "__end__")


if __name__ == '__main__':
    com_agent = workflow.compile()
    result = com_agent.invoke({
        'messages': [HumanMessage('''tell me about sarthak's proficiency in python''')],
        'name': 'TEST_EMPLOYER1',
        'email': 'blahblah@gmail.com',
        'visible_messages': ['''tell me about sarthak's proficiency in python'''],
        'latest_info': '',
        'next': 'supervisor'
    })
    print(result)