from fastapi import APIRouter, Depends, HTTPException, Request, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from core.authentication import AuthHandler
from beanie.operators import And, Eq, GT, LT
from beanie import Link, WriteRules
from core import security
from uuid import UUID
from models.post import Post
from models.user import User


auth_handler = AuthHandler()

router = APIRouter()

@router.get("/post/all",response_description="get all posts")
async def getPosts(request:Request, user_id = Depends(auth_handler.decode_token)):
    if not user_id:
        raise HTTPException(status_code=401, detail="User details not found")
    posts = await Post.find(Post.user_id == UUID(user_id["user_id"])).to_list()
    json_posts = jsonable_encoder(posts)

    return JSONResponse(content=json_posts)

@router.get("/post/findposts",response_description="get all posts")
async def findPosts(request:Request, type:str, city:str, maxPrice:int, minPrice:int, user_id = Depends(auth_handler.decode_token)):
    if not user_id:
        raise HTTPException(status_code=401, detail="User details not found")
    posts = await Post.find(And(
            Eq(Post.c_type, type.lower()),
            Eq(Post.city, city),
            GT(Post.price, minPrice),
            LT(Post.price, maxPrice)
        )
                            ).to_list()
    print("Found:",posts)
    json_posts = jsonable_encoder(posts)
    return JSONResponse(content=json_posts)

@router.get("/post/get-saved")
async def get_saved_posts(user_id= Depends(auth_handler.decode_token)):
    if not user_id:
        raise HTTPException(status_code=401,detail="User not found")
    user = await User.get(UUID(user_id["user_id"]))
    await user.fetch_link("saved_posts")
    saved_posts = user.saved_posts

    
    print("Printing id of saved posts")
    saved_post_ids = []
    for post in saved_posts:
        saved_post_ids.append(str(post.id))
    saved_json_posts = jsonable_encoder(saved_post_ids)
    return JSONResponse(content=saved_json_posts)


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

@router.post("/post/save/{post_id}")
async def save_post(post_id: str, user_id = Depends(auth_handler.decode_token)):
    if not user_id:
        raise HTTPException(status_code=401,detail="User not found")
    user = await User.get(UUID(user_id["user_id"]))

    post = await Post.get(UUID(post_id))

    if not post:
        raise HTTPException(status_code=404, detail="Post not found!")
    
    await user.fetch_link("saved_posts")

    if any(link.id == post.id for link in user.saved_posts):
        res = {"isSaved":True}
        res = jsonable_encoder(res)
        return JSONResponse(content=res, status_code=200)
    
    user.saved_posts.append(post)
    await user.save(link_rule=WriteRules.WRITE)
    return {"message":"Post Saved!"}

@router.post("/post/unsave/{post_id}")
async def unsave_post(post_id: str, user_id = Depends(auth_handler.decode_token)):
    if not user_id:
        raise HTTPException(status_code=401,detail="User not found")
    user = await User.get(UUID(user_id["user_id"]))
    post = await Post.get(UUID(post_id))
    if not post:
        raise HTTPException(status_code=404, detail="Post not found!")
    
    await user.fetch_link("saved_posts")
    user.saved_posts = [p for p in user.saved_posts if p.id != post.id]
    await user.save(link_rule=WriteRules.WRITE)
    return {"message": "Post Unsaved"}

