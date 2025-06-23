import os
import warnings
warnings.filterwarnings('ignore')
from dotenv import load_dotenv
#os.environ["SERPER_API_KEY"] = ""  
#os.environ['OPENAI_API_KEY'] = ""

from crewai import Agent, Task, Crew, LLM
from crewai.process import Process
from crewai_tools import (
    SerperDevTool,
    WebsiteSearchTool,
    ScrapeWebsiteTool
)

llm = LLM(model="openai/gpt-4o-mini")  # model: 사용할 언어 모델 이름

# 도구 인스턴스 생성
search_tool = SerperDevTool()        # SerperDevTool: 웹 검색 API 도구. 정보가 있는 웹사이트를 검색
web_rag_tool = WebsiteSearchTool()   # WebsiteSearchTool: 웹사이트 안에서 RAG를 해서 필요한 정보 가져옴. 자동으로 db파일 생성됨
scrap_tool = ScrapeWebsiteTool()     # ScrapeWebsiteTool: 웹 스크래핑 도구

# ─────────────────────────────────────────────────────────────────────────────
# 에이전트 정의: 테크 트렌드 연구원 (AI 최신 기술 조사 및 요약 담당)
researcher = Agent(
    role='테크 트렌드 연구원',  
    # role: 에이전트의 직책 또는 역할 이름
    goal="인공지능 분야의 최신 기술 트렌드를 한국어로 제공합니다. 지금은 2024년 8월입니다.",
    # goal: 에이전트가 달성해야 할 구체적인 목표
    backstory='기술 트렌드에 예리한 안목을 지닌 전문 분석가이자 AI 개발자입니다.',
    # backstory: 에이전트의 배경 스토리 설정
    tools=[search_tool, web_rag_tool],
    # tools: 에이전트가 활용할 외부 도구 리스트
    verbose=True,
    # verbose: 수행 과정 중 세부 로그 출력 여부
    max_iter=5,
    # max_iter: 최대 반복 수행 횟수 제한 / 이 경우에는 웹 검색을 5번만 하도록 제한
    llm=llm
    # llm: 에이전트가 사용할 언어 모델 인스턴스
)

# 에이전트 정의: 뉴스레터 작성자 (조사 결과 기반 뉴스레터 작성 담당)
writer = Agent(
    role='뉴스레터 작성자',
    # role: 에이전트의 직책 또는 역할 이름
    goal="최신 AI 기술 트렌드에 대한 매력적인 테크 뉴스레터를 한국어로 작성하세요. 지금은 2024년 8월입니다.",
    # goal: 에이전트가 달성해야 할 구체적인 목표
    backstory='기술에 대한 열정을 가진 숙련된 작가입니다.',
    # backstory: 에이전트의 배경 스토리 설정
    verbose=True,
    # verbose: 수행 과정 중 세부 로그 출력 여부
    allow_delegation=False,
    # allow_delegation: 하위 에이전트에 업무 위임 허용 여부
    llm=llm
    # llm: 에이전트가 사용할 언어 모델 인스턴스
)

# ─────────────────────────────────────────────────────────────────────────────
# 태스크 정의: AI 최신 기술 동향 조사 및 요약
research = Task(
    description='AI 업계의 최신 기술 동향을 조사하고 요약을 제공하세요.',
    # description: 태스크의 구체적 실행 지시문
    expected_output='AI 업계에서 가장 주목받는 3대 기술 개발 동향과 그 중요성에 대한 신선한 관점을 요약한 글',
    # expected_output: 태스크가 생성해야 할 결과물의 형태
    agent=researcher
    # agent: 이 태스크를 수행할 에이전트 지정
)

# 태스크 정의: 조사 결과 기반 테크 뉴스레터 작성
write = Task(
    description="""테크 트렌드 연구원의 요약을 바탕으로 AI 산업에 대한 매력적인 테크 뉴스레터를 작성하세요.
    테크 뉴스레터이므로 전문적인 용어를 사용해도 괜찮습니다.""",
    # description: 태스크의 구체적 실행 지시문
    expected_output='최신 기술 관련 소식을 이모티콘을 사용하며 재밌는 말투로 소개하는 4문단짜리 마크다운 형식 뉴스레터',
    # expected_output: 태스크가 생성해야 할 결과물의 형태
    agent=writer,
    # agent: 이 태스크를 수행할 에이전트 지정
    output_file=r'./02_new_post.md'  
    # output_file: 생성된 결과물을 저장할 파일 경로
)

# ─────────────────────────────────────────────────────────────────────────────
# Crew 구성: 순차적 실행 방식으로 태스크 연결
crew = Crew(
    agents=[researcher, writer],
    # agents: 크루에 포함될 에이전트 리스트
    tasks=[research, write],
    # tasks: 순서대로 실행할 태스크 리스트
    verbose=True,
    # verbose: 전체 크루 실행 로그 출력 여부
    process=Process.sequential
    # process: 태스크 실행 방식 (sequential: 순차 실행)
)

# ─────────────────────────────────────────────────────────────────────────────
# 크루 실행
result = crew.kickoff()  # kickoff(): 모든 태스크를 지정된 방식으로 실행

print(result)  

'''
테크 트렌드 연구원의 요약문이 Crew 내부의 task 실행 결과로 저장되어있고, 
뉴스레터 작성자는 write task의 설명에 의해 테크 트렌드 연구원의 요약을 참고하여 글을 작성하게된다. 
'''