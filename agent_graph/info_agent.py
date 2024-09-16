from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from configs import deepseek_api_key, set_env
from langchain_core.pydantic_v1 import BaseModel, Field

set_env()

info_llm = ChatOpenAI(
    model='deepseek-chat',
    openai_api_key=deepseek_api_key,
    openai_api_base='https://api.deepseek.com/beta',
    temperature=1.0,
    max_tokens=8192,
    timeout=None,
    max_retries=2,
    api_key=deepseek_api_key
)


class InfoResponse(BaseModel):
    info_message: str = Field(description="A concise message, giving the information requested")


info_parser = PydanticOutputParser(pydantic_object=InfoResponse)


info_prompt = PromptTemplate(
    template=(
        '''
        Sarthak Kakkar
+1 (857) 313 2670
kakkar.sa@northeastern.edu
linkedin.com/in/sarthakkakkar03
https://skakkarsportfolio.netlify.app/
Availability: January 2024 - July 2024
Education
Bachelor of Science in Computer Science
Northeastern University, Khoury College of Computer Science
Boston, MA
GPA: 3.73
05/2026
Work Experience
Northeastern University
Boston, USA
09/2024 - Present
Teaching Assistant
Part-time
Provided personalized support to students, working as a Teaching Assistant for the Programming in C++ course at Northeastern University.

Hosted weekly virtual and in-person office hours, assisting students with their C++ projects. Improved student performance and comprehension.

Graded projects, and assignments for a class of more than 100 students, resulting in a more organized and efficient classroom environment.

Wissen Infotech
Bangalore, India
06/2024 - 08/2024
LLMOps Intern
Full-time
Designed an LLM-powered accelerator, advancing AI-driven automation, and projected to reduce processing times by 2-3 months.

Designed and deployed a multi-agent system for automated testing and error correction, enhancing reliability and precision.

Built a dynamic, chain-based codebase that boosted testing and production efficiency by 30%.

Led research initiatives to fine-tune Large Language Models for specialized tasks, optimizing model performance for industry applications.

Applify Tech Private Limited
Mohali, India
07/2023 - 08/2023
Intern
Full-time
Developed a backend in Java with JDBC while learning the implementation of Agile methodology using a JIRA board.

Optimized structure management and client communications, leading to a 25% reduction in errors and a more cohesive productive team environment.

Facilitated documenting meetings, developed subsequent sprint goals, and presented to various clients.

Pushing the Boundaries with TMNIST
Boston, USA
01/2023 - 04/2023
Author
Collaborated with industry experts to present a study on Mapping the Typographic Latent Space of Digits at the International Conference for Learning Representation.

Effectively presented research findings at RISE, resulting in a 30% increase in inquiries about the research and its applications.

Contributed to the implementation of algorithms like Beta-VAE’s, gaining insight into typographic feature latent space mapping and inspiring potential modifications for PANOSE.

Projects
Portfolio Website
07/2024 - 08/2024
Created a career website using React with dynamic data management through JSON structures.
Deployed the website on Netlify with automatic builds synced to Git pushes.
Improved usability and streamlined updates through efficient integration of front-end and deployment workflows.
EcoSim: Dynamic Predator-Prey Ecosystem Simulation
03/2024 - 04/2024
Developed a C++ simulation featuring advanced OOP for realistic Predator-Prey dynamics, using inheritance and polymorphism.
Added sophisticated behaviors and basic game physics to model critter movements and environmental interactions.
Deployed and fine-tuned the simulation on the Khoury server environment, ensuring performance stability while demonstrating development proficiency.
Random Forest Weather Analysis
01/2024 - 03/2024
Developed a Python-based Random Forest algorithm to categorize and analyze 30 years of Boston's weather data, generating feature importance with approximately 80% accuracy.
Installed data collection from an online weather API and managed subsequent storage using PostgreSQL.
Analyzed a confusion matrix to identify API sensor limitations and frequent misclassifications, leading to augmented accuracy.
Snake Game
02/2024 - 03/2024
Developed a Snake Game with a Command Line Interface using the Ncurses library in C++.
Implemented innovative gameplay elements, such as randomly placed, size-varying food items and evolving obstacles, with complex difficulty modes that dynamically adjust game speed and obstacles.
Collaborated via GitHub to build and deploy the game on Khoury Linux Server.
Calendar App
06/2023 - 07/2023
Developed a Java-based calendar application with a weekly view, secured access via password, a progress tracker, and the classification of tasks and events.
Configured the application with a graphical user interface using JavaFX that allows customizable themes.
Battleship Game
05/2023 - 06/2023
Created a Battleship game in Java that allows players to compete against a smart algorithm in a manual setting.
Implemented an automatic mode, where the program battles against other compatible algorithms.
Designed the application to utilize JSON for data handling and the proxy server design pattern for its architecture.
Publications
Mapping the Typographic Latent Space of Digits
04/2023
International Conference for Learning Representations
Used disentangled Beta-VAE's in an unsupervised learning approach to map latent feature spaces with a dataset of MNIST Style Typographic Images across 2990 unique font styles, helping typographers explore new attributes for their classification systems.

Skills
Languages and Frameworks: C++, Java, JavaScript, Langchain, Langgraph, Python, SQL
System and Tools: IntelliJ IDEA, Jupyter Notebook, Langsmith, Linux, macOS, Pycharm, Vim, Visual Studio, VMware, Windows
Machine Learning & Data Science: Beta-VAE's, Clustering, Matplotlib, Numpy, Pandas, PCA, Random Forest, Regression, Scikit-​Learn
Software Development: Agile, API Development, CI/CD, GDB, Java Database Connectivity, JUnit 5, OOP, Unit Testing
Version Control & Collaboration: Git, GitHub, JIRA, LaTeX
        '''
        "Based on the following request, provide the information requested. If the information wasn't mentioned "
        "above, respond with 'Not available'.\n\n"
        "{query}\n\n"
        "Follow the given format instructions:\n{format_instructions}"
    ),
    input_variables=['query', 'employer_name'],
    partial_variables={"format_instructions": info_parser.get_format_instructions()}

)

info_chain = info_prompt | info_llm | info_parser


if __name__ == '__main__':
    result = info_chain.invoke(
        {'query': ['''Provide information about Sarthak Kakkar.'''],
         'employer_name': 'ABC',
         'email': 'test@mail',
         'display_messages': [''''''],
         'latest_info': 'sarthak knows python'}
    )
    print(result.info_message)