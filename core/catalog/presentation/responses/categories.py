from pydantic import BaseModel


class CategoriesResponse(BaseModel):
    categories: list[dict]

    class Config:
        schema_extra = {
            "example": {
                "categories": [
                    {"id": 1, "name": "Electronics", "description": "All electronic items"},
                    {"id": 2, "name": "Books", "description": "All kinds of books"},
                ]
            }
        }
