from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
import json
from typing import Annotated,Literal,Optional
class patient(BaseModel):
    id:Annotated[str,Field(...,description="ID of the patient",example="P001")]
    name: Annotated[str,Field(...,description="Name of the patient")]
    city:Annotated[str,Field(...,description="City of the patient")]
    age:Annotated[int,Field(...,gt=0,lt=120,description="Age of the patient")]
    gender:Annotated[Literal["male","female","other"],Field(...,description="gender of the patient")]
    height:Annotated[float,Field(...,gt=0,description="Height of the patient")]
    weight:Annotated[float,Field(...,gt=0,description="Weight of the patient")]
    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18.50:
            return "Underweight"
        elif self.bmi<25:
            return "Normal"
        elif self.bmi<30:
            return "Normal"
        else:
            return "Obese"
class patientUpdate(BaseModel):
        name: Annotated[Optional[str],Field(default=None)]
        city:Annotated[Optional[str],Field(default=None)]
        age:Annotated[Optional[int],Field(gt=0,lt=120,default=None)]
        gender:Annotated[Optional[Literal["male","female","other"]],Field(default=None)]
        height:Annotated[Optional[float],Field(gt=0,default=None)]
        weight:Annotated[Optional[float],Field(gt=0,default=None)]


app=FastAPI()
def load_data():
    with open("patience.json","r") as f:
        data=json.load(f)
    return data  
def save_data(data):
    with open("patience.json","w") as f:
        json.dump(data,f) 
@app.get("/")
def home():
    return {"message":"welcome to home page"}        
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
@app.post("/create")
def create_patient(patient:patient):
    #load existing data
    data=load_data()
    #check if patient already exist
    if patient.id in data:
        raise HTTPException(status_code=400,detail="Patient already exist")
    #new patient added in DB
    data[patient.id]=patient.model_dump(exclude=['id'])
    save_data(data)
    return JSONResponse(status_code=201,content={"message":"Patient added successfully"})
@app.put("/edit/{patient_id}")
def update_patient(patient_id:str, patient_update: patientUpdate):
    data=load_data()
    if patient_id in data:
        raise HTTPException(status_code=404,detail="patient not found")
    patient_info=data[patient_id]
    updated_patient_info=patient_update.model_dump(exclude_unset=True)
    for key,value in updated_patient_info.items():
        patient_info[key]=value
    patient_info['id']=patient_id
    patient_pydantic_obj=patient(**patient_info)
    patient_info=patient_pydantic_obj.model_dump(exclude='id')   
    data[patient_id]=patient_info 
    save_data(data)
    return JSONResponse(status_code=200,content={"messsage",'patient updated'})
# adding this code



