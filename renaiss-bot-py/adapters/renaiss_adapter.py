
import aiohttp
import json
from typing import List, Dict, Any
from config import config
from utils.logger import logger

class RenaissAdapter:
    """Adapter for the Renaiss platform API."""

    def __init__(self):
        self.api_url = config.RENAISS_API_URL
        self.base_url = "https://www.renaiss.xyz"

    async def get_all_listed_cards(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Fetches all listed cards from the Renaiss API."""
        logger.info(f"Fetching {limit} listed cards from Renaiss, offset {offset}")
        params = {
            "0": {
                "json": {
                    "limit": limit,
                    "offset": offset,
                    "listedOnly": True,
                    "sortBy": "listDate",
                    "sortOrder": "desc"
                }
            }
        }
        try:
            async with aiohttp.ClientSession() as session:
                # The input parameter needs to be a JSON string
                input_str = json.dumps(params)
                async with session.get(f"{self.api_url}?batch=1&input={input_str}") as response:
                    response.raise_for_status() # Raise an exception for bad status codes
                    data = await response.json()
                    return self._normalize_cards(data)
        except aiohttp.ClientError as e:
            logger.error(f"Error fetching data from Renaiss API: {e}")
            return []
        except Exception as e:
            logger.error(f"An unexpected error occurred in RenaissAdapter: {e}")
            return []

    def _normalize_cards(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Normalizes the raw card data from the API into a structured format."""
        normalized_cards = []
        if not raw_data or not isinstance(raw_data, list) or not raw_data[0].get("result"):
            logger.warning("Renaiss API returned empty or invalid data format.")
            return []

        collection = raw_data[0]["result"]["data"]["json"]["collection"]
        
        for item in collection:
            try:
                ask_price = float(item.get("askPriceInUSDT", 0)) / 1e18 if item.get("askPriceInUSDT") else None
                fmv_price = float(item.get("fmvPriceInUSD", 0)) / 100 if item.get("fmvPriceInUSD") else None
                offer_price = float(item.get("offerPriceInUSDT", 0)) / 1e18 if item.get("offerPriceInUSDT") else None

                normalized_cards.append({
                    "renaiss_id": item["id"],
                    "token_id": item["tokenId"],
                    "name": item["name"],
                    "ask_price": round(ask_price, 2) if ask_price is not None else None,
                    "fmv_price": round(fmv_price, 2) if fmv_price is not None else None,
                    "offer_price": round(offer_price, 2) if offer_price is not None else None,
                    "grade": item.get("grade"),
                    "image_url": item.get("frontImageUrl"),
                    "link": f"{self.base_url}/card/{item['tokenId']}"
                })
            except (TypeError, ValueError, KeyError) as e:
                logger.error(f"Error normalizing card data for item {item.get('id')}: {e}")
                continue
        
        logger.info(f"Successfully normalized {len(normalized_cards)} cards.")
        return normalized_cards
