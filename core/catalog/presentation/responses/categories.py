from pydantic import BaseModel


class CategoriesResponse(BaseModel):
    categories: list[dict]

    class Config:
        json_schema_extra = {
            "example": {
                "categories": [
                    {"id": "e842076c-1ceb-4306-a5a6-565e411f7b87", "name": "Electronics", "description": "All electronic items"},
                    {"id": "a1234567-89ab-cdef-0123-456789abcdef", "name": "Books", "description": "All kinds of books"},
                ]
            }
        }
