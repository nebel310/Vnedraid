from datetime import datetime, timezone
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from database import Model




class CarOrm(Model):
    __tablename__ = 'cars'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    brand: Mapped[str]
    model: Mapped[str]
    year: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class CarImageOrm(Model):
    __tablename__ = 'car_images'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey('cars.id'))
    image_url: Mapped[str]