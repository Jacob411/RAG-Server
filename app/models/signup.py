from pydantic import BaseModel
from typing import Optional

class SignupRequest(BaseModel):
   email: str
   r2r_user_id: str  # Since we're using R2R auth, we'll store their user ID
   subscription_tier: Optional[str] = "free"