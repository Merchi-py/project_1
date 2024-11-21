from .settings import *
from .db import *
from fastapi import Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse

@app.get("/", response_class=HTMLResponse)
async def main():
    return templates.TemplateResponse("/main.html")

@app.get("/registration", response_class=HTMLResponse)
async def registration(request: Request):
    return templates.TemplateResponse("/registration.html", {"request": request})


@app.post("/registration")
async def registration(username: str = Form(), email: str = Form(), password: str = Form(), db: Session = Depends(get_db)):
    user = User(name=username, email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return RedirectResponse("/", status_code=303)

@app.get('/login', response_class=HTMLResponse)
def login(request: Request, after_fail: bool = False):
    context = {'request': request}
    if after_fail:
        context['message'] = 'Username or password is incorrect'
    return templates.TemplateResponse('login.html', context)


@app.post('/login')
def login(request: Request, name: str = Form(), password: str = Form(), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(name=name).first()
    if user is None or user.password != password:
        return RedirectResponse('/login?after_fail=True', status_code=303)
    request.session['user_id'] = user.id
    request.session['is_auth'] = True
    return RedirectResponse('/', status_code=303)