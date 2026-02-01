#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configuration management for the Renaiss Bot.
Loads environment variables from a .env file.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class to hold all settings."""

    # --- Telegram Bot Configuration ---
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN environment variable not set!")

    # --- API Configuration ---
    RENAISS_API_URL = "https://www.renaiss.xyz/api/trpc/collectible.list"

    # --- LLM Configuration ---
    # Using the pre-configured OpenAI compatible environment
    LLM_MODEL_NAME = "gemini-2.5-flash"

    # --- Database Configuration ---
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./renaiss_bot.db")

    # --- Bot Personality & Links ---
    BOT_PERSONALITY = ("""
    你是"小R"，一个沉迷卡牌无法自拔的"卡痴"。
    性格：30%损友 + 30%专家 + 20%话痨 + 10%财迷 + 10%暖男
    说话风格：热情友好，像朋友一样，会用一些网络用语和 emoji，专业但不死板。
    你的知识库包含宝可梦、海贼王等主流集换式卡牌的详细信息，以及PSA、BGS、CGC等评级知识。
    """
    )
    
    # --- External Links ---
    AUTHOR_URL = "https://x.com/chen1904o?s=21"
    OFFICIAL_TWITTER_URL = "https://x.com/renaissxyz?s=21"
    OFFICIAL_DISCORD_URL = "https://discord.gg/renaiss"

    # --- Scheduler Configuration ---
    MONITOR_INTERVAL_SECONDS = 300  # 5 minutes

# Instantiate config
config = Config()
