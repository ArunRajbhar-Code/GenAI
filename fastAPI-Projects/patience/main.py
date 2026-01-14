from fastapi import FastAPI, HTTPException
import json
app=FastAPI()
def load_data():
    with open("patience.json","r") as f:
        data=json.load(f)
    return data    
@app.get("/view")
def view():
    data=load_data()
    return data
@app.get("/patient/{patience_id}")
def view_patience(patience_id:str):
    data=load_data()
    if patience_id in data:
        return data[patience_id]
    # return {"erroe":"patience not found"} this line will generate status code 200 which is not indicating a correct status code hence we will use below code
    raise HTTPException(status_code=404,detail="patient not found")
