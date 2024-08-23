import base64
import json
import random
from hashlib import md5, sha256

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import Response

import mailing
from db_connector import query, update

from . import sample

router = APIRouter(prefix="/api")

router.include_router(sample.router)


@router.get("/")
def root():
    return "Road Eye API v1.0"


@router.post("/login")
async def login(request: Request, response: Response):
    data = await request.json()
    user = query("SELECT * FROM user WHERE (email = %s OR username = %s) AND password = %s", (data["username"], data["username"], sha256(data["password"].encode()).hexdigest()))
    if not user:
        return "Invalid username / password"
    user = user[0]
    user["reg_time"] = None
    user["mod_time"] = None
    json_data = json.dumps(user)
    base64_data = base64.b64encode(json_data.encode()).decode()
    response.set_cookie(key="road-eye-user", value=base64_data)
    return "ok"


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="road-eye-user")


@router.post("/otp")
async def send_otp(request: Request):
    data = await request.json()
    email = data["email"]
    otp = random.randint(111111, 999999)
    update("INSERT INTO otp(email, otp) VALUES (%s, %s)", (email, otp))
    mailing.send_otp(email, otp)


@router.post("/register")
async def register(request: Request):
    data: dict = await request.json()
    data["role"] = 0
    data["password"] = sha256(data["password"].encode()).hexdigest()[:64]
    otp = query("SELECT otp FROM otp WHERE email = %s ORDER BY reg_time DESC LIMIT 1", (data["email"],))
    if len(otp) == 0:
        return "Email not verified"
    if otp[0]["otp"] != data["otp"]:
        return "Invalid OTP"
    try:
        update("INSERT INTO user (first_name, last_name, email, phone, nic, username, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(phone)s, %(nic)s, %(username)s, %(password)s)", data)
    except:
        return "Email already exists"
    return "ok"


@router.post("/vehicle/add")
async def add_vehicle(request: Request):
    data: dict = await request.json()
    try:
        update("INSERT INTO vehicle (user, vehicle_number, brand, model, yom, millage, color, owner, absolute_owner, type) VALUES (%(user)s, %(vehicle_number)s, %(brand)s, %(model)s, %(yom)s, %(millage)s, %(color)s, %(owner)s, %(absolute_owner)s, %(type)s)", data)
    except Exception as e:
        print(e)
        return "Already registered under your account"
    return "ok"


@router.post("/vehicle/list")
async def vehicle_list(request: Request):
    data: dict = await request.json()
    return query("SELECT * FROM vehicle WHERE user = %s", (data["user"],))


@router.post("/vehicle/details")
async def vehicle_details(request: Request):
    data: dict = await request.json()
    return query("SELECT * FROM vehicle WHERE vehicle_id = %s", (data["id"],))[0]


@router.post("/vehicle/delete")
async def vehicle_delete(request: Request):
    data: dict = await request.json()
    update("DELETE FROM vehicle WHERE vehicle_id = %s", (data["id"],))
    return "ok"
