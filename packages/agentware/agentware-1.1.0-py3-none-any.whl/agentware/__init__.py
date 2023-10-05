import os
from dotenv import load_dotenv
from agentware.agent_logger import Logger

logger = Logger()
logger.set_level(Logger.WARNING)
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")