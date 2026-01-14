from fastapi import FastAPI
app=FastAPI()
@app.get("/")
def hello():
    return {"message", "hello"}
@app.get("/about")
def about():
    return {"message","welcome to about page"}