from pydantic import BaseModel


class LocalHandle(BaseModel):
    name: str
