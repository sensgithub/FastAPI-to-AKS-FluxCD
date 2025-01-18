from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

class Person(BaseModel):
    name: str
    age: int 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/person")
async def create_person(person: Person, db: db_dependency):
    db_person = models.Person(name=person.name, age=person.age)
    db.add(db_person)
    db.commit()
    db.refresh(db_person)

@app.get("/person/", response_model=List[Person])
async def get_all_persons(db: db_dependency):
    persons = db.query(models.Person).all()
    return persons

@app.get("/person/{person_id}")
async def get_person_by_id(person_id, db: db_dependency):
    res = db.query(models.Person).filter(models.Person.id == person_id).first()
    if not res:
        raise HTTPException(status_code=404, detail="Person not found")
    return res