from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from db.database import context_get_conn
from sqlalchemy.exc import SQLAlchemyError

from schemas.blog_schema import BlogData

router = APIRouter(prefix="/blogs", tags=["blogs"])

templates = Jinja2Templates(directory="templates") 

# http://127.0.0.1:8002/blogs
