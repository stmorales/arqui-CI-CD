from starlette.applications import Starlette
from starlette.routing import Route, Mount
from fastapi import templating

templates = templating.Jinja2Templates(directory="templates")

async def home(request):
    return templates.TemplateResponse("index.html", context={"request": request})

async def about(request):
    return PlainTextResponse("About")

web_app = Starlette(
    routes=[
        Route('/', home, methods=['GET', 'POST']),
    ],
)