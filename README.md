
# Financial Analysis Agent System

## Overview
The Financial Analysis Agent System is an intelligent system that combines SEC filing analysis with real-time market data to provide comprehensive financial insights. It demonstrates the integration of AI agents with uAgent microservices through the Agentverse platform.

## Key Features
- Team-based AI agent architecture
- Real-time market data analysis
- SEC filing processing with RAG
- Microservice-based tool integration
- Agentverse platform integration

## System Architecture
<img width="636" alt="Screenshot 2025-01-23 at 6 30 42 AM" src="https://github.com/user-attachments/assets/9027f68c-9601-46d3-b509-f0d1a2b65d41" />


### Components
1. **Financial Analysis Agent**
   - Supervisor Agent: Coordinates analysis
   - Search Agent: Handles market research
   - SEC Agent: Analyzes financial documents

2. **Tools Agents**
   - Search Tool : Tavily search API
   - RAG Tool : Provides document analysis through Qdrant vector database

3. **Primary Agent**
   - Routes user queries
   - Manages responses
   - Handles discovery

4. **Frontend**
   - React-based user interface
   - Real-time updates
   - Interactive query system
  
5. **Agentverse**
   - Manages agent communication and discovery
   - Real-time updates
   - Interactive query system
   - All components communicate through Agentverse's message routing system, ensuring decoupled and scalable architecture.

## Prerequisites
- Python 3.8+
- Node.js 14+
- Agentverse account and API key
- Tavily API key
- OpenAI API key

## Environment Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/financial-analysis-agent.git
cd financial-analysis-agent

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Update .env with your API keys
```

Required Environment Variables:
```env
OPENAI_API_KEY=your_openai_key
TAVILY_API_KEY=your_tavily_key
AGENTVERSE_API_KEY=your_agentverse_key
FINANCIAL_AGENT_KEY=your_agent_seed
PRIMARY_AGENT_KEY=your_primary_agent_seed
```

## Running the System

### 1. Start Tool uAgents
```bash
# Start Search Tool uAgent
python src/tool_agents/search_tool/agent.py

# Start RAG Tool uAgent
python src/tool_agents/rag_tool/agent.py
```

### 2. Start Financial Analysis Agent
```bash
python src/agentverse/register.py
```

### 3. Start Primary Agent
```bash
python src/main.py
```

### 4. Start Frontend
```bash
cd frontend
npm install
npm run dev
```

The system will be available at:
- Frontend: http://localhost:5174
- Primary Agent: http://localhost:5001
- Financial Agent: http://localhost:5008
- Search Tool: http://localhost:8000
- RAG Tool: http://localhost:8001

## Usage Guide

### Making Queries
1. Open the frontend interface
2. Enter your financial analysis query
3. The system will:
   - Route your query through the Primary Agent
   - Process it using the Financial Analysis Agent
   - Utilize tool uAgents as needed
   - Return comprehensive analysis

Example Queries:
```
"What are Apple's recent revenue trends?"
"Analyze the risk factors from the latest 10-K"
"Compare current market sentiment with financial metrics"
```

### Understanding Responses
The system provides multi-faceted analysis including:
- SEC filing insights
- Current market data
- Analyst opinions
- Trend analysis

## Project Structure
```
src/
├── agents/                 # AI Agent Components
│   ├── search_agent.py     
│   ├── sec_agent.py        
│   └── supervisor.py       
├── agentverse/
│   └── register.py         # Agent registration
├── tools/           
│   ├── search_tool/        # Search microservice
│   └── rag_tool/          # RAG microservice
└── utils/
    └── helpers.py         # Helper functions
```

## Development Guide

### Adding New Tools
1. Create new tools:
```
src/tools/
├── __init__.py
├── tool3.py       
└── tool4.py       
```

2. Register with Agentverse:
- Generate new agent seed
- Add registration in agent.py
- Update environment variables

3. Update specialist agents to use new tool

### Modifying Agent Behavior
- Supervisor logic in `supervisor.py`
- Specialist behavior in respective agent files
- Tool logic in uAgent implementations

## Troubleshooting

### Common Issues

1. **Connection Errors**
   - Verify all services are running
   - Check port availability
   - Ensure Agentverse connection

2. **Authentication Issues**
   - Verify API keys in .env
   - Check agent seeds
   - Confirm Agentverse registration

3. **Message Flow Issues**
   - Check webhook endpoints
   - Verify message formats
   - Monitor Agentverse logs

### Logs Location
```
logs/
├── financial_agent.log
├── primary_agent.log
├── search_tool.log
└── rag_tool.log
```

## Contributing

1. Fork the repository
2. Create your feature branch
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Commit your changes
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. Push to the branch
   ```bash
   git push origin feature/amazing-feature
   ```
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- [Fetch.ai](https://fetch.ai/) for Agentverse platform
- [LangChain](https://langchain.com/) for agent frameworks
- [Tavily](https://tavily.com/) for search API
- OpenAI for language models

## Contact
Rajashekar Vennavelli rajashekarvennavelli@gmail.com

