import os
from uuid import uuid4
from database import new_session
from models.car import CarOrm, CarImageOrm
from schemas.car import SCarBase
from sqlalchemy import select
from fastapi import UploadFile




class CarRepository:
    counter = 0
    UPLOAD_DIR = "uploads"

    @classmethod
    def _ensure_upload_dir_exists(cls):
        os.makedirs(cls.UPLOAD_DIR, exist_ok=True)


    @classmethod
    async def save_car_images(cls, car_id: int, files: list[UploadFile]) -> list[str]:
        cls._ensure_upload_dir_exists()
        saved_paths = []
        
        for file in files:
            # Генерируем уникальное имя файла
            file_ext = os.path.splitext(file.filename)[1]
            unique_filename = f"{uuid4()}{file_ext}"
            file_path = os.path.join(cls.UPLOAD_DIR, unique_filename)
            
            # Сохраняем файл
            with open(file_path, "wb") as buffer:
                buffer.write(await file.read())
            
            saved_paths.append(unique_filename)
            
            # Сохраняем запись в БД
            async with new_session() as session:
                session.add(CarImageOrm(
                    car_id=car_id,
                    image_url=unique_filename  # Сохраняем только имя файла
                ))
                await session.commit()
        
        return saved_paths


    @classmethod
    async def create_car(cls, car_data: SCarBase) -> int:
        async with new_session() as session:
            car = CarOrm(
                brand=car_data.brand,
                model=car_data.model,
                year=car_data.year
            )
            session.add(car)
            await session.flush()
            await session.commit()
            return car.id


    @classmethod
    async def get_damage_report(cls) -> dict:
        cls.counter = (cls.counter + 1) % 3
        
        reports = [
            {
                "damage_description": "Незначительные царапины на бампере",
                "current_damage_coef": 0.1,
                "historical_damage_coef": 0.3
            },
            {
                "damage_description": "Вмятина на двери, царапины",
                "current_damage_coef": 0.4,
                "historical_damage_coef": 0.7
            },
            {
                "damage_description": "Крупные повреждения кузова",
                "current_damage_coef": 0.8,
                "historical_damage_coef": 1.0
            }
        ]
        
        return reports[cls.counter]