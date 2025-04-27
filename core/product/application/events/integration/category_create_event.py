from dataclasses import dataclass


@dataclass
class CategoryCreateEvent:
    category_id: str
    category_name: str

