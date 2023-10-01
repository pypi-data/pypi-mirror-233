# generated by datamodel-codegen:
#   filename:  Burn.json

from __future__ import annotations

from pydantic import BaseModel
from pydantic import Extra


class Burn(BaseModel):
    class Config:
        extra = Extra.forbid

    owner: str
    tickLower: int
    tickUpper: int
    amount: int
    amount0: int
    amount1: int
