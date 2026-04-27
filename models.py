#validation class
from pydantic import BaseModel, Field,field_validator,model_validator,computed_field
from typing import Optional

class Product(BaseModel):
    id: int = Field(min_length=2, max_length=100, description="Unique identifier for the course")
    title: str = Field(min_length=2, max_length=100, description="Title of the course")
    instructor: str = Field(min_length=2, max_length=100, description="Instructor of the course")
    category: str = Field(min_length=2, max_length=100, description="Category of the course")
    price: float = Field(gt=0, description="Price of the course")
    duration_hours: float = Field(gt=0, description="Duration of the course in hours")
    is_published: bool = Field(default=False, description="Whether the product is published")
    discount_percent: Optional[float] = Field(default=None, ge=0, le=100, description="Discount percentage for the product")

    @field_validator('instructor')
    @classmethod
    def instructor_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Instructor cannot be empty")
        return v
    
    @field_validator('category')
    @classmethod
    def category_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Category cannot be empty")
        return v
    
    @model_validator(mode="before")
    @classmethod
    #if not is_published and discount_percent is provided, raise error
    def is_published_and_rated(cls, values):
        is_published = values.get('is_published')
        discount_percent = values.get('discount_percent')
        if not is_published and discount_percent is not None:
            raise ValueError("Discount percentage cannot be provided for unpublished courses")
        return values
    
    @computed_field
    @property
    def price_category(self) -> str:
        if self.price <700 :
            return "Budget"
        elif self.price < 1000:
            return "Standard"
        else:
            return "Premium"