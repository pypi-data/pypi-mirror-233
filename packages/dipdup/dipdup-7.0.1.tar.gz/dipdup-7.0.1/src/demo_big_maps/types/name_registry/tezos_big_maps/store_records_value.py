# generated by datamodel-codegen:
#   filename:  store_records_value.json

from __future__ import annotations

from typing import Dict
from typing import Optional

from pydantic import BaseModel
from pydantic import Extra


class StoreRecordsValue(BaseModel):
    class Config:
        extra = Extra.forbid

    address: Optional[str]
    data: Dict[str, str]
    expiry_key: Optional[str]
    internal_data: Dict[str, str]
    level: str
    owner: str
    tzip12_token_id: Optional[str]
