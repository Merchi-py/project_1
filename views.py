from settings import *
from db import *
from fastapi import Request, Form, Depends, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.exc import IntegrityError
from functools import wraps


def login_required(endpoint):
    @wraps(endpoint)
    async def wrapper(request: Request, *args, **kwargs):
        if not request.session.get("is_auth", False):
            return RedirectResponse("/login", status_code=303)
        return await endpoint(request, *args, **kwargs)
    return wrapper


#main_page
@app.get("/", response_class=HTMLResponse)
@login_required
async def main(request: Request, db: Session = Depends(get_db)):
    tours = db.query(Tour).all()
    user = db.query(User).get(request.session["user_id"])
    return templates.TemplateResponse("main.html", {"request": request, "tours": tours, "user": user})


@app.post("/")
@login_required
async def main_post(request: Request, price : int = Form(), db: Session = Depends(get_db)):
    price_tours = db.query(Tour).filter_by(price=price)
    user = db.query(User).get(request.session["user_id"])
    tours = ""
    for t in price_tours:
        if user.is_admin:

            tours += f"""<img style='height: 250px; width: 350px;' src='/static/images/{t.id}.jpg'>
             <h4><u>{t.name}</u></h4>
             <h5>{t.price}$</h5>
             <h6>{t.description}</h6>
             <h6>{t.from_time}</h6>
             <h6>{t.to_time}</h6>
             <h6>{t.people} Перосона/ни</h6>
             <button class='btn btn-primary add_to_basket' data-url='/add_basket/{t.id}'>Додати
             </button>
             <div class='action-buttons'>
                <a class='deleteTour btn btn-white'>🗑️</a>
                <a href='/edit_tour/{t.id}' class='btn btn-white'>🖌️</a>
            </div>
             """
        else:
            tours += f"""<img style='height: 250px; width: 350px;' src='/static/images/{t.id}.jpg'>
                         <h4><u>{t.name}</u></h4>
                         <h5>{t.price}$</h5>
                         <h6>{t.description}</h6>
                         <h6>{t.from_time}</h6>
                         <h6>{t.to_time}</h6>
                         <h6>{t.people} Перосона/ни</h6>
                         <button class='btn btn-primary add_to_basket' data-url='/add_basket/{t.id}'>Додати
                         </button>
                         """



    return {"tours": tours}

# user_registration_page
@app.get('/registration', response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse('registration.html', {"request": request})

@app.post("/registration")
async def registration(request: Request, name: str = Form(),
                       email: str = Form(), password: str = Form(),
                       r_password: str = Form(), is_admin: str = Form() , db: Session = Depends(get_db)):
    if r_password != password:
        return templates.TemplateResponse("registration.html", {"message": "The passwort isn't similar", "request": request})
    if is_admin == "Admin123":
        user = User(name=name, email=email, password=password, is_admin=True)
    else:
        user = User(name=name, email=email, password=password)
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError:
        return templates.TemplateResponse("registration.html", {"message_error_email": "Name or Email or Password are busy", "request": request})
    request.session['user_id'] = user.id
    request.session['is_auth'] = True
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

@app.get("/add_tour", response_class=HTMLResponse)
@login_required
async def add_tour_page(request: Request):
    return templates.TemplateResponse("/add_tour.html", {"request": request})



@app.post("/add_tour")
@login_required
async def add_tour(
        request: Request, name: str = Form(),
        price: int = Form(), description: str = Form(),
        from_time: str = Form(),
        to_time: str = Form(),
        people: int = Form(),
        file: UploadFile = File(),
        db: Session = Depends(get_db)):
    user = db.query(User).get(request.session["user_id"])
    if not user.is_admin:
        return templates.TemplateResponse("/admin.html", {"message": "Wrong password"})
    from_time = datetime.strptime(from_time, '%Y-%m-%d')
    to_time = datetime.strptime(to_time, '%Y-%m-%d')
    tours = Tour(name=name, price=price, description=description, from_time=from_time, to_time=to_time, people=people)
    db.add(tours)
    db.commit()
    with open(f'static/images/{tours.id}.jpg', 'wb') as image:
        content = await file.read()
        image.write(content)
        tours.picture = f"/static/images/{tours.id}.jpg"
    db.add(tours)
    db.commit()
    db.refresh(tours)
    return RedirectResponse("/", status_code=303)


#edit tour
@app.get("/edit_tour/{tour_id}")
@login_required
async def edit_tour_page(request: Request, tour_id, db: Session = Depends(get_db)):
    tour = db.query(Tour).get(tour_id)
    return templates.TemplateResponse("/edit_tour.html", {"request": request, "tour": tour})



@app.post("/edit_tour/{tour_id}")
@login_required
async def edit_tour(
                    request: Request,
                    tour_id: int,
                    name: str = Form(),
                    price: int = Form(),
                    description: str = Form(),
                    from_time: str = Form(),
                    to_time: str = Form(),
                    people: int = Form(),
                    db: Session = Depends(get_db)
                    ):
    tour = db.query(Tour).get(tour_id)
    if not to_time or from_time:
        tour.name = name
        tour.price = price
        tour.description = description
        tour.people = people
        db.add(tour)
        db.commit()
        db.refresh(tour)
    else:
        from_time = datetime.strptime(from_time, '%Y-%m-%d')
        to_time = datetime.strptime(to_time, '%Y-%m-%d')
        tour.name = name
        tour.price = price
        tour.description = description
        tour.from_time = from_time
        tour.to_time = to_time
        tour.people = people
        db.add(tour)
        db.commit()
        db.refresh(tour)
    return RedirectResponse("/", status_code=303)



# delete tour
@app.post("/delete_tour/{tour_id}")
@login_required
async def delete_tour(request: Request, tour_id: int, db: Session = Depends(get_db)):
    tour = db.query(Tour).get(tour_id)
    db.delete(tour)
    db.commit()
    return {}


@app.post("/add_basket/{tour_id}")
async def add_basket(request: Request, tour_id: str):
    if not request.session.get("basket"):
        request.session["basket"] = {}
    if request.session['basket'].get(tour_id) is None:
        request.session["basket"][tour_id] = 1
    else:
        request.session["basket"][tour_id] += 1
    return {}


@app.post("/basket")
async def basket(request: Request, db: Session = Depends(get_db)):
    basket = ""
    for id, amount in request.session["basket"].items():
        tour = db.query(Tour).get(int(id))
        basket += f"{tour.name} {tour.price * amount}: {amount}"
    return {"basket": basket}




@app.post("/buy")
@login_required
async def buy(request: Request, db: Session = Depends((get_db))):
    user = db.query(User).get(request.session["user_id"])
    for b in request.session["basket"]:
        tours = db.query(Tour).get(b)
        if user.balance <= tours.price:
            message = "Not enough money"
            return {"message": message}
    return {}
