from __future__ import annotations

from typing import Dict

from pydantic import BaseModel, Field


class UserDonates(BaseModel):

    total_amount: int = Field(alias="totalAmount")
    total_count: int = Field(alias="totalCount")

    def __repr__(self) -> Dict[str, int]:
        return self.model_dump()

    def __str__(self) -> str:
        return f"{self.model_dump()}"

    def __lt__(self, other: UserDonates) -> bool:
        return self.total_amount < other.total_amount