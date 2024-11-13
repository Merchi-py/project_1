from .settings import *
from .db import *
from fastapi import Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse

@app.get("/", response_class=HTMLResponse)
async def main():
    return templates.TemplateResponse("/main.html")