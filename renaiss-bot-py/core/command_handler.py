from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import config
from utils.logger import logger

class CommandHandler:
    """Handles all slash commands for the bot."""

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler for the /start command."""
        logger.info(f"User {update.effective_user.id} started the bot.")
        user_name = update.effective_user.first_name
        
        welcome_text = (
            f"嘿，{user_name}！我是小R，一个沉迷卡牌无法自拔的机器人！😜\n\n"
            f"你可以直接跟我聊天，比如：\n"
            f"- `喷火龙现在啥价？`\n"
            f"- `给我找找套利机会`\n\n"
            f"或者使用下面的命令来调戏我：\n"
            f"/help - 查看所有命令\n"
            f"/arbitrage - 主动寻找套利机会\n\n"
            f"准备好进入卡牌的奇妙世界了吗？🚀"
        )
        
        keyboard = [
            [InlineKeyboardButton("👨‍💻 作者推特", url=config.AUTHOR_URL)],
            [InlineKeyboardButton("🏢 官方推特", url=config.OFFICIAL_TWITTER_URL)],
            [InlineKeyboardButton("💬 官方Discord", url=config.OFFICIAL_DISCORD_URL)],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler for the /help command."""
        logger.info(f"User {update.effective_user.id} requested help.")
        help_text = (
            f"我是小R，你的专属卡牌伙伴！这是我的使用说明书：\n\n"
            f"**直接聊天** (推荐！✨)\n"
            f"就像和朋友聊天一样，直接给我发消息就行。我能理解自然语言，比如：\n"
            f"- `告诉我关于妙蛙种子的信息`\n"
            f"- `路飞和索隆的卡哪个更值钱？`\n"
            f"- `有没有能赚钱的机会？`\n\n"
            f"**命令列表**\n"
            f"/start - 重新认识一下我\n"
            f"/help - 就是你现在看到的这个啦\n"
            f"/arbitrage - 主动帮你寻找当前市场上的套利机会\n\n"
            f"**重要链接**\n"
            f"- [作者推特]({config.AUTHOR_URL})\n"
            f"- [官方推特]({config.OFFICIAL_TWITTER_URL})\n"
            f"- [官方Discord]({config.OFFICIAL_DISCORD_URL})\n\n"
            f"有任何问题，随时找我！我24小时在线（除非我在偷偷打牌...）🃏"
        )
        await update.message.reply_text(help_text, parse_mode='Markdown', disable_web_page_preview=True)

    async def arbitrage(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler for the /arbitrage command."""
        from services.arbitrage_service import ArbitrageService # Avoid circular import
        logger.info(f"User {update.effective_user.id} triggered /arbitrage command.")
        await update.message.reply_text("好的，财迷！我这就去帮你扒一扒市场上有没有漏可以捡... 🕵️‍♂️ 请稍等！")
        
        arbitrage_service = ArbitrageService()
        opportunities = await arbitrage_service.find_opportunities()
        
        if not opportunities:
            await update.message.reply_text("唉，今天市场风平浪静，没啥油水可捞。下次再试试吧！🤷‍♂️")
            return

        response = "🎉 发现宝贝了！快看这些潜在的套利机会：\n\n"
        for opp in opportunities[:5]: # Show top 5
            response += (
                f"**{opp['card_name']} ({opp['grade']})**\n"
                f"- 售价: *${opp['ask_price']}*\n"
                f"- FMV: *${opp['fmv_price']}*\n"
                f"- **潜在利润: ${opp['profit_usd']} ({opp['profit_percent']}%)** 🔥\n"
                f"- [直达链接]({opp['link']})\n\n"
            )
        
        response += "记住，市场价瞬息万变，下手要快哦！祝你发财！💰"
        await update.message.reply_text(response, parse_mode='Markdown', disable_web_page_preview=True)
