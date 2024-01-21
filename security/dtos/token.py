from typing import Optional

from pydantic import BaseModel


class TokenPayload(BaseModel):
    sub: Optional[int] = None
