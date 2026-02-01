
from typing import List, Dict, Any
from sqlalchemy.future import select
from models.database import Card, Listing, ArbitrageLog, get_session
from utils.logger import logger

class ArbitrageService:
    """Service to find and log arbitrage opportunities."""

    async def find_opportunities(self, min_profit_percent: float = 5.0) -> List[Dict[str, Any]]:
        """Finds arbitrage opportunities from the database."""
        logger.info(f"Finding arbitrage opportunities with min profit >= {min_profit_percent}%")
        opportunities = []
        async for session in get_session():
            # Query for cards and their Renaiss listings
            stmt = select(Card, Listing).join(Listing).where(Listing.source == "renaiss")
            result = await session.execute(stmt)
            
            for card, listing in result.all():
                if not listing.ask_price or not listing.fmv_price or listing.ask_price == 0:
                    continue

                # FMV Arbitrage
                profit_percent = ((listing.fmv_price - listing.ask_price) / listing.ask_price) * 100
                if profit_percent >= min_profit_percent:
                    opp = {
                        "card_name": card.name,
                        "grade": card.grade,
                        "image_url": card.image_url,
                        "ask_price": listing.ask_price,
                        "fmv_price": listing.fmv_price,
                        "profit_percent": round(profit_percent, 2),
                        "profit_usd": round(listing.fmv_price - listing.ask_price, 2),
                        "link": listing.link,
                        "type": "FMV Arbitrage"
                    }
                    opportunities.append(opp)
                    # Log the opportunity
                    log_entry = ArbitrageLog(
                        card_id=card.id,
                        profit_percent=opp["profit_percent"],
                        profit_usd=opp["profit_usd"],
                        type=opp["type"],
                        details=f"Ask: ${listing.ask_price}, FMV: ${listing.fmv_price}"
                    )
                    session.add(log_entry)

        # Sort by highest profit percentage
        opportunities.sort(key=lambda x: x["profit_percent"], reverse=True)
        
        if opportunities:
            await session.commit()
            logger.info(f"Found {len(opportunities)} arbitrage opportunities.")
        
        return opportunities
