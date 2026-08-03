# from fastapi import APIRouter, Request
# from fastapi.templating import Jinja2Templates

# router = APIRouter()

# templates = Jinja2Templates(directory="app/templates")


# @router.get("/")
# def home(request: Request):
#     return templates.TemplateResponse(
#         "home.html",
#         {"request": request}
#     )
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def home():
    return {
        "message": "Welcome to AI Resume Optimizer"
    }