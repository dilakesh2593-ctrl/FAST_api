
from pickletools import pylist
from typing import Optional
import random
from fastapi import Body, FastAPI, Response,status,HTTPException
from pydantic import BaseModel
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating : Optional[int] = None

my_list = [{"Title" : "First post" , "Content" : "Hello there", "id" : 2},
               {"Title" : "Second post" , "Content" : "Hello there", "id" : 3}]

@app.get("/")
def root():
    return {"message": "Hello World Dilakesh and harivishnu"}


def findpost(id):
    for i in my_list:
        if i["id"] == id:
            return i
         
@app.get("/posts")
def user_post():
    return {"message": my_list}

@app.post("/posts" , status_code= status.HTTP_201_CREATED)
def poster(new_post : Post):
    post_dict = new_post.dict()
    post_dict['id'] = random.randint(0, 1000000)
    my_list.append(post_dict)
    return {"message": post_dict}

@app.get("/posts/{id}")
def get_post(id : int):
     
    idvalue = findpost(id)
    if not idvalue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail= {"Message" : "ID value is not found"})
    return{"Data" : idvalue}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    for i in my_list:
        if i["id"] == id:
            my_list.remove(i)
            return {"Message": "Item got removed"}
        
               
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"message" : "Idnotfound"}


@app.put("/posts/{id}")
def updatethetitlee(id: int, post: Post):
    for i, p in enumerate(my_list):
        if p["id"] == id:
            my_post = post.dict()
            my_post["id"] = id
            my_list[i] = my_post
            return {"data": "Updated"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Id not found"
    )

         
      