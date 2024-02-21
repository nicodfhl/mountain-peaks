from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column

from .create import Base


class DBPeak(Base):
    __tablename__ = "peaks"

    pid: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    height: Mapped[int] = mapped_column(Integer)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
