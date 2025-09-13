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
    message: str = Field('Message to the agent which is going to frame a response for the employer, using the '
                         'information you provided')


info_parser = PydanticOutputParser(pydantic_object=InfoResponse)


info_prompt = PromptTemplate(
    template=(
        '''
       Sarthak Kakkar
+1 (857) 313 2670 | kakkar.sar@gmail.com | linkedin.com/in/sarthakkakkar03 | https://skakkar.netlify.app/
EDUCATION
Bachelor of Science in Computer Science | Business Administration minor
Northeastern University, Khoury College of Computer Science | Boston, MA | GPA: 3.70 | 05/2026
WORK EXPERIENCE
Movement NeuroScience Lab | Boston, USA | 01/2025 - 06/2025
Embedded Systems Engineer Co-op | Full-time
• Engineered C++/Python embedded system with BLE stimulators & force sensors, enabling real-time IRB-approved human subject experiments.
• Re-architected vendor API into async modular framework, boosting portability across 3+ projects and enabling live control stimulation.
• Reverse-engineered undocumented BLE hardware and created Python APIs for real-time data streaming and device control.
• Automated end-to-end pipelines from raw sensor input to clinician-ready visualizations, producing research-grade reports for federal trials.
Northeastern University | Boston, USA | 09/2024 - 12/2024
Teaching Assistant - Programming in C++ | Part-time
• Taught over 100 students advanced C++ (OOP, memory management, smart pointers), optimizing course-wide Linux development workflows.
• Delivered independent lecture on smart pointers with live coding demos, simplifying complex memory-safe design for large student audiences.
• Debugged and optimized student projects, resolved Khoury Linux server issues, and streamlined productivity across multiple course sections.
Wissen Infotech | Bangalore, India | 06/2024 - 08/2024
LLMOps Intern | Full-time
• Built Python code-conversion accelerator projected to reduce enterprise migration timelines by 2–3 months across global client systems.
• Designed LangChain/LangGraph feedback loop for autonomous error detection, targeted regeneration, and recovery, boosting pipeline efficiency.
• Drove LLM adoption by delivering technical prototypes/demos to executives and prospective clients, influencing high-level business strategy.
• Benchmarked OpenAI, DeepSeek, and GenAI models; authored comprehensive reports that guided internal adoption and client recommendations.
Applify Tech Private Limited | Mohali, India | 07/2023 - 08/2023
Intern | Full-time
• Developed Java backend services with REST APIs, SQL queries, and JDBC integration, strengthening scalability and production reliability.
• Implemented JaCoCo unit tests and debugged production code, improving release stability and reducing runtime issues.
• Collaborated in an agile environment using Git and JIRA, documenting workflows and aligning sprint goals with client needs.
PROJECTS
Squegg Python API
• Reverse-engineered the BLE protocol of the Squegg smart squeeze ball, enabling seamless desktop integration for analytics and control.
• Built open-source Python API streaming grip strength, battery status, and notifications, delivering reliable real-time device monitoring.
• Packaged tool with PyInstaller into a cross-platform executable, deployed in medical research labs for clinician-ready data access.
Typographic Latent Space (ICLR 2023 Publication)
• Co-authored ICLR 2023 paper mapping digit latent space using β-VAE, advancing generative design and representation research.
• Implemented automated PyTorch training loops with reproducible configs, metadata, and labeled sample grids for validation.
• Explored latent structure through controllable sampling of generative factors, revealing design patterns and model transparency.
AI Powered Communication Assistant
• Designed AI workflow handling professional profile inquiries, improving communication efficiency and response automation.
• Implemented real-time AI alerts including inquirer details (name, email), enabling targeted and timely follow-up engagement.
• Built with LangChain, LangGraph, and LangServe using supervisor architecture, ensuring scalable orchestration of AI pipelines.
Portfolio Website
• Built a responsive portfolio with React, React Router, and Tailwind CSS, featuring polished GSAP animations and smooth transitions.
• Implemented dark/light mode and modular JSON-based content architecture, ensuring fast updates and scalability.
• Deployed on Netlify with continuous integration and automated Git builds, streamlining deployment and publishing workflows.
EcoSim: Dynamic Predator-Prey Ecosystem Simulation
• Developed C++ OOP simulation (inheritance, polymorphism) to model predator–prey dynamics with accurate ecosystem variability.
• Added critter behaviors simulating realistic movement, interactions, and emergent environmental complexity.
• Deployed and fine-tuned simulation on Khoury Linux servers, ensuring performance stability and showcasing scalable C++ design.
Snake Game
• Developed a Snake Game with a Command Line Interface using the Ncurses library in C++.
• Introduced dynamic gameplay with randomly placed, size-varying food items, evolving obstacles, and adaptive difficulty.
• Deployed on the Khoury Linux Server with version control and collaboration through GitHub.
Industry Practicum - PawtoGrader Platform (Ongoing)
• Undertook an exclusive practicum project, collaborating in a 6-person Agile team to extend PawtoGrader for 3k+ Khoury College CS students.
• Serve as client liaison with Dr. Jonathan Bell, gathering requirements, aligning priorities, and translating needs into technical deliverables.
• Contribute as a full-stack developer using TypeScript, SurveyJS, and Supabase, delivering surveys, dashboards, and automated group formation.
Calendar App
• Developed a Java-based calendar application with a weekly view, secured access via password, a progress tracker, and the classification of tasks and
events.
• Configured the application with a graphical user interface using JavaFX that allows customizable themes.
Battleship Game
• Created a Battleship game in Java with player-vs-algorithm and automated algorithm-vs-algorithm modes.
• Structured the application with JSON data handling and the Proxy Design Pattern for maintainability.
• Configured Gradle build automation with JaCoCo integration, achieving over 90% unit test coverage.
PUBLICATIONS
Mapping the Typographic Latent Space of Digits | 04/2023
International Conference for Learning Representations
Used disentangled Beta-VAE's in an unsupervised learning approach to map latent feature spaces with a dataset of MNIST Style Typographic Images across
2990 unique font styles, helping typographers explore new attributes for their classification systems.
SKILLS
Programming Languages: C++, Java, JavaScript, OCaml, Python, SQL, TypeScript
Frameworks & Libraries: LangChain, LangGraph, Matplotlib, NumPy, Pandas, PyTorch, React, scikit-learn, Tailwind CSS
Systems & Tools: Git, GitHub, JIRA, Linux, Netlify, Streamlit
Software Development: Agile, API Development, Async Programming, CI/CD, Object-Oriented Design (OOD), Unit Testing
Machine Learning & Data Science: Data Visualization, Deep Learning, PCA, Random Forest, Regression
Embedded Systems: Arduino, Asynchronous & Event-Driven Architectures, BLE, Raspberry Pi, USB HID, Wireless & IoT Integration
Frontend & Web Development: HTML5, Next.js, React, React Router DOM, RESTful APIs, Server-Side Development, State Management, Tailwind CSS
Backend Development: Authentication & Authorization, Database Integration, Express.js, Flask, RESTful API Design, Server-Side Development
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