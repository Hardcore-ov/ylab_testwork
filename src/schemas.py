from pydantic import BaseModel


class SchemaBase(BaseModel):
    title: str
    description: str


class StatusMessage(BaseModel):
    status: bool
    message: str
