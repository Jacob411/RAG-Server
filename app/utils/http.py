import requests
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

async def make_request(base_url: str, method: str, endpoint: str, **kwargs) -> Dict[Any, Any]:
    """
    Helper function to make HTTP requests to the RAG server
    """
    url = f"{base_url}{endpoint}"
    logger.info(f"Making {method} request to {url}")
    
    try:
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        try:
            return response.json()
        except:
            return response.text
    except Exception as e:
        logger.error(f"Request failed: {str(e)}")
        return {
            "success": False,
            "message": f"Request failed: {str(e)}",
            "status_code": 500
        }