from pydantic import BaseModel


class CategoryCreateRequest(BaseModel):
    name: str
    description: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Electronics",
                "description": "All electronic items",
            }
        }


