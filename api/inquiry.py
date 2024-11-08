from fastapi import APIRouter
from starlette.requests import Request

from db_connector import query, update

router = APIRouter(prefix="/inquiry")


# Inquiries API List

# Get all inquiries
@router.get("/all")
def all_inquiries():
    return query('SELECT * FROM Inquiry')

# Get inquiries by user ID
@router.post("/user")
async def user_inquiries(request: Request):
    data: dict = await request.json()
    return query("SELECT * FROM Inquiry WHERE userid = %s", (data["userid"],))

# Get inquiry details by inquiry ID
@router.post("/one")
async def one_inquiry(request: Request):
    data: dict = await request.json()
    return query("SELECT * FROM Inquiry WHERE id = %s", (data["id"],))

# Create a new inquiry
@router.post("/create")
async def create_inquiry(request: Request):
    data: dict = await request.json()
    try:
        update("""
            INSERT INTO Inquiry (userid, title, description, attachment, reply) 
            VALUES (%(userid)s, %(title)s, %(description)s, %(attachment)s, %(reply)s)
        """, data)
    except Exception as e:
        print(e)
        return "Error while submitting inquiry"
    return "Inquiry submitted successfully"

# Update inquiry (Modify existing inquiry)
@router.put("/update")
async def update_inquiry(request: Request):
    data: dict = await request.json()
    try:
        update("""
            UPDATE Inquiry SET 
            title = %(title)s, 
            description = %(description)s, 
            attachment = %(attachment)s, 
            reply = %(reply)s 
            WHERE id = %(id)s
        """, data)
    except Exception as e:
        print(e)
        return "Error while updating inquiry"
    return "Inquiry updated successfully"

# Delete inquiry (Remove existing inquiry)
@router.delete("/delete")
async def delete_inquiry(request: Request):
    data: dict = await request.json()
    try:
        update("DELETE FROM Inquiry WHERE id = %s", (data["id"],))
    except Exception as e:
        print(e)
        return "Error while deleting inquiry"
    return "Inquiry deleted successfully"

#Add reply to an inquiry
@router.put("/reply")
async def update_inquiry(request: Request):
    data: dict = await request.json()
    try:
        update("""
            UPDATE Inquiry SET 
            reply = %(reply)s 
            WHERE id = %(id)s
        """, data)
    except Exception as e:
        print(e)
        return "Error while updating inquiry"
    return "Reply Sent successfully"
