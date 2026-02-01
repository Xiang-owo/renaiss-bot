'''
LLM Adapter to interact with the AI model for chat functionalities.
'''

import openai
import json
from config import config, Config
from utils.logger import logger

class LLMAdapter:
    '''Adapter for the Large Language Model.'''

    def __init__(self, cfg: Config = config):
        '''Initializes the LLM adapter.'''
        self.client = openai.AsyncOpenAI()
        self.model = cfg.LLM_MODEL_NAME
        self.personality = cfg.BOT_PERSONALITY

    async def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        '''
        Generates a response from the LLM based on a system and user prompt.

        Args:
            system_prompt: The system prompt defining the bot's personality and context.
            user_prompt: The user's message.

        Returns:
            The generated response string.
        '''
        logger.info(f"Generating LLM response for prompt: {user_prompt}")
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=500,
            )
            text_response = response.choices[0].message.content.strip()
            logger.info(f"LLM generated response: {text_response}")
            return text_response
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            return "抱歉，我的大脑好像断线了... 🧠💥 能稍等一下再问我吗？"

    async def parse_intent(self, user_message: str) -> dict:
        '''
        Uses the LLM to parse the user's intent and extract entities.

        Args:
            user_message: The raw text message from the user.

        Returns:
            A dictionary with "intent" and "entities".
        '''
        logger.info(f"Parsing intent for message: {user_message}")
        prompt = f'''
        Analyze the user message below and identify the primary intent and any relevant entities (like card names or numbers).

        User Message: "{user_message}"

        Possible Intents:
        - "query_card": User is asking for information about one or more specific cards.
        - "compare_cards": User is asking to compare two or more cards.
        - "find_arbitrage": User is asking about arbitrage opportunities.
        - "ask_help": User is asking for help or instructions.
        - "general_chat": A general conversation, question, or greeting.

        Respond ONLY with a valid JSON object in the following format:
        {{"intent": "...", "entities": ["...", "..."]}}

        Example for "查询喷火龙":
        {{"intent": "query_card", "entities": ["喷火龙"]}}

        Example for "路飞和索隆哪个贵":
        {{"intent": "compare_cards", "entities": ["路飞", "索隆"]}}
        '''
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at classifying user intent and extracting entities. Respond only in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            intent_data = json.loads(response.choices[0].message.content)
            logger.info(f"Parsed intent: {intent_data}")
            return intent_data
        except Exception as e:
            logger.error(f"Error parsing intent: {e}")
            return {"intent": "general_chat", "entities": [user_message]} # Default to general chat on error
