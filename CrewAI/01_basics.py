from crewai import Agent, Task, Crew, LLM
import os

from dotenv import load_dotenv
#os.environ['OPENAI_API_KEY'] = ""

#목차 설정 에이전트
outline_generator = Agent(
    role='Outline Generator',
    goal='Create structured outlines for articles on given topics. answer in Korean',
    llm = LLM(model = "openai/gpt-4o-mini", max_tokens = 1000),
    backstory='You are an expert at organizing information and creating comprehensive outlines for various subjects.'
)
#본문 작성 에이전트
writer = Agent(
    role='Writer',
    goal='Create engaging content based on research. answer in Korean',
    llm = LLM(model = "openai/gpt-4o-mini", max_tokens = 3000),
    backstory='You are a skilled writer who can transform complex information into readable content.'
)

# Task 정의
outline_task = Task(
    description='Create a detailed outline for an article about AI\'s impact on job markets',
    agent=outline_generator,
    expected_output="""A comprehensive outline covering the main aspects of AI\'s 
    influence on employment"""
)

writing_task = Task(
    description='Write an article about the findings from the research',
    agent=writer,
    expected_output='An engaging article discussing AI\'s influence on job markets'
)

# Crew 정의
ai_impact_crew = Crew(
    agents=[outline_generator, writer],
    tasks=[outline_task, writing_task],
    verbose=True
    #Process=Process.sequential
)

# Crew 실행
result = ai_impact_crew.kickoff()

print(result)

'''
위 코드 실행 시 두 Task가 실행되는데 
이때 Crew에 Process를 따로 정의하지 않으면 기본값은 sequential 이기 때문에 
첫번째 task가 끝나면 이어서 두번째 task가 실행된다. 

또한 첫 번째 task가 완료된 후에 Crew안에 첫번째 task가 만든 결과물이 저장되고,
두 번째 task 실행 시 이를 참고하여 글을 쓰게 된다. 
'''