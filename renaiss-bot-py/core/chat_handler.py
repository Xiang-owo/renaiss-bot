
from telegram import Update
from telegram.ext import ContextTypes
from adapters.llm_adapter import LLMAdapter
from services.card_info_service import CardInfoService
from services.arbitrage_service import ArbitrageService
from config import config
from utils.logger import logger

class ChatHandler:
    """Handles all non-command text messages for natural language interaction."""

    def __init__(self):
        self.llm = LLMAdapter()
        self.card_service = CardInfoService()
        self.arbitrage_service = ArbitrageService()

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Main entry point for handling user messages."""
        user_message = update.message.text
        logger.info(f"Received message from user {update.effective_user.id}: {user_message}")

        # 1. Parse Intent
        intent_data = await self.llm.parse_intent(user_message)
        intent = intent_data.get("intent", "general_chat")
        entities = intent_data.get("entities", [])

        # 2. Execute Action based on Intent
        action_data = await self._execute_action(intent, entities)

        # 3. Generate Response
        response_text = await self._generate_response(user_message, intent, action_data)
        
        await update.message.reply_text(response_text, parse_mode='Markdown')

    async def _execute_action(self, intent: str, entities: list) -> dict:
        """Executes the corresponding service based on the parsed intent."""
        if intent == "query_card" and entities:
            card_info = await self.card_service.get_card_info_by_name(entities[0])
            return {"card_info": card_info, "card_name": entities[0]}
        
        if intent == "find_arbitrage":
            opportunities = await self.arbitrage_service.find_opportunities()
            return {"opportunities": opportunities[:3]} # Return top 3

        # For compare_cards and general_chat, we might not need to fetch data beforehand
        return {}

    async def _generate_response(self, user_message: str, intent: str, data: dict) -> str:
        """Generates a fun and informative response using the LLM."""
        system_prompt = config.BOT_PERSONALITY
        
        # Craft a detailed prompt for the LLM
        user_prompt = f"""
        You are responding to a user in a Telegram chat. Here is the context:

        User's original message: "{user_message}"
        Your analysis of their intent: {intent}
        Data you fetched from the database: {data}

        Based on this, craft a fun, engaging, and helpful response in character as '小R'.
        - If you have card data, format it nicely using Markdown.
        - If you found arbitrage opportunities, present them clearly.
        - If you don't have specific data, just have a fun, on-brand conversation.
        - Always be helpful and embody your personality traits.
        - Keep it concise and use emojis! 😜
        """
        
        return await self.llm.generate_response(system_prompt, user_prompt)
