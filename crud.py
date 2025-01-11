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
destinations_db: List[Destination] = []

# Ручка для получения всех направлений
@app.get("/destinations/", response_model=List[Destination])
def get_destinations():
    return destinations_db

# Ручка для получения направления по ID
@app.get("/destinations/{destination_id}", response_model=Destination)
def get_destination(destination_id: int):
    destination = next((d for d in destinations_db if d.id == destination_id), None)
    if destination is None:
        raise HTTPException(status_code=404, detail="Destination not found.")
    return destination

# Ручка для создания нового направления
@app.post("/destinations/", response_model=Destination)
def create_destination(destination: Destination):
    if any(d.id == destination.id for d in destinations_db):
        raise HTTPException(status_code=400, detail="Destination with this ID already exists.")
    
    destinations_db.append(destination)
    return destination

# Ручка для обновления направления
@app.put("/destinations/{destination_id}", response_model=Destination)
def update_destination(destination_id: int, updated_destination: Destination):
    destination_index = next((index for index, d in enumerate(destinations_db) if d.id == destination_id), None)
    if destination_index is None:
        raise HTTPException(status_code=404, detail="Destination not found.")
    
    destinations_db[destination_index] = updated_destination
    return updated_destination

# Ручка для удаления направления
@app.delete("/destinations/{destination_id}", response_model=Destination)
def delete_destination(destination_id: int):
    destination_index = next((index for index, d in enumerate(destinations_db) if d.id == destination_id), None)
    if destination_index is None:
        raise HTTPException(status_code=404, detail="Destination not found.")
    
    return destinations_db.pop(destination_index)

# Запуск приложения
# Для запуска используйте команду: uvicorn main:app --reload
