from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

class PlayerCreate(BaseModel):
    name: Annotated[str, StringConstraints(min_length=2, max_length=50)]
    position: Annotated[str, StringConstraints(min_length=2, max_length=20)]
    shirt_number: int = Field(ge=1, le=99)
    email: Annotated[str, StringConstraints(pattern=r"\d{min_length=1, max_length=100}&.com")]

class PlayerUpdate(BaseModel):
    position: Optional[Annotated[str, StringConstraints(min_length=2, max_length=50)]] = None
    shirt_number: Optional[int] = Field(default=None, ge=1, le=99)

class PlayerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    position: str
    shirt_number: int
    email: str
