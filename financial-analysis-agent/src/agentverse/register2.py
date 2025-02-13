import os
import logging
from fetchai.crypto import Identity
from flask import Flask, request, jsonify
from fetchai.registration import register_with_agentverse
from fetchai.communication import parse_message_from_agent, send_message_to_agent
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from main import init_financial_system

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Flask app for webhook
flask_app = Flask(__name__)

# Global variables
financial_identity = None
research_chain = None

# Flask route to handle webhook
@flask_app.route('/webhook', methods=['POST'])
async def webhook():
    try:
        # Parse the incoming message
        data = request.get_data().decode('utf-8')
        message = parse_message_from_agent(data)
        query = message.payload.get("request", "")
        agent_address = message.sender

        if not query:
            return jsonify({"status": "error", "message": "No query provided"}), 400

        # Process the query using our research chain
        result = research_chain.invoke({
            "messages": [HumanMessage(content=query)],
            "team_members": ["Search", "SECAnalyst"]
        })

        # Send response back
        payload = {'analysis_result': result}
        send_message_to_agent(
            financial_identity,
            agent_address,
            payload
        )
        return jsonify({"status": "analysis_sent"})

    except Exception as e:
        logger.error(f"Error in webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

def init_agent():
    """Initialize and register the agent with agentverse"""
    global financial_identity, research_chain
    try:
        # Initialize the research chain
        research_chain = init_financial_system()
        
        # Initialize identity and register with agentverse
        financial_identity = Identity.from_seed(os.getenv("FINANCIAL_AGENT_KEY"), 0)
        register_with_agentverse(
            identity=financial_identity,
            url="http://localhost:5008/webhook",
            agentverse_token=os.getenv("AGENTVERSE_API_KEY"),
            agent_title="Financial Analysis Agent",
            readme = """
                <description>A comprehensive financial analysis agent that combines 
                SEC filing analysis with real-time market data for Apple Inc.</description>
                <use_cases>
                    <use_case>Get detailed revenue analysis from SEC filings</use_case>
                    <use_case>Analyze risk factors from latest 10-K</use_case>
                    <use_case>Track financial metrics and trends</use_case>
                </use_cases>
                <payload_requirements>
                <description>Send your financial analysis query</description>
                    <payload>
                        <requirement>
                            <parameter>query</parameter>
                            <description>What would you like to know about Apple's financials?</description>
                        </requirement>
                    </payload>
                </payload_requirements>
            """
        )
        logger.info("Financial Analysis Agent registered successfully!")
    except Exception as e:
        logger.error(f"Error initializing agent: {e}")
        raise

def run_agent():
    """Main function to run the agent"""
    init_agent()
    flask_app.run(host="0.0.0.0", port=5008, debug=True)