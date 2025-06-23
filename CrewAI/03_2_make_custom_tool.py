import os
import warnings
warnings.filterwarnings('ignore')
from crewai_tools import tool
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

# yfinance 라이브러리로 최근 종가 불러오는 Tool 만들기
@tool
def latest_stock_price(ticker):
    """
    주어진 주식 티커에 대한 최근 종가를 가져오는 툴
    """
    ticker = yf.Ticker(ticker)
    historical_prices = ticker.history(period='5d', interval='1d')
    latest_price = historical_prices['Close']
    return (latest_price)

print(">>>1. Getting Stock Prices Of Apple ==================")
print(latest_stock_price.run("AAPL"))

# yfinance 라이브러리로 재무제표 불러오는 Tool 만들기
@tool
def financial_analysis(ticker):
    """
    연간 재무제표의 주요 정보 가져오는 툴
    """       
    ticker = yf.Ticker(ticker)
    annual_financials = ticker.get_financials()
    summary = {}
    for date, data in annual_financials.items():
        date_str = date.strftime('%Y-%m-%d')
        summary[date_str] = {
            "총수익": data.get('TotalRevenue'),
            "영업이익": data.get('OperatingIncome'),
            "순이익": data.get('NetIncome'),
            "EBITDA": data.get('EBITDA'),
            "EPS(희석)": f"${data.get('DilutedEPS'):.2f}" if pd.notna(data.get('DilutedEPS')) else "N/A"
        }
    return summary


print(">>>2. Getting Financial Analysis Of Apple ============")
print(financial_analysis.run("AAPL"))

