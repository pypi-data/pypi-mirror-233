# generated by datamodel-codegen:
#   filename:  Collect.json

from __future__ import annotations

from pydantic import BaseModel
from pydantic import Extra


class Collect(BaseModel):
    class Config:
        extra = Extra.forbid

    tokenId: int
    recipient: str
    amount0: int
    amount1: int
