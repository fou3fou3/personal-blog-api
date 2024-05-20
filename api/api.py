from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from api.database import *
from api.config import *

app = FastAPI()

conn = psycopg2.connect(
	dbname=DB_INFO['name'],
	user=DB_INFO['usr'],
	password=DB_INFO['passwd'],
	host=DB_INFO['host'],
	port=DB_INFO['port']
)


class CreatePost(BaseModel):
	title: str
	article: str

class UpdatePost(BaseModel):
	post_id: int
	title: str
	article: str


@app.get("/")
def root():
	return {"message": "Api working properly ."}


@app.get("/post/{id}", status_code=200)
def fetch_post(id: int, response: Response):
	post = db_fetch_post(conn, id)
	if post:
		return {"message": "Post was fetch successfully !", "post": post}
	response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
	return {"message": "There was a problem fetching the post ): .", "post": None}

@app.post("/post/create", status_code=200)
def create_post(post_data: CreatePost, response: Response):
	confirmation = db_create_post(conn, post_data.title, post_data.article)
	if confirmation:
		return {"message": "Post was created successfully"}
	
	return {"message": "There was a problem creating the post ): ."}

@app.put("/post/update", status_code=200)
def update_post(post_data: UpdatePost, response: Response):
	confirmation = db_update_post(conn, post_data.post_id, post_data.title, post_data.article)
	if confirmation:
		return {"message": "Post was updated successfully"}
	response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
	return {"message": "There was a problem updating the post ): ."}

@app.delete("/post/delete/{id}", status_code=200)
def delete_post(id: int, response: Response):
	confirmation = db_delete_post(conn, id)
	if confirmation:
		return {"message": "Post was deleted successfully"}
	response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
	return {"message": "There was a problem deleting the post ): ."}


@app.get("/posts", status_code=200)
def fetch_posts(response: Response):
	post = db_fetch_posts(conn, id)
	if post:
		return {"message": "Posts were fetch successfully !", "posts": post}
	response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
	return {"message": "There was a problem fetching the posts ): .", "posts": None}