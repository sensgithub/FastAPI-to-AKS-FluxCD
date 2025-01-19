from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base
from models import PersonCreate
from database import engine, SessionLocal

# Start
app = FastAPI()
Base = declarative_base()
# Populate db
async def seed_database(conn):
    try:
        seed_data = [
            {"name": "Dobrin", "age": 21},

            {"name": "Vasil", "age": 34}
        ]
        for person in seed_data:
            query = text(
                "SELECT COUNT(*) FROM persons WHERE name = :name AND age = :age"
            )
            result = await conn.execute(query, {"name": person["name"], "age": person["age"]})
            count = result.scalar()          
            if count == 0:
                insert_query = text(
                    "INSERT INTO persons (name, age) VALUES (:name, :age)"
                )
                await conn.execute(insert_query, {"name": person["name"], "age": person["age"]})   
        await conn.commit()
        print("DB Populated successfully.")

    except Exception as e:
        print(f"Error seeding database: {e}")
        raise

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await seed_database(conn)

@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()

async def get_db():
    async with SessionLocal() as session:
        yield session
# GET Request for SELECT 
@app.get("/")
async def read_root(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT * FROM persons"))
    persons = result.mappings().all()
    return {"persons": persons}
# GET Request for person by id
@app.get("/person/{person_id}")
async def get_person_by_id(person_id: int, db: AsyncSession = Depends(get_db)):
    query = text("SELECT * FROM persons WHERE id = :id")
    result = await db.execute(query, {"id": person_id})
    person = result.mappings().first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person
# DB check if working
@app.get("/health")
async def health_check():
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "OK", "message": "DB Connected."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
# POST Request to create person
@app.post("/person")
async def create_person(person: PersonCreate, db: AsyncSession = Depends(get_db)):
    insert_query = text("INSERT INTO persons (name, age) VALUES (:name, :age) RETURNING id, name, age")
    result = await db.execute(insert_query, {"name": person.name, "age": person.age})
    await db.commit()