from fastapi import APIRouter
from starlette.requests import Request

from db_connector import query, update

router = APIRouter(prefix="/post")

# Posts API List

# Get all posts
@router.get("/all")
def all_posts():
    return query("SELECT * FROM Post")

# Get posts by user ID
@router.post("/user")
async def user_posts(request: Request):
    data: dict = await request.json()
    return query("SELECT * FROM Post WHERE userid = %s", (data["userid"],))

# Get post details by post ID
@router.post("/one")
async def one_post(request: Request):
    data: dict = await request.json()
    return query("SELECT * FROM Post WHERE id = %s", (data["id"],))

# Create a new post
@router.post("/create")
async def create_post(request: Request):
    data: dict = await request.json()
    try:
        update("""
            INSERT INTO Post (userid, video_link, likes, views, description, title) 
            VALUES (%(userid)s, %(video_link)s, %(likes)s, %(views)s, %(description)s, %(title)s)
        """, data)
    except Exception as e:
        print(e)
        return "Error while creating post"
    return "Post created successfully"

# Update post (Modify existing post)
@router.put("/update")
async def update_post(request: Request):
    data: dict = await request.json()
    try:
        update("""
            UPDATE Post SET 
            video_link = %(video_link)s, 
            likes = %(likes)s, 
            views = %(views)s, 
            description = %(description)s, 
            title = %(title)s
            WHERE id = %(id)s
        """, data)
    except Exception as e:
        print(e)
        return "Error while updating post"
    return "Post updated successfully"

# Delete post (Remove existing post)
@router.delete("/delete")
async def delete_post(request: Request):
    data: dict = await request.json()
    try:
        update("DELETE FROM Post WHERE id = %s", (data["id"],))
    except Exception as e:
        print(e)
        return "Error while deleting post"
    return "Post deleted successfully"


# Comments API List within Post

# Get all comments for a post
@router.get("/{post_id}/comments")
def all_comments(post_id: int):
    return query("SELECT * FROM Comment WHERE postid = %s", (post_id,))

# Get comments by user ID
@router.post("/comments/user")
async def user_comments(request: Request):
    data: dict = await request.json()
    return query("SELECT * FROM Comment WHERE userid = %s", (data["userid"],))

# Get comment details by comment ID
@router.post("/comments/one")
async def one_comment(request: Request):
    data: dict = await request.json()
    return query("SELECT * FROM Comment WHERE commentid = %s", (data["commentid"],))

# Create a new comment on a post
@router.post("/{post_id}/comments/create")
async def create_comment(post_id: int, request: Request):
    data: dict = await request.json()
    data["postid"] = post_id  # Ensure post ID is set in data
    try:
        update("""
            INSERT INTO Comment (postid, userid, comment) 
            VALUES (%(postid)s, %(userid)s, %(comment)s)
        """, data)
    except Exception as e:
        print(e)
        return "Error while creating comment"
    return "Comment created successfully"

# Update comments on post
@router.put("/comments/update")
async def update_comment(request: Request):
    data: dict = await request.json()
    try:
        update("""
            UPDATE Comment SET 
            comment = %(comment)s
            WHERE commentid = %(commentid)s
        """, data)
    except Exception as e:
        print(e)
        return "Error while updating comment"
    return "Comment updated successfully"

# Delete comment (Remove existing comment)
@router.delete("/comments/delete")
async def delete_comment(request: Request):
    data: dict = await request.json()
    try:
        update("DELETE FROM Comment WHERE commentid = %s", (data["commentid"],))
    except Exception as e:
        print(e)
        return "Error while deleting comment"
    return "Comment deleted successfully"

