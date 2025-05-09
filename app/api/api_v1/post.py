from fastapi import APIRouter, Depends, HTTPException, Request, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from core.authentication import AuthHandler
from models.user import UserUpdate, User, UserOut
from core import security
from uuid import UUID
from models.post import Post


auth_handler = AuthHandler()

router = APIRouter()

@router.get("/post/all",response_description="get all posts")
async def getPosts(request:Request, user_id = Depends(auth_handler.decode_token)):
    if not user_id:
        raise HTTPException(status_code=401, detail="User details not found")
    posts = await Post.find(Post.user_id == UUID(user_id["user_id"])).to_list()
    json_posts = jsonable_encoder(posts)

    return JSONResponse(content=json_posts)

@router.get("/post/{id}",response_description="get single post")
async def getPost(request:Request, id:str, user_id = Depends(auth_handler.decode_token)):
    if not user_id:
        raise HTTPException(status_code=401,detail="User not found")
    print(id)
    post = await Post.get(UUID(id))
    json_post = jsonable_encoder(post)
    return JSONResponse(content=json_post)

@router.post("/post/create", response_description="Upload a post")
async def addPost(request: Request,user_id = Depends(auth_handler.decode_token), newPost: Post = Body(...)):
    # 1. Save the post to DB
    if not user_id:
        raise HTTPException(status_code=401,detail="User not found!")
    newPost.user_id = UUID(user_id["user_id"])
 
    await newPost.save()


    return {
        "message": "Post uploaded successfully",
        "post_id": str(newPost.id),
        "post": newPost
    }

@router.put("/",response_description="update a post")
async def updatePost(request:Request):
    return {"updated your post"}

@router.delete("/post/delete/{id}",response_description="update a post")
async def deletePost(request:Request, id:str, user_id = Depends(auth_handler.decode_token)):
    if not user_id:
        raise HTTPException(status_code=401,detail="User not found")
    post = await Post.get(UUID(id))
    if post:
       await post.delete()
    else:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"deleted your post"}