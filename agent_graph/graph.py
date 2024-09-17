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
        'messages': [HumanMessage('''How is sarthak a good fit for this job: Job Description

As a Software Engineer at Socotec, you will play a pivotal role in our mission to optimize processes and enhance user experiences through the development of robust software solutions. You will collaborate closely with cross-functional teams to identify and address process bottlenecks, architecting and implementing both client-side and server-side structures.

While not mandatory, we highly value candidates with expertise in machine learning (ML) and experience in developing custom chatbot agents. Familiarity with advanced ML techniques, such as model chaining, fine-tuning pre-trained models for specific applications, and implementing function calling, would be a significant advantage. Experience in natural language processing (NLP) and integrating chatbot agents into existing systems would be beneficial and is considered a plus.

Your responsibilities will include:

 Collaborating with Cross-Functional Teams: Work closely with stakeholders from various departments to understand their needs and pain points, translating them into effective software solutions. 
 Architecting Scalable Solutions: Design and develop scalable and maintainable client-side and server-side architectures that meet both current and future needs. 
 Building Engaging Frontend Interfaces: Create visually appealing and intuitive frontend interfaces using modern technologies such as React, ensuring a seamless user experience across devices. 
 Ensuring Software Quality: Conduct rigorous testing to ensure the performance, reliability, and usability of our software products, identifying and addressing any issues that arise. 
 Maintaining and Updating Software: Diagnose and resolve any technical issues that arise post-launch, ensuring our software remains up-to-date with the latest technologies and best practices. 
 Perform all other duties as assigned by your supervisor or manager
 Implementing Security Measures: Implement robust security measures and data protection protocols to safeguard sensitive information and mitigate potential risks. 
 Documentation: Document technical processes and system architecture comprehensively, providing clear and detailed documentation for future reference. 
 Machine Learning and Chatbot Development: Develop and integrate custom chatbot agents, leveraging ML techniques such as model chaining, fine-tuning, and function calling to enhance user interactions and automate processes. 
 Perform all other duties as assigned by your supervisor or manager. 

Qualifications

 Proficiency in programming languages such as JavaScript, TypeScript, Python, and CSS. 
 Experience with frameworks and technologies such as React, Django, FastAPI, AWS (Amazon Web Services), and Microsoft Azure. 
 Familiarity with other relevant technologies and tools such as SQL databases (e.g., PostgreSQL, MySQL), containerization (e.g., Docker, Kubernetes), CI/CD pipelines, and version control systems (e.g., Git, GitHub). 
 Knowledge of agile development methodologies and best practices. 
 Experience in machine learning, particularly in developing and fine-tuning models for specific applications. 
 Expertise in creating and deploying custom chatbot agents using various techniques, including chaining, fine-tuning, and function calling. 

We are looking for a proactive and innovative individual who is passionate about technology and eager to contribute to our team's success. If you have a strong background in software development and are excited about working on cutting-edge projects, we encourage you to apply.
'''), HumanMessage(content='ask sarthak to contact us')],
        'name': 'Goldman Employer',
        'email': '@gmail.com',
        'visible_messages': ['''How is sarthak a good fit for this job: Job Description

As a Software Engineer at Socotec, you will play a pivotal role in our mission to optimize processes and enhance user experiences through the development of robust software solutions. You will collaborate closely with cross-functional teams to identify and address process bottlenecks, architecting and implementing both client-side and server-side structures.

While not mandatory, we highly value candidates with expertise in machine learning (ML) and experience in developing custom chatbot agents. Familiarity with advanced ML techniques, such as model chaining, fine-tuning pre-trained models for specific applications, and implementing function calling, would be a significant advantage. Experience in natural language processing (NLP) and integrating chatbot agents into existing systems would be beneficial and is considered a plus.

Your responsibilities will include:

 Collaborating with Cross-Functional Teams: Work closely with stakeholders from various departments to understand their needs and pain points, translating them into effective software solutions. 
 Architecting Scalable Solutions: Design and develop scalable and maintainable client-side and server-side architectures that meet both current and future needs. 
 Building Engaging Frontend Interfaces: Create visually appealing and intuitive frontend interfaces using modern technologies such as React, ensuring a seamless user experience across devices. 
 Ensuring Software Quality: Conduct rigorous testing to ensure the performance, reliability, and usability of our software products, identifying and addressing any issues that arise. 
 Maintaining and Updating Software: Diagnose and resolve any technical issues that arise post-launch, ensuring our software remains up-to-date with the latest technologies and best practices. 
 Perform all other duties as assigned by your supervisor or manager
 Implementing Security Measures: Implement robust security measures and data protection protocols to safeguard sensitive information and mitigate potential risks. 
 Documentation: Document technical processes and system architecture comprehensively, providing clear and detailed documentation for future reference. 
 Machine Learning and Chatbot Development: Develop and integrate custom chatbot agents, leveraging ML techniques such as model chaining, fine-tuning, and function calling to enhance user interactions and automate processes. 
 Perform all other duties as assigned by your supervisor or manager. 

Qualifications

 Proficiency in programming languages such as JavaScript, TypeScript, Python, and CSS. 
 Experience with frameworks and technologies such as React, Django, FastAPI, AWS (Amazon Web Services), and Microsoft Azure. 
 Familiarity with other relevant technologies and tools such as SQL databases (e.g., PostgreSQL, MySQL), containerization (e.g., Docker, Kubernetes), CI/CD pipelines, and version control systems (e.g., Git, GitHub). 
 Knowledge of agile development methodologies and best practices. 
 Experience in machine learning, particularly in developing and fine-tuning models for specific applications. 
 Expertise in creating and deploying custom chatbot agents using various techniques, including chaining, fine-tuning, and function calling. 

We are looking for a proactive and innovative individual who is passionate about technology and eager to contribute to our team's success. If you have a strong background in software development and are excited about working on cutting-edge projects, we encourage you to apply.
''', 'ask sarthak to contact us'],
        'latest_info': '',
        'next': 'supervisor'
    })
    print(result)