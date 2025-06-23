# CrewAI Demo Codes

This folder contains simple CrewAI demonstration codes showing various features and functionalities.

## Code Overview

| File | Functions Demonstrated | Description |
|------|----------------------|-------------|
| `01_basics.py` | Basic Agents, Tasks, Crew | Basic CrewAI setup with outline generator and writer agents for sequential task execution |
| `02_tool.py` | Web Tools Integration | Using SerperDevTool, WebsiteSearchTool, and ScrapeWebsiteTool for research and newsletter creation |
| `03_1_make_custom_tool_yfinance.ipynb` | yfinance Integration | Jupyter notebook showing how to use yfinance library to fetch stock data and financial information |
| `03_2_make_custom_tool.py` | Custom Tool Creation | Creating custom tools with @tool decorator for stock price and financial analysis |
| `04_cutom_tool.py` | Multi-Agent Investment Analysis | Advanced investment analysis system with multiple specialized agents and dynamic task creation |

## Key Features Demonstrated

- **Basic Agent Setup**: Simple agent configuration with roles, goals, and backstories
- **Task Definition**: Creating tasks with descriptions and expected outputs
- **Sequential Processing**: Using CrewAI's sequential process for task execution
- **Tool Integration**: Incorporating external tools (web search, financial data)
- **Custom Tool Creation**: Building custom tools with the @tool decorator
- **Multi-Agent Collaboration**: Complex workflows with multiple specialized agents
- **Dynamic Task Generation**: Creating tasks programmatically based on user input
- **LLM Integration**: Using different language models (OpenAI, Anthropic) for different agents

## Usage Notes

- Most files require API keys (OpenAI, Serper, etc.) to be set in environment variables
- The investment analysis tool (`04_cutom_tool.py`) includes interactive user input
- Tools demonstrate Korean language output capabilities
- Custom financial tools use yfinance for real-time stock data