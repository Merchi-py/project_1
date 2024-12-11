from settings import *
from db import *
from fastapi import Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse

#main_page
@app.get("/", response_class=HTMLResponse)
async def main(request: Request, db: Session = Depends(get_db)):
    tours = db.query(Tour).all()
    user = db.query(User).get(id=id)
    return templates.TemplateResponse("main.html", {"request": request, "tours": tours, "user": user})


@app.get('/registration', response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse('registration.html', {"request": request})

@app.post("/registration")
async def registration(request: Request, name: str = Form(), email: str = Form(), password: str = Form(), r_password: str = Form(), is_admin: str = Form() , db: Session = Depends(get_db)):
    if r_password != password:
        return templates.TemplateResponse("registration.html", {"message": "The passwort isn't similar", "request": request})
    if is_admin == "Admin123":
        user = User(name=name, email=email, password=password, is_admin=True)
    else:
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

@app.get("/add_tour", response_class=HTMLResponse)
async def add_tour_page(request: Request):
    return templates.TemplateResponse("/add_tour.html", {"request": request})


@app.post("/add_tour")
async def add_tour(name: str = Form(), price: int = Form(), description: str = Form(), time: str = Form(), people: int = Form() , db: Session = Depends(get_db)):
    user = db.query(User).filter_by(name=name).first()
    if not user.is_admin:
        return templates.TemplateResponse("/admin.html", {"message": "Wrong password"})
    datetime.strptime(time, '%d.%m.%Y') or datetime.strptime(time, '%Y.%m.%d')
    tours = Tour(name=name, price=price, description=description, time=time, people=people)
    db.add(tours)
    db.commit()
    db.refresh(tours)


#edit tour



@app.get("/edit_tour/{tour.id}", response_class=HTMLResponse)
async def edit_tour_page(request: Request):
    return templates.TemplateResponse("/edit_tour.html", {"request": request})
@app.post("/edit_tour/{tour.id}")
async def edit_tour(name: str = Form(), price: int = Form(), description: str = Form(), time: str = Form(), people: int = Form(), db: Session = Depends(get_db)):
    tours = db.query(Tour).get(id=id)
    datetime.strptime(time, '%d.%m.%Y') or datetime.strptime(time, '%Y.%m.%d')
    tours.name = name
    tours.price = price
    tours.description = description
    tours.time = time
    tours.people = people
    tour = Tour(name=name, price=price, description=description, time=time, people=people)
    db.add(tour)
    db.commit()
    db.refresh(tour)
    return RedirectResponse("/", status_code=303)



# delete tour
# @app.post("/delete_tour/{tour_id}")
# async def delete_tour(db: Session = Depends(get_db)):
#     tour = db.query(Tour).get(id=id)
#     del tour
#     return RedirectResponse("/", status_code=303)