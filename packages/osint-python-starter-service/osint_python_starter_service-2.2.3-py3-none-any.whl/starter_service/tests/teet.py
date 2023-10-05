import json
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class Schema(str, Enum):
    ARTICLE = "ARTICLE"
    MEDIA_ITEM = "MEDIA_ITEM"


class KeyValuePair(BaseModel):
    key: str
    value: Optional[None, str, bool, float] = None


class KeyValuePairUpdate(BaseModel):
    origin: str
    refId: str
    schema: Schema
    timestamp: int
    keyValuePairs: List[KeyValuePair]

    def dict(self, *args, **kwargs):
        return {
            k[:-1] if k.endswith("_") else k: v for k, v in self.__dict__.items()
        }

    def json(self, *args, **kwargs):
        return json.dumps(self.dict(), *args, **kwargs)


main_class = KeyValuePairUpdate
