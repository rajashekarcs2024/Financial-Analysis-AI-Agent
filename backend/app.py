from flask import Flask, request, jsonify
from flask_cors import CORS
from fetchai.crypto import Identity
from fetchai.registration import register_with_agentverse
from fetchai.communication import parse_message_from_agent, send_message_to_agent
from fetchai import fetch
import logging
import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {'origins': 'http://localhost:5174'}})

class PrimaryAgent:
    def __init__(self):
        self.identity = None
        self.latest_response = None
    
    def initialize(self):
        try:
            self.identity = Identity.from_seed(os.getenv("PRIMARY_AGENT_KEY"), 0)
            
            register_with_agentverse(
                identity=self.identity,
                url="http://localhost:5001/webhook",
                agentverse_token=os.getenv("AGENTVERSE_API_KEY"),
                agent_title="Financial Query Router",
                readme="<description>Routes queries to Financial Analysis Agent</description>"
            )
            logger.info("Primary agent initialized successfully!")
                
        except Exception as e:
            logger.error(f"Initialization error: {e}")
            raise

    def find_financial_agent(self):
        """Find our registered financial analysis agent"""
        try:
            available_ais = fetch.ai("Financial Analysis Agent")
            agents = available_ais.get('ais', [])
            
            if agents:
                logger.info(f"Found financial agent at address: {agents[0]['address']}")  # Add this log
                return agents[0]
            return None
            
        except Exception as e:
            logger.error(f"Error finding financial agent: {e}")
            return None

primary_agent = PrimaryAgent()

@app.route('/api/send-request', methods=['POST'])
def send_request():
    try:
        data = request.json
        user_input = data.get('input')
        
        if not user_input:
            return jsonify({"error": "No input provided"}), 400
        
        # Find financial analysis agent
        agent = primary_agent.find_financial_agent()
        if not agent:
            return jsonify({"error": "Financial analysis agent not available"}), 404
        
        logger.info(f"Sending request to agent at: {agent['address']}")  # Add this log
        # Send request to financial agent
        send_message_to_agent(
            primary_agent.identity,
            agent['address'],
            {
                "request": user_input
            }
        )
        
        return jsonify({"status": "request_sent"})
        
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/get-response', methods=['GET'])
def get_response():
    try:
        if primary_agent.latest_response:
            response = primary_agent.latest_response
            primary_agent.latest_response = None
            return jsonify(response)
        return jsonify({"status": "waiting"})
    except Exception as e:
        logger.error(f"Error getting response: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_data().decode("utf-8")
        message = parse_message_from_agent(data)
        
        # Store response
        primary_agent.latest_response = message.payload
        
        return jsonify({"status": "success"})
        
    except Exception as e:
        logger.error(f"Error in webhook: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    load_dotenv()
    primary_agent.initialize()
    app.run(host="0.0.0.0", port=5001)