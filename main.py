from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import service, models, schemas
from database.connection import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/subjects", response_model=list[schemas.Subject])
def get_subjects(db: Session = Depends(get_db)):
    db_subjects = service.get_subjects(db)
    return db_subjects


@app.post("/subjects", response_model=schemas.Subject)
def create_subject(subject: schemas.SubjectCreate, db: Session = Depends(get_db)):
    db_subject = service.create_subject(db, subject)
    return db_subject


@app.put("/subjects", response_model=schemas.Subject)
def modify_subject(subject: schemas.SubjectModify, db: Session = Depends(get_db)):
    db_subject = service.modify_subject(db, subject)
    return db_subject


@app.put("/subjects/status", response_model=schemas.Subject)
def change_subject_status(subject_id: int, status: str, db: Session = Depends(get_db)):
    db_subject = service.change_subject_status(db, subject_id, status)
    return db_subject


@app.get("/subjects/{subject_id}", response_model=schemas.Subject)
def get_subject_by_id(subject_id: int, db: Session = Depends(get_db)):
    subject = service.get_subject(db, subject_id)
    if subject is None:
        raise HTTPException(status_code=404, detail="subject not found")
    return subject


@app.get("/labels/{subject_id}", response_model=list[schemas.Label])
def get_labels(subject_id: int, db: Session = Depends(get_db)):
    db_labels = service.get_labels(db, subject_id)
    return db_labels


@app.post("/labels", response_model=schemas.Label)
def create_label(label: schemas.LabelCreate, db: Session = Depends(get_db)):
    db_label = service.create_label(db, label)
    return db_label


@app.put("/labels", response_model=schemas.Label)
def update_label(label: schemas.LabelModify, db: Session = Depends(get_db)):
    db_label = service.update_label(db, label)
    return db_label


@app.delete("/labels", response_model=schemas.Label)
def delete_label(label_id: int, db: Session = Depends(get_db)):
    db_label = service.delete_label(db, label_id)
    return db_label


@app.post("/subjects_agents", response_model=schemas.SubjectAgentMapping)
def create_subject_agent_mapping(mapping: schemas.SubjectAgentMappingCreate, db: Session = Depends(get_db)):
    db_mapping = service.create_subject_agent_mapping(db, mapping)
    return db_mapping


@app.delete("/subjects_agents", response_model=schemas.SubjectAgentMapping)
def delete_subject_agent_mapping(mapping: schemas.SubjectAgentMappingCreate, db: Session = Depends(get_db)):
    db_mapping = service.delete_subject_agent_mapping(db, mapping)
    return db_mapping


@app.get("/subjects_agents/by_subject_id/{subject_id}")
def get_mappings_by_subject_id(subject_id: int, db: Session = Depends(get_db)):
    db_mappings = service.get_mappings_by_subject(db, subject_id)
    return db_mappings


@app.get("/subjects_agents/by_agent_id/{agent_id}")
def get_mappings_by_agent_id(agent_id: str, db: Session = Depends(get_db)):
    db_mappings = service.get_mappings_by_agent(db, agent_id)
    return db_mappings


@app.get("/content")
def get_content(subject_id: int, agent_id: str, db: Session = Depends(get_db)):
    db_content = service.get_content(db, subject_id, agent_id)
    return db_content


@app.post("/test_data")
def make_test_data(db: Session = Depends(get_db)):
    retval = service.make_test_data(db)
    return retval

