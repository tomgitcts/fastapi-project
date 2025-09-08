from fastapi import HTTPException

print("I am from outside main")

from fastapi import FastAPI
import pandas as pd
from pydantic import BaseModel

from database import get_connection


app = FastAPI()
# df = pd.read_csv("data.csv")

@app.get("/")
def home():
    return {"Message": "Welcome to Employee Data API"}

@app.get("/employees")
def get_all_employees():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/employees/{emp_id}")
def get_all_employees(emp_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE id = ?",
                   (emp_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


#  For post endpoint
class Employee(BaseModel):
    name:str
    age: int
    department: str
    salary: float

@app.post("/employees")
def add_employees(emp:Employee):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO employees(name, department, salary, age) VALUES(?,?,?,?)",
        (emp.name, emp.department, emp.salary, emp.age)
    )
    conn.commit()
    conn.close()
    return{"message":"Employee added successfully"}

# Put to update the API data

@app.put('/employees/{emp_id}')
def update_employee(emp_id:int, emp: Employee):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE employees SET name = ?, age = ?, department = ?, salary = ? WHERE id = ?",
        (emp.name, emp.age , emp.department, emp.salary, emp_id,)
    )
    conn.commit()
    conn.close()
    return {"message": f"Employee {emp_id} updated successfully"}

@app.delete('/employees/{emp_id}')
def delete_employee(emp_id:int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM employees  WHERE id = ?",
        (emp_id,)
    )
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code = 404, detail = "Employee not found")
    return {"message": f"Employee {emp_id} deleted successfully"}

# @app.get("/employees")
# def get_all_employees():
#     return df.to_dict(orient="records")

# @app.get("/employees/{emp_id}")
# def get_employee_by_id(emp_id: int):
#     emp = df[df["id"] == emp_id]
#     if emp.empty:
#         return {"error":"Employee not found"}
#     return emp.to_dict(orient = "records")[0]


# @app.post("/employees")
# def add_employee(emp: Employee):
#     global df
#     if emp.id in df["id"].values:
#         return {"error":"Employee with this ID already exists."}
#     new_data = pd.DataFrame([emp.dict()])
#     df = pd.concat([df, new_data], ignore_index = True)
#     return {"Message": "Employee added successfully", "Employee": emp}

# Put to update the API data

# @app.put('/employees/{emp_id}')
# def update_employee(emp_id:int, updated: Employee):
#     global df
#     if emp_id in df['id'].values:
#         df.loc[df['id'] == emp_id,['name', 'department','salary']] =(updated.name, updated.department,updated.salary)
#         return {"message": "Employee updated successfully."}
#     return {"error":"Employee not found"}
#
#
# @app.delete('/employees/{emp_id}')
# def delete_employee(emp_id:int):
#     global df
#     if emp_id in df['id'].values:
#         df = df[df['id'] != emp_id]
#         return {"message":f"Employee {emp_id} deleted"}
#     return {"error":"Employee not found"}
