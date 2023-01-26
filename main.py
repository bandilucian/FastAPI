
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn

app = FastAPI()


@app.get('/')
def index():
    return {'data': 'blog list'}

# conteaza ordinea pt path urile care incep la fel


@app.get('/blog')  # ?limit=10&published=true de ex
def index(limit=10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {'data': f'{limit} published blogs from db'}
    else:
        return {'data': f'{limit} blogs from db'}


@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'unpublished blogs'}


@app.get('/blog/{id}')
def show(id: int):
    return {'data': id}


@app.get('/blog/{id}/comments')
def comments(id: int, limit=10):
    return {'data': {'1', '2'}}


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.post('/blog')
def create_blog(blog: Blog):

    return {'data': f"blog created with the title {blog.title}"}


# if __name__ == "__main__":
#     uvicorn.run(app, host='127.0.0.1', port=9000)
