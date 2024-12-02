from settings import *
from db import *
from fastapi import Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse

#main_page
@app.get("/", response_class=HTMLResponse)
async def main(request: Request, db: Session = Depends(get_db)):
    tours = db.query(Tour).all()
    return templates.TemplateResponse("/main.html", {"request": request, "tours": tours})


# registration_model
@app.post("/registration")
async def registration(name: str = Form(), email: str = Form(), password: str = Form(), r_password: str = Form(), is_admin: str = Form() , db: Session = Depends(get_db)):
    if r_password == password:
        return templates.TemplateResponse("registration.html", {"message": "The passwort isn't similar"})
    if is_admin == "Admin123":
        user = User(name=name, email=email, password=password, is_admin=is_admin)
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        return templates.TemplateResponse("registration.html", {"message_admin": "The password is incorrect"})
    user = User(name=name, email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return RedirectResponse("/", status_code=303)

# user_login_page
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

@app.get('/logout')
def logout(request: Request):
    del request.session['user_id']
    request.session['is_auth'] = False
    return RedirectResponse('/', status_code=303)

# admin page

# add tour
@app.post("/add_tour")
async def admin(name: str = Form(), price: int = Form(), description: str = Form(), time: str = Form(), people: int = Form() , db: Session = Depends(get_db)):
    user = db.query(User).filter_by(name=name).first()
    datetime.strptime(time, '%d.%m.%Y') or datetime.strptime(time, '%Y.%m.%d')
    if not user.is_admin:
        return templates.TemplateResponse("/admin.html", {"message": "Wrong password"})
    tours = Tour(name=name, price=price, description=description, time=time, people=people)
    db.add(tours)
    db.commit()
    db.refresh(tours)


#edit tour
app.post("/edit/{tour.id}/tour")
async def edit_tour():
    return {}

#delete tour
# @app.post("/delete_tour/{tour_id}")
# async def delete_tour(db: Session = Depends(get_db)):
#     tour = db.query(Tour).get(id=id)
#     del tour
#     return RedirectResponse("/", status_code=303)