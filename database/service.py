from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import func

from datetime import datetime
from . import models, schemas

import random


def get_subjects(db: Session):
    return db.query(models.Subject).all()


def get_subject(db: Session, subject_id: int):
    return db.query(models.Subject).filter(models.Subject.id == subject_id).first()


def create_subject(db: Session, subject: schemas.SubjectCreate):
    db_subject = models.Subject(subject_name=subject.subject_name,
                                random_rate=subject.random_rate, overlap_rate=subject.overlap_rate,
                                status=subject.status, task=subject.task)

    db_subject.created_at = datetime.now()

    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)

    return db_subject


def modify_subject(db: Session, subject: schemas.SubjectModify):
    db_subject = db.query(models.Subject).filter(models.Subject.id == subject.id).first()

    db_subject.subject_name = subject.subject_name
    db_subject.random_rate = subject.random_rate
    db_subject.overlap_rate = subject.overlap_rate
    db_subject.status = subject.status
    db_subject.task = subject.task

    db.commit()
    return db_subject


def change_subject_status(db: Session, subject_id: int, status: str):
    db_subject = db.query(models.Subject).filter(models.Subject.id == subject_id).first()

    db_subject.status = status
    db.commit()

    return db_subject


def get_labels(db: Session, subject_id):
    db_labels = db.query(models.Label).filter(models.Label.subject_id == subject_id).all()
    return db_labels


def create_label(db: Session, label: schemas.LabelCreate):
    shortcut = label.shortcut.lower()
    if shortcut in ['h', 'b', 'q', '?'] or not (ord('a') <= ord(shortcut) <= ord('z')):
        raise HTTPException(status_code=400, detail="reserved shortcut")

    db_label = models.Label(subject_id=label.subject_id, value=label.value, shortcut=label.shortcut)
    db.add(db_label)
    db.commit()
    db.refresh(db_label)
    return db_label


def update_label(db: Session, label: schemas.LabelModify):
    db_label = db.query(models.Label).filter(models.Label.id == label.id).first()
    db_label.value = label.value
    db_label.shortcut = label.shortcut
    db.commit()
    return db_label


def delete_label(db: Session, label_id: int):
    db_label = db.query(models.Label).filter(models.Label.id == label_id).first()
    db.delete(db_label)
    db.commit()
    return db_label


def create_subject_agent_mapping(db: Session, mapping: schemas.SubjectAgentMappingCreate):
    db_mapping = models.SubjectAgentMapping(subject_id=mapping.subject_id, agent_id=mapping.agent_id)
    db.add(db_mapping)
    db.commit()
    db.refresh(db_mapping)
    return db_mapping


def delete_subject_agent_mapping(db: Session, mapping: schemas.SubjectAgentMappingCreate):
    db_mapping = db.query(models.SubjectAgentMapping).filter(models.SubjectAgentMapping.subject_id == mapping.subject_id)\
        .filter(models.SubjectAgentMapping.agent_id == mapping.agent_id).first()
    db.delete(db_mapping)
    db.commit()
    return db_mapping


def get_mappings_by_subject(db: Session, subject_id: int):
    db_mappings = db.query(models.SubjectAgentMapping).filter(models.SubjectAgentMapping.subject_id == subject_id).all()
    return db_mappings


def get_mappings_by_agent(db: Session, agent_id: str):
    db_mappings = db.query(models.SubjectAgentMapping).filter(models.SubjectAgentMapping.agent_id == agent_id).all()
    return db_mappings


# 분배
def get_content(db: Session, subject_id: int, agent_id: str):
    db_subject = db.query(models.Subject).filter(models.Subject.id == subject_id).first()

    overlap_rate = db_subject.overlap_rate
    random_rate = db_subject.random_rate

    content_model = models.ImageClassification if db_subject.task == 'ImageClassification' else models.TextClassification

    if random.random() <= overlap_rate: # 중복분배 수행
        print("trying cross checking")
        db_content = db.query(content_model).filter(content_model.subject_id == subject_id)\
            .filter(content_model.status == 'labled').filter(content_model.updated_by != agent_id)\
            .order_by(func.random()).first()

        if db_content:
            print("return")
            return db_content

    if random.random() <= random_rate: # 랜덤샘플링 수행
        print("trying random")
        db_content = db.query(content_model).filter(content_model.subject_id == subject_id) \
            .filter(content_model.status == 'ready').order_by(func.random()).first()

        if db_content:
            print("return")
            return db_content

    # 선별스코어에 의한 분배
    print("trying priority")
    db_content = db.query(content_model).filter(content_model.subject_id == subject_id)\
        .order_by(content_model.priority.desc()).first()
    return db_content


import time
import random
def make_test_data(db: Session):
    tstr = str(int(time.time()))

    subject = models.Subject(subject_name="subject"+tstr, created_at=datetime.now(), random_rate=0.2,
                             overlap_rate=0.2, task="TextClassification")
    db.add(subject)
    db.commit()
    db.refresh(subject)

    for i in range(1000):
        tc = models.TextClassification(content="content", subject_id=subject.id, priority=random.random())
        db.add(tc)

    db.commit()

    return subject