from pydantic import BaseModel
class patient(BaseModel):
    name :str
    age :int

def insert_patient(patient :patient):
    print(patient.name)
    print(patient.age)

patient_info={"name":"Arun","age":24}
p1=patient(**patient_info)#creating object of patient by passing dictionary as argument
insert_patient(p1)    # calling function and passing above object
