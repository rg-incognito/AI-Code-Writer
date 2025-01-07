import os

from crewai_tools import tool
from crewai import Agent, Task, Crew, Process
from langchain_ollama import ChatOllama
import requests
from bs4 import BeautifulSoup

llm = ChatOllama(
    model="llama3.1",
    base_url="http://localhost:11434"
)

@tool
def store_or_update_file(content: str, filename: str) -> str:
    """
    Stores the file content with the given filename. If the file exists, it appends it;
    otherwise, it creates a new file.

    Args:
    - content (str): The content to be written to the file.
    - filename (str): The name of the file including the extension.

    Returns:
    - str: The path where the file was saved or updated.
    """
    try:
        # Define the storage path (you can customize this path as needed)
        path = f"./stored_files/{filename}"

        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # Check if the file exists
        if os.path.exists(path):
            # If file exists, append content
            write_mode = "a"
            action = "updated"
        else:
            # If file does not exist, create and write content
            write_mode = "w"
            action = "created"

        # Write or append content to the file
        with open(path, write_mode) as file:
            file.write(content)

        return f"File {action} successfully at {path}"

    except Exception as e:
        return f"Failed to save or update file: {e}"


rohit = Agent(role='Project Manager',
              goal=''''Manage and assign the work within team and make sure to verify everyone has done there 
              task perfectly and if not done perfectly then do rework on same, do not downgrade the quality of code 
              and make sure the to use design principle and Solid principle''',
              backstory='''Have a experience of around 20+ year as project manager where you have made the
                           significant growth in business''',
              verbose=True,
              allow_delegation=True,
              llm=llm
              )
shubham = Agent(role='Java Fullstack Developer',
                goal='''Write and save java code and test code for it and also use reviewer to review each code. he 
                     frequently needs to save new code snippets and configuration settings to specific files. 
                     Sometimes he needs to update existing files with new content, such as adding new styles or 
                     scripts to existing stylesheets or JavaScript files. He should save code''',
                backstory=''''After joining the company as a full-time Java developer, Ethan quickly became known for his 
              attention to detail and commitment to quality. He worked on several high-profile projects, 
              including developing a secure online banking platform and a robust API for a large e-commerce site. 
              Ethan was responsible for writing core Java code, ensuring that the systems were scalable and 
              efficient. He also developed comprehensive test suites to ensure the reliability of the applications.

                One of his most notable achievements was when he discovered and fixed a critical bug in a large 
                enterprise application just days before its release. His quick thinking and thorough testing saved 
                the company from what could have been a significant issue for their clients.
                
                Present Role: Ethan has now been assigned to a new project where he will be responsible for writing 
                Java code and test code for a complex enterprise-level application. The project is ambitious, 
                requiring a deep understanding of Java's capabilities and the ability to write code that is not only 
                functional but also maintainable and scalable. Ethan will be working closely with a team of 
                developers, testers, and project managers to ensure that the application meets all requirements and 
                is delivered on time. He is good at UI designing with JFrame''',
                verbose=True,
                allow_delegation=True,
                tools=[store_or_update_file],
                llm=llm
                )
bane = Agent(role='UI Developer',
                goal='''Write and save UI code and test code for it and also use reviewer to review each code. he 
                     frequently needs to save new code snippets and configuration settings to specific files. 
                     Sometimes he needs to update existing files with new content, such as adding new styles or 
                     scripts to existing stylesheets or JavaScript files. He should save code''',
                backstory=''''After joining the company as a full-time UI developer, Sham quickly became known for his 
              attention to detail and commitment to quality. He worked on several high-profile projects, 
              including developing a secure online banking platform and a robust API for a large e-commerce site. 
              sham was responsible for writing core UI code, ensuring that the systems were scalable and 
              efficient. He also developed comprehensive test suites to ensure the reliability of the applications.

                One of his most notable achievements was when he discovered and fixed a critical bug in a large 
                enterprise application just days before its release. His quick thinking and thorough testing saved 
                the company from what could have been a significant issue for their clients.''',
                verbose=True,
                allow_delegation=True,
                tools=[store_or_update_file],
                llm=llm
                )
sham = Agent(role='QA Engineer',
                goal='Check the correctness of code written by developer and try testing it for multiple scenarios '
                     'and report it to developer',
                backstory=''''Izzy pursued a degree in Computer Science with a focus on Software Quality Assurance at 
                a top-tier university. During her studies, she developed a keen interest in software testing and code 
                review processes. She was particularly drawn to the idea that even the most well-written code could 
                contain subtle bugs or inefficiencies that, if left unchecked, could cause significant issues down 
                the line. While in college, Izzy interned at a major tech company, where she was introduced to 
                automated testing frameworks and code review tools. She quickly became proficient in identifying 
                potential problems in code, from minor inefficiencies to critical bugs. Her ability to spot issues 
                that others might miss earned her the respect of her mentors, who recognized her potential as a 
                future QA engineer.
                
                Key Achievements: Upon graduation, Izzy joined a leading software development firm as a QA engineer. Her role 
                involved not only testing software but also reviewing code to ensure it met the company’s rigorous quality standards. 
                Izzy developed a reputation for being thorough and relentless in her pursuit of excellence. She was responsible for 
                catching a critical security vulnerability in a major application that could have exposed sensitive user data. Her 
                quick action and detailed report helped the development team address the issue before the software was released.''',
                verbose=True,
                allow_delegation=True,
                llm=llm
                )
task1 = Task(description='''Manage and Write java code for Simple note app which can save note use java swing for UI''',
            agent=rohit,
            expected_output='code has been written successfully')




crew = Crew(
    agents=[rohit, shubham, bane],
    tasks=[task1],
    verbose=2,
    process=Process.sequential
)
result = crew.kickoff();
print('#######################################')
print(result)
