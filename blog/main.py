from fastapi import FastAPI, Depends, status, Response, HTTPException
from schemas import BlogBase
from database import Base
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from models import Blog

app = FastAPI()

Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: BlogBase, db: Session = Depends(get_db)):
    new_blog = Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog')
def get_all(db: Session = Depends(get_db)):
    blogs = db.query(Blog).all()
    return blogs


@app.delete('/blog/{pk}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(pk: int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == pk)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {pk} was not found')
    blog.delete(synchronize_session='evaluate')
    db.commit()
    return {'deleted': "object"}


@app.put('/blog/{pk}', status_code=status.HTTP_202_ACCEPTED)
def update(pk: int, request: BlogBase, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == pk)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {pk} was not found')
    blog.update(request.__dict__)
    db.commit()
    return 'updated'


@app.get('/blog/{pk}', status_code=status.HTTP_200_OK)
def show(pk: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == pk).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with id {pk} is not available')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f'Blog with id {pk} is not available'}
    return blog
