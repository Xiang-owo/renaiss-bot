#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main entry point for the Renaiss Telegram Bot.
"""

import asyncio
from telegram.ext import Application, CommandHandler as TGCommandHandler, MessageHandler, filters

from config import config
from models.database import init_db
from core.command_handler import CommandHandler
from core.chat_handler import ChatHandler
from jobs.scheduler import Scheduler
from utils.logger import logger

def main():
    """Main function to run the bot."""
    logger.info("Starting Renaiss Bot...")

    # --- Initialize Database ---
    asyncio.run(init_db())
    logger.info("Database initialized.")

    # --- Initialize Scheduler ---
    scheduler = Scheduler()
    scheduler.start()

    # --- Initialize Telegram Bot Application ---
    application = Application.builder().token(config.TELEGRAM_TOKEN).build()

    # --- Register Handlers ---
    command_handler = CommandHandler()
    chat_handler = ChatHandler()

    application.add_handler(TGCommandHandler("start", command_handler.start))
    application.add_handler(TGCommandHandler("help", command_handler.help))
    application.add_handler(TGCommandHandler("arbitrage", command_handler.arbitrage))

    # Add a handler for all non-command text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_handler.handle_message))

    logger.info("Telegram handlers registered. Starting polling...")
    
    # --- Start the Bot ---
    try:
        application.run_polling()
    except Exception as e:
        logger.error(f"Bot polling failed: {e}")
    finally:
        scheduler.shutdown()
        logger.info("Bot has been shut down.")

if __name__ == "__main__":
    main()
