from __future__ import annotations

import os
from pydantic import BaseModel

class DataSchema(BaseModel):
    phone:   str
    address: str