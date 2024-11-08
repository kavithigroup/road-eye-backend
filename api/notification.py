from fastapi import APIRouter
from starlette.requests import Request

from db_connector import query, update

router = APIRouter(prefix="/notification")

#notification
# Get all notifications
@router.get("/all")
def all_notifications():
    return query("SELECT * FROM Notification")

# Get notifications by user ID
@router.post("/user")
async def user_notifications(request: Request):
    data: dict = await request.json()
    return query("SELECT * FROM Notification WHERE userid = %s", (data["userid"],))

# Get notification details by user ID and title (unique notification)
@router.post("/one")
async def one_notification(request: Request):
    data: dict = await request.json()
    return query("SELECT * FROM Notification WHERE userid = %s AND title = %s", (data["userid"], data["title"]))

# Create a new notification
@router.post("/create")
async def create_notification(request: Request):
    data: dict = await request.json()
    try:
        update("""
            INSERT INTO Notification (userid, title, description)
            VALUES (%(userid)s, %(title)s, %(description)s)
        """, data)
    except Exception as e:
        print(e)
        return "Error while creating notification"
    return "Notification created successfully"

# Update notification (Modify existing notification)
@router.put("/update")
async def update_notification(request: Request):
    data: dict = await request.json()
    try:
        update("""
            UPDATE Notification SET 
            description = %(description)s
            WHERE userid = %(userid)s AND title = %(title)s
        """, data)
    except Exception as e:
        print(e)
        return "Error while updating notification"
    return "Notification updated successfully"

# Delete notification (Remove existing notification)
@router.delete("/delete")
async def delete_notification(request: Request):
    data: dict = await request.json()
    try:
        update("DELETE FROM Notification WHERE userid = %s AND title = %s", (data["userid"], data["title"]))
    except Exception as e:
        print(e)
        return "Error while deleting notification"
    return "Notification deleted successfully"
