from sqlalchemy.orm import session

from settings import *
from db import *
from fastapi import Request, Form, Depends, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse


def login_requiered(endpoint):
    def wrapper(request, *args, **kwargs):
        if not request.session.get("is_authentificated", False):
            return RedirectResponse("/login", status_code=303)
        endpoint(request, *args, **kwargs)
        return wrapper()

#main_page
@app.post("/")
async def main_post(price: int = Form(), db: Session = Depends(get_db)):
    price_tours = db.query(Tour).filter_by(price=price)
    tours = ""
    for t in price_tours:
        tours += f"{t.name} {t.price} {t.description} {t.people} {t.time} {t.picture}"
    return {"tours": tours}

@login_requiered
@app.get("/", response_class=HTMLResponse)
async def main(request: Request, db: Session = Depends(get_db)):
    tours = db.query(Tour).all()
    user = db.query(User).get(request.session["user_id"])
    return templates.TemplateResponse("main.html", {"request": request, "tours": tours, "user": user})

# user_registration_page
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

# add tour
@login_requiered
@app.get("/add_tour", response_class=HTMLResponse)
async def add_tour_page(request: Request):
    return templates.TemplateResponse("/add_tour.html", {"request": request})


@login_requiered
@app.post("/add_tour")
async def add_tour(request: Request, name: str = Form(), price: int = Form(), description: str = Form(), from_time: str = Form(), to_time: str = Form(), people: int = Form(), db: Session = Depends(get_db)):
    user = db.query(User).get(request.session["user_id"])
    if not user.is_admin:
        return templates.TemplateResponse("/admin.html", {"message": "Wrong password"})
    from_time = datetime.strptime(from_time, '%Y-%m-%d')
    to_time = datetime.strptime(to_time, '%Y-%m-%d')
    tours = Tour(name=name, price=price, description=description, from_time=from_time, to_time=to_time, people=people)
    db.add(tours)
    db.commit()
    db.refresh(tours)
    return RedirectResponse("/", status_code=303)


#edit tour
@login_requiered
@app.get("/edit_tour/{tour.id}", response_class=HTMLResponse)
async def edit_tour_page(id, request: Request, db: Session = Depends(get_db)):
    tour = db.query(Tour).get(id=id)
    return templates.TemplateResponse("/edit_tour.html", {"request": request})


@login_requiered
@app.post("/edit_tour/{tour.id}")
async def edit_tour(id, name: str = Form(), price: int = Form(), description: str = Form(), time: str = Form(), people: int = Form(), db: Session = Depends(get_db)):
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


@login_requiered
# delete tour
@app.post("/delete_tour/{tour_id}")
async def delete_tour(tour_id: int, db: Session = Depends(get_db)):
    tour = db.query(Tour).get(tour_id)
    del tour
    return RedirectResponse("/", status_code=303)

@login_requiered
@app.post("/add_basket/{id}")
async def add_basket(id: int, request: Request):
    if not request.session.get("basket"):
        request.session["basket"] = []
    request.session["basket"].append(id)
    return RedirectResponse("/", status_code=303)

@login_requiered
@app.post("/basket")
async def basket(request: Request, db: Session = Depends(get_db)):
    if not request.session.get("basket"):
        request.session["basket"] = []
    basket = ""
    for b in request.session["basket"]:
        tour = db.query(Tour).get(b)
        basket += f"{tour.name} {tour.price}"
    return {"basket": basket}


@login_requiered
@app.post("/buy")
async def buy(request: Request, db: Session = Depends((get_db))):
    user = db.query(User).get(request.session["user_id"])
    for b in request.session["basket"]:
        tours = db.query(Tour).get(b)
        if user.balance <= tours.price:
            message = "Not enough money"
            return {"message": message}
    return {}
