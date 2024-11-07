from fastapi import APIRouter
from starlette.requests import Request

from db_connector import query, update

router = APIRouter(prefix="/complain")

#Complaints APIS LIST
@router.get("/all")
def all_complaints():
    return query('SELECT * FROM complain')

@router.post("/user")
async def user_complaints(request: Request):
    data: dict = await request.json()
    return query("SELECT * FROM complain WHERE user = %s", (data["user"],))

@router.post("/one")
async def one_complaints(request: Request):
    data: dict = await request.json()
    return query("SELECT * FROM complain WHERE complain_id = %s", (data["id"],))


@router.post("/create")
async def create_complain(request: Request):
    data: dict = await request.json()
    try:
        update("""
            INSERT INTO complain (user, district, police_station, type, subject, complain, proof) 
            VALUES (%(user)s, %(district)s, %(police_station)s, %(type)s, %(subject)s, %(complain)s, %(proof)s)
        """, data)
    except Exception as e:
        print(e)
        return "Error while submitting complain"
    return "Complaint submitted successfully"


# Update complaint (PUT: Modifying existing complaint)
@router.put("/update")
async def update_complain(request: Request):
    data: dict = await request.json()
    try:
        update("""
            UPDATE complain SET 
            district = %(district)s, 
            police_station = %(police_station)s, 
            type = %(type)s, 
            subject = %(subject)s, 
            complain = %(complain)s, 
            proof = %(proof)s 
            WHERE complain_id = %(complain_id)s
        """, data)
    except Exception as e:
        print(e)
        return "Error while updating complain"
    return "Complaint updated successfully"

# Delete complaint (DELETE: Removing existing complaint)
@router.delete("/delete")
async def delete_complain(request: Request):
    data: dict = await request.json()
    try:
        update("DELETE FROM complain WHERE complain_id = %s", (data["complain_id"],))
    except Exception as e:
        print(e)
        return "Error while deleting complain"
    return "Complaint deleted successfully"