# 툴의 별칭을 붙혀주는 방법 (기본적으로는 함수명이 툴의 이름이 됨)
@tool("Updated Comprehensive Stock Analysis")
def comprehensive_stock_analysis(ticker: str) -> str:
    """
    주어진 주식 티커에 대한 업데이트된 종합적인 재무 분석을 수행합니다.
    최신 주가 정보, 재무 지표, 성장률, 밸류에이션 및 주요 비율을 제공합니다.
    가장 최근 영업일 기준의 데이터를 사용합니다.
    
    :param ticker: 분석할 주식의 티커 심볼
    :return: 재무 분석 결과를 포함한 문자열
    """
    def format_number(number):
        if number is None or pd.isna(number):
            return "N/A"
        return f"{number:,.0f}"

    def calculate_growth_rate(current, previous):
        if previous and current and previous != 0:
            return (current - previous) / abs(previous) * 100
        return None

    def format_financial_summary(financials):
        summary = {}
        for date, data in financials.items():
            date_str = date.strftime('%Y-%m-%d')
            summary[date_str] = {
                "총수익": format_number(data.get('TotalRevenue')),
                "영업이익": format_number(data.get('OperatingIncome')),
                "순이익": format_number(data.get('NetIncome')),
                "EBITDA": format_number(data.get('EBITDA')),
                "EPS(희석)": f"${data.get('DilutedEPS'):.2f}" if pd.notna(data.get('DilutedEPS')) else "N/A"
            }
        return summary

    ticker = yf.Ticker(ticker)
    historical_prices = ticker.history(period='1d', interval='1m')
    latest_price = historical_prices['Close'].iloc[-1]
    latest_time = historical_prices.index[-1].strftime('%Y-%m-%d %H:%M:%S')

    # 연간 및 분기별 재무제표 데이터 가져오기
    annual_financials = ticker.get_financials()
    quarterly_financials = ticker.get_financials(freq="quarterly")

    # 주요 재무 지표 (연간)
    revenue = annual_financials.loc['TotalRevenue', annual_financials.columns[0]]
    cost_of_revenue = annual_financials.loc['CostOfRevenue', annual_financials.columns[0]]
    gross_profit = annual_financials.loc['GrossProfit', annual_financials.columns[0]]
    operating_income = annual_financials.loc['OperatingIncome', annual_financials.columns[0]]
    net_income = annual_financials.loc['NetIncome', annual_financials.columns[0]]
    ebitda = annual_financials.loc['EBITDA', annual_financials.columns[0]]
    
    # 주요 비율 계산
    gross_margin = (gross_profit / revenue) * 100 if revenue != 0 else None
    operating_margin = (operating_income / revenue) * 100 if revenue != 0 else None
    net_margin = (net_income / revenue) * 100 if revenue != 0 else None
    
    # 성장성 지표 계산 (연간)
    revenue_growth = calculate_growth_rate(revenue, annual_financials.loc['TotalRevenue', annual_financials.columns[1]])
    net_income_growth = calculate_growth_rate(net_income, annual_financials.loc['NetIncome', annual_financials.columns[1]])

    # 주당 지표
    diluted_eps = annual_financials.loc['DilutedEPS', annual_financials.columns[0]]
    
    # 분기별 데이터 분석
    quarterly_revenue = quarterly_financials.loc['TotalRevenue', quarterly_financials.columns[0]]
    quarterly_net_income = quarterly_financials.loc['NetIncome', quarterly_financials.columns[0]]
    
    quarterly_revenue_growth = calculate_growth_rate(
        quarterly_revenue, 
        quarterly_financials.loc['TotalRevenue', quarterly_financials.columns[1]]
    )
    quarterly_net_income_growth = calculate_growth_rate(
        quarterly_net_income, 
        quarterly_financials.loc['NetIncome', quarterly_financials.columns[1]]
    )

    return {
        "현재 주가":{
            "현재 주가": latest_price,
            "기준 시간": latest_time
        },
        "연간 데이터": {
            "매출": format_number(revenue),
            "매출원가": format_number(cost_of_revenue),
            "매출총이익": format_number(gross_profit),
            "영업이익": format_number(operating_income),
            "순이익": format_number(net_income),
            "EBITDA": format_number(ebitda),
            "매출총이익률": f"{gross_margin:.2f}%" if gross_margin is not None else "N/A",
            "영업이익률": f"{operating_margin:.2f}%" if operating_margin is not None else "N/A",
            "순이익률": f"{net_margin:.2f}%" if net_margin is not None else "N/A",
            "매출 성장률": f"{revenue_growth:.2f}%" if revenue_growth is not None else "N/A",
            "순이익 성장률": f"{net_income_growth:.2f}%" if net_income_growth is not None else "N/A",
            "희석주당순이익(EPS)": f"${diluted_eps:.2f}" if diluted_eps is not None else "N/A",
        },
        "분기 데이터": {
            "매출": format_number(quarterly_revenue),
            "순이익": format_number(quarterly_net_income),
            "매출 성장률(QoQ)": f"{quarterly_revenue_growth:.2f}%" if quarterly_revenue_growth is not None else "N/A",
            "순이익 성장률(QoQ)": f"{quarterly_net_income_growth:.2f}%" if quarterly_net_income_growth is not None else "N/A",
        },
        "연간 재무제표 요약": format_financial_summary(annual_financials),
        "분기별 재무제표 요약": format_financial_summary(quarterly_financials),
    }


print(">>>3. Getting Comprehensive Stock Analysis Of Apple ==")
print(comprehensive_stock_analysis.run("AAPL"))

'''
CrewAI tool 정의 3가지 필수요소 
1. @tool
2. doc string: 툴 함수를 시작에 함수에 대한 설명을 적어두는 것. Agent가 이것을 읽고 함수를 사용한다. (없으면 오류남)
3. 함수 안에서의 로직

위 코드는 실행해도 바로 종료된다! 
왜냐하면 @tool로 감싼 함수들은 CLI 형 툴로 인식되어 “명령 줄”에서 바로 실행할 수 있는 독립 프로그램 형태의 스크립트처럼 작동한다. 

flowchart LR
    A[스크립트 시작] --> B[@tool 래퍼 진입]
    B --> C[함수 로직 실행 → 결과 반환]
    C --> D[결과 출력]
    D --> E[sys.exit() 호출 → 프로세스 종료]
'''