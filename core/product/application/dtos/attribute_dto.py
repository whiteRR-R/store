from pydantic import BaseModel


class AttributeDTO(BaseModel):
    key: str
