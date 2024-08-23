from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from database import SessionLocal
import models

app = FastAPI()
db = SessionLocal()


class OurBaseModel(BaseModel):
    class Config:
        orm_mode = True


class Person(BaseModel):
    id: int
    first_name: str
    last_name: str
    isMale: bool


@app.get('/', response_model=list[Person], status_code=status.HTTP_200_OK)
def getAll_persons():
    getAllpersons = db.query(models.Person).all()
    return getAllpersons


@app.post('/addPerson', response_model=Person, status_code=status.HTTP_201_CREATED)
def add_Person(person: Person):
    newPerson = models.Person(
        id=person.id,
        first_name=person.first_name,
        last_name=person.last_name,
        isMale=person.isMale
    )
    find_person = db.query(models.Person).filter(models.Person.id == person.id).first()
    if find_person is not None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Person with this id is already exist..")
    else:
        db.add(newPerson)
        db.commit()
        return newPerson


@app.put('/updatePerson/{person_id}', response_model=Person, status_code=status.HTTP_202_ACCEPTED)
def updatePerson(person_id: int, person: Person):
    find_person = db.query(models.Person).filter(models.Person.id == person_id).first()
    if find_person is not None:
        find_person.id = person.id
        find_person.first_name = person.first_name
        find_person.last_name = person.last_name
        find_person.isMale = person.isMale

        db.commit()
        return find_person
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person with this id is not exist..")


@app.delete('/deletePerson/{person_id}', response_model=Person, status_code=200)
def deletePerson(person_id):
    find_person = db.query(models.Person).filter(models.Person.id == person_id).first()
    if find_person is not None:
        db.delete(find_person)
        db.commit()
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Person with this id is deleted successfully..")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Person with this id is either alreday deleted or not found..")


@app.get('/getById/{person_id}', response_model=Person, status_code=status.HTTP_200_OK)
def get_PersonById(person_id: int):
    getSingle_Person = db.query(models.Person).filter(models.Person.id == person_id).first()
    if getSingle_Person is not None:
        return getSingle_Person
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found..")

# @app.get("/", status_code=200)
# def getPersonInfo():
#     return {"message": "Server is running"}
#
# @app.get('/getpersonebyid/{person_id}', status_code=200)
# def getPerson_By_Id(person_id: int):
#     return {"message": f"Your person Id is {person_id}"}
#
# @app.post('/addpersoninfo', status_code=200)
# def addPersson_Info(person: Person):
#     return{
#         'id': person.id,
#         'first_name': person.first_name,
#         'last_name': person.last_name,
#         'isMale': person.isMale
#     }
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
