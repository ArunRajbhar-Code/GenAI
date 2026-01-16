# Import FastAPI framework to create APIs
from fastapi import FastAPI, HTTPException

# Used to return custom JSON responses with status codes
from fastapi.responses import JSONResponse

# BaseModel is used to define request/response schemas
# Field is used for validation and documentation
# computed_field is used to create derived fields (Pydantic v2)
from pydantic import BaseModel, Field, computed_field

# json module is used to read/write JSON files
import json

# Used for type hints and validation
from typing import Annotated, Literal, Optional


# -------------------- Patient Model --------------------
# This model defines the structure of a patient record
class patient(BaseModel):

    # Patient ID (mandatory)
    id: Annotated[str, Field(..., description="ID of the patient", example="P001")]

    # Patient name
    name: Annotated[str, Field(..., description="Name of the patient")]

    # Patient city
    city: Annotated[str, Field(..., description="City of the patient")]

    # Patient age (must be between 1 and 119)
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient")]

    # Gender must be one of the given values
    gender: Annotated[
        Literal["male", "female", "other"],
        Field(..., description="gender of the patient")
    ]

    # Height in meters (must be > 0)
    height: Annotated[float, Field(..., gt=0, description="Height of the patient")]

    # Weight in kg (must be > 0)
    weight: Annotated[float, Field(..., gt=0, description="Weight of the patient")]

    # -------------------- Computed BMI --------------------
    # This field is automatically calculated, not stored
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi

    # -------------------- BMI Verdict --------------------
    # Another computed field based on BMI value
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.50:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Normal"
        else:
            return "Obese"


# -------------------- Update Model --------------------
# This model is used for updating patient data
# All fields are OPTIONAL so partial updates are allowed
class patientUpdate(BaseModel):

    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(gt=0, lt=120, default=None)]
    gender: Annotated[
        Optional[Literal["male", "female", "other"]],
        Field(default=None)
    ]
    height: Annotated[Optional[float], Field(gt=0, default=None)]
    weight: Annotated[Optional[float], Field(gt=0, default=None)]


# -------------------- FastAPI App --------------------
# Create FastAPI application instance
app = FastAPI()


# -------------------- Load Data Function --------------------
# Reads patient data from JSON file
def load_data():
    with open("patience.json", "r") as f:
        data = json.load(f)
    return data


# -------------------- Save Data Function --------------------
# Writes patient data back to JSON file
def save_data(data):
    with open("patience.json", "w") as f:
        json.dump(data, f)


# -------------------- Home Route --------------------
# Simple welcome endpoint
@app.get("/")
def home():
    return {"message": "welcome to home page"}


# -------------------- View All Patients --------------------
# Returns all patients data
@app.get("/view")
def view():
    data = load_data()
    return data


# -------------------- View Single Patient --------------------
# Fetch patient using patient ID
@app.get("/patient/{patience_id}")
def view_patience(patience_id: str):

    # Load existing data
    data = load_data()

    # If patient exists, return patient data
    if patience_id in data:
        return data[patience_id]

    # If patient not found, raise proper HTTP error
    raise HTTPException(status_code=404, detail="patient not found")


# -------------------- Create Patient --------------------
# Adds a new patient
@app.post("/create")
def create_patient(patient: patient):

    # Load existing patient data
    data = load_data()

    # Check if patient ID already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exist")

    # Store patient data without ID (ID is used as key)
    data[patient.id] = patient.model_dump(exclude=['id'])

    # Save updated data to JSON file
    save_data(data)

    # Return success response
    return JSONResponse(
        status_code=201,
        content={"message": "Patient added successfully"}
    )


# -------------------- Update Patient --------------------
# Updates an existing patient using patient ID
@app.put("/edit/{patient_id}")
def update_patient(patient_id: str, patient_update: patientUpdate):

    # Load existing data
    data = load_data()

    # Check if patient exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="patient not found")

    # Get existing patient information
    patient_info = data[patient_id]

    # Extract only fields that were sent in request
    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    # Update existing patient data with new values
    for key, value in updated_patient_info.items():
        patient_info[key] = value

    # Add ID back for validation
    patient_info['id'] = patient_id

    # Validate updated data using Pydantic model
    patient_pydantic_obj = patient(**patient_info)

    # Remove ID again before saving
    patient_info = patient_pydantic_obj.model_dump(exclude={'id'})

    # Save updated patient data
    data[patient_id] = patient_info
    save_data(data)

    # Return success response
    return JSONResponse(
        status_code=200,
        content={"message": "patient updated"}
    )
@app.delete("/delete/{patient_id}")
def delete_patient(patient_id:str):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail="patient not found")
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200,content={"message":"patient deleted"})

