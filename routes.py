from itertools import product

from utils import read_data,write_data
from fastapi import APIRouter,HTTPException,Query
from typing import Optional
from models import Product

route = APIRouter()

#get data
@route.get("/courses")
def get_courses():
    data = read_data()
    return data

#course by id #Get
@route.get("/courses/{course_id}")
def get_course(course_id: int):
    data = read_data()
    course = next((item for item in data if item["id"] == course_id), None)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

#Post create new course
@route.post("/create_courses")
def create_course(course: Product):
    data = read_data()
    data.append(course.dict())
    write_data(data)
    return course

#PUT update existing course
@route.put("/update_courses/{course_id}")
def update_course(course_id: int, course: Product):
    data = read_data()
    for i, item in enumerate(data):
        if item["id"] == course_id:
            data[i] = course.dict()
            write_data(data)
            return course
    raise HTTPException(status_code=404, detail="Course not found")

#Delete course
@route.delete("/delete_courses/{course_id}")
def delete_course(course_id: int):
    data = read_data()
    data = [item for item in data if item["id"] != course_id]
    write_data(data)
    return {"detail": "Course deleted"}

#GET filter courses by category
@route.get("/courses/filter")
def filter(
    category: Optional[str] = Query(None, description="Category to filter by"),
    price_min: Optional[float] = Query(None, description="Minimum price to filter by"),
    price_max: Optional[float] = Query(None, description="Maximum price to filter by")
):
    data = read_data()
    filtered_courses = data
    if category:
        filtered_courses = [course for course in filtered_courses if course["category"].lower() == category.lower()]
    if price_min is not None:
        filtered_courses = [course for course in filtered_courses if course["price"] >= price_min]
    if price_max is not None:
        filtered_courses = [course for course in filtered_courses if course["price"] <= price_max]


    return filtered_courses

#GET pagination
@route.get("/courses/pagination")
def get_paginated_courses(
    page: int = Query(1, description="Page number"),
    size: int = Query(10, description="Number of courses per page")
):
    data = read_data()
    start = (page - 1) * size
    end = start + size
    paginated_courses = data[start:end]

    return paginated_courses
