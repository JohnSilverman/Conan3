from pydantic import BaseModel, Json
from datetime import datetime


class SubjectBase(BaseModel):
    subject_name: str
    random_rate: float
    overlap_rate: float
    status: str
    task: str


class SubjectCreate(SubjectBase):
    pass


class SubjectModify(SubjectBase):
    id: int


class Subject(SubjectBase):
    id: int

    class Config:
        orm_mode = True


class LabelBase(BaseModel):
    value: str
    shortcut: str


class LabelCreate(LabelBase):
    subject_id: int


class LabelModify(LabelBase):
    id: int


class Label(LabelBase):
    subject_id: int
    id: int

    class Config:
        orm_mode = True


class AgentBase(BaseModel):
    privilege: str


class AgentCreate(AgentBase):
    pass


class Agent(AgentBase):
    id: int

    class Config:
        orm_mode = True


class SubjectAgentMappingBase(BaseModel):
    subject_id: int
    agent_id: str


class SubjectAgentMappingCreate(SubjectAgentMappingBase):
    pass


class SubjectAgentMapping(SubjectAgentMappingBase):
    id: int

    class Config:
        orm_mode = True


class TextClassificationBase(BaseModel):
    content: str
    subject_id: int
    label_id: int
    priority: float
    meta: Json
    status: str
    updated_by: str


class TextClassification(TextClassificationBase):
    id: int

    class Config:
        orm_mode = True


class ImageClassificationBase(BaseModel):
    content_url: str
    subject_id: int
    label_id: int
    priority: float
    meta: Json
    status: str
    updated_by: str


class ImageClassification(ImageClassificationBase):
    id: int

    class Config:
        orm_mode = True


class LabelLogBase(BaseModel):
    agent_id: str
    subject_id: int
    content_id: int
    label_id: int


class LabelLog(LabelLogBase):
    id: int
    created_at: datetime

