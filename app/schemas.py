from typing import Annotated, Optional
from pydantic import BaseModel, ConfigDict, Field, StringConstraints


class BookCreate(BaseModel):
    title: Annotated[str, StringConstraints(min_length=2, max_length=100)]
    author: Annotated[str, StringConstraints(min_length=2, max_length=60)]
    isbn: Annotated[str, StringConstraints(pattern=r"^\d{13}$")]
    year: int = Field(ge=1450, le=2026)

class BookUpdate(BaseModel):
    title: Optional[Annotated[str, StringConstraints(min_length=2, max_length=100)]] = None
    author: Optional[Annotated[str, StringConstraints(min_length=2, max_length=60)]] = None
    year: Optional[int] = Field(default=None, ge=1450, le=2026)


class BookRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    author: str
    isbn: str
    year: int
