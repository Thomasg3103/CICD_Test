from sqlalchemy import Interger, String
from sqlalchemy import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class PlayerDB(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    position: Mapped[str] = mapped_column(String(20), nullable=False)
    shirt_number: Mapped[int] = mapped_column(Interger, nullable=False)
    email: Mapped[str] = mapped_column(String(99), unique = True, nullable=False)