
import json
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from typing import List, Optional, Dict, Union
from uuid import UUID

from pydantic import BaseModel

class MetadataItem(BaseModel):
    type: str
    value: Union[str, float]
    id: Optional[str] = None
    start: Optional[int] = None
    end: Optional[int] = None
    label: Optional[str] = None
    lemma: Optional[str] = None
    wkt: Optional[str] = None
    options: Optional[Dict[str, Union[str, float, bool]]] = None


class Metadata(BaseModel):
    articleId: str
    origin: str
    data: List[MetadataItem]

    def dict(self, *args, **kwargs):
            return {
                k[:-1] if k.endswith("_") else k: v for k, v in self.__dict__.items()
            }

    def json(self, *args, **kwargs):
            return json.dumps(self.dict(), *args, **kwargs)
    

main_class = Metadata
