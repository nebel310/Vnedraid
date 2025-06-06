import os
from fastapi import APIRouter, UploadFile, File, Form, Depends
from schemas.car import SCarBase, SDamageReport
from repositories.car import CarRepository
from typing import Annotated, List




car_router = APIRouter(
    prefix="/cars",
    tags=['Автомобили']
)


@car_router.post("/assess", response_model=SDamageReport)
async def assess_car(
    brand: Annotated[str, Form()],
    model: Annotated[str, Form()],
    year: Annotated[int, Form()],
    files: Annotated[List[UploadFile], File(description="Фотографии автомобиля")]
):
    # Сохраняем данные об автомобиле
    car_data = SCarBase(brand=brand, model=model, year=year)
    car_id = await CarRepository.create_car(car_data)
        
    # Сохраняем изображения
    await CarRepository.save_car_images(car_id, files)
    
    # Получаем отчет о повреждениях
    report = await CarRepository.get_damage_report()
    
    return report