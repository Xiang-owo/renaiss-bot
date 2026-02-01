
from typing import List, Dict, Any, Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.database import Card, Listing, get_session
from adapters.renaiss_adapter import RenaissAdapter
from utils.logger import logger

class CardInfoService:
    """Service to manage card information from various sources."""

    def __init__(self):
        self.renaiss_adapter = RenaissAdapter()

    async def refresh_all_cards(self):
        """Refreshes all card data from the Renaiss API and updates the database."""
        logger.info("Starting to refresh all card data.")
        # In a real-world scenario, you might want to handle pagination
        listed_cards = await self.renaiss_adapter.get_all_listed_cards(limit=200)
        
        async for session in get_session():
            for card_data in listed_cards:
                # Check if card exists
                stmt = select(Card).where(Card.renaiss_id == card_data["renaiss_id"])
                result = await session.execute(stmt)
                card = result.scalars().first()

                if not card:
                    # Create new card
                    card = Card(
                        renaiss_id=card_data["renaiss_id"],
                        token_id=card_data["token_id"],
                        name=card_data["name"],
                        grade=card_data["grade"],
                        image_url=card_data["image_url"]
                    )
                    session.add(card)
                    await session.flush() # Flush to get the card ID

                # Update or create listing for Renaiss
                stmt_listing = select(Listing).where(Listing.card_id == card.id, Listing.source == "renaiss")
                result_listing = await session.execute(stmt_listing)
                listing = result_listing.scalars().first()

                if listing:
                    listing.ask_price = card_data["ask_price"]
                    listing.fmv_price = card_data["fmv_price"]
                    listing.offer_price = card_data["offer_price"]
                else:
                    listing = Listing(
                        card_id=card.id,
                        source="renaiss",
                        ask_price=card_data["ask_price"],
                        fmv_price=card_data["fmv_price"],
                        offer_price=card_data["offer_price"],
                        link=card_data["link"]
                    )
                    session.add(listing)
            
            await session.commit()
            logger.info(f"Database updated with {len(listed_cards)} cards.")

    async def get_card_info_by_name(self, card_name: str) -> Optional[Dict[str, Any]]:
        """Retrieves detailed information for a card by its name."""
        logger.info(f"Querying database for card: {card_name}")
        async for session in get_session():
            stmt = select(Card).where(Card.name.ilike(f"%{card_name}%"))
            result = await session.execute(stmt)
            card = result.scalars().first()

            if not card:
                logger.warning(f"Card ‘{card_name}’ not found in database.")
                return None

            # Fetch its listing
            stmt_listing = select(Listing).where(Listing.card_id == card.id, Listing.source == "renaiss")
            result_listing = await session.execute(stmt_listing)
            listing = result_listing.scalars().first()

            if not listing:
                return None # Should not happen if data is consistent

            return {
                "name": card.name,
                "grade": card.grade,
                "image_url": card.image_url,
                "ask_price": listing.ask_price,
                "fmv_price": listing.fmv_price,
                "offer_price": listing.offer_price,
                "link": listing.link
            }
