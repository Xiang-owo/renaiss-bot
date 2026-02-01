from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.card_info_service import CardInfoService
from config import config
from utils.logger import logger

class Scheduler:
    """Manages all scheduled background jobs for the bot."""

    def __init__(self):
        self.scheduler = AsyncIOScheduler(timezone="UTC")
        self.card_service = CardInfoService()

    def start(self):
        """Starts the scheduler and adds jobs."""
        logger.info("Starting background job scheduler.")
        self.scheduler.add_job(
            self.card_service.refresh_all_cards,
            'interval',
            seconds=config.MONITOR_INTERVAL_SECONDS,
            id='refresh_cards_job',
            replace_existing=True
        )
        self.scheduler.start()
        logger.info(f"Card refresh job scheduled to run every {config.MONITOR_INTERVAL_SECONDS} seconds.")

    def shutdown(self):
        """Shuts down the scheduler."""
        logger.info("Shutting down scheduler.")
        self.scheduler.shutdown()
