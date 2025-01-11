from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Pydantic модель для направления путешествия
class Destination(BaseModel):
    id: int
    name: str
    country: str
    description: Optional[str] = None
    image_url: str

# Хранилище для направлений (в реальном приложении это будет база данных)
destinations_db = []

# Ручка для получения всех направлений
@app.get("/destinations/", response_model=List[Destination])
def get_destinations():
    return destinations_db

# Ручка для добавления нового направления
@app.post("/destinations/", response_model=Destination)
def create_destination(destination: Destination):
    # Проверка на существующее направление с тем же id
    for existing_destination in destinations_db:
        if existing_destination.id == destination.id:
            raise HTTPException(status_code=400, detail="Destination with this ID already exists.")
    
    destinations_db.append(destination)
    return destination

# Ручка для получения направления по ID
@app.get("/destinations/{destination_id}", response_model=Destination)
def get_destination(destination_id: int):
    for destination in destinations_db:
        if destination.id == destination_id:
            return destination
    raise HTTPException(status_code=404, detail="Destination not found.")

# Ручка для обновления направления
@app.put("/destinations/{destination_id}", response_model=Destination)
def update_destination(destination_id: int, updated_destination: Destination):
    for index, destination in enumerate(destinations_db):
        if destination.id == destination_id:
            destinations_db[index] = updated_destination
            return updated_destination
    raise HTTPException(status_code=404, detail="Destination not found.")

# Ручка для удаления направления
@app.delete("/destinations/{destination_id}", response_model=Destination)
def delete_destination(destination_id: int):
    for index, destination in enumerate(destinations_db):
        if destination.id == destination_id:
            return destinations_db.pop(index)
    raise HTTPException(status_code=404, detail="Destination not found.")

# Запуск приложения
# Для запуска используйте команду: uvicorn main:app --reload
