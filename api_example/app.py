

# data=[{
#     "id":"1","name":"IITM Admin","salary":"16700"
#     },{
#     "id":"2","name":"Ram","salary":"46700"
#     },
#     {
#     "id":"3","name":"Davi","salary":"17000"
#     },
# ]

# @app.route("/employees")
# def get_employees():
#     return data

# @app.route("/employee/<id>")
# def search_employee(id):
#     for e in data:
#         if e["id"] == id:
#             return e
#     return {"message":"Sorry, employee %s is not found!"%(id)},404

# @app.route("/add_emp",methods=["POST"])
# def add_new_emp():
#     id=request.json["id"]
#     name=request.json["name"]
#     salary=request.json["salary"]
#     data.append({"id":id,"name":name,"salary":salary})
#     return {"message":"New record added!"},201

from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource,Api

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///emp_db"
db=SQLAlchemy(app) #app is connected to db
api=Api(app) #app is connected to Api
app.app_context().push() #application from outside modules

#Defining models
class Employee(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    salary=db.Column(db.Float,nullable=False)


#CRUD operations using Restful API
class EmployeeApi(Resource):
    #standard method of request
    def get(self): #Read all the data
        emp_data=Employee.query.all()
        emp_list=[]
        for e in emp_data:
            emp_list.append({"id":e.id,"name":e.name,"salary":e.salary})
        return emp_list
                
    def post(self): #Create new record
        new_emp=Employee(name=request.json["name"],salary=request.json["salary"])
        db.session.add(new_emp)
        db.session.commit()
        return {"message":"New employee is added!"},201
    
    def put(self,id): #update the record
        emp=Employee.query.filter_by(id=id).first()
        if emp:
            #request body
            new_name=request.json['name']
            new_salary=request.json['salary']
            emp.name=new_name
            emp.salary=new_salary
            db.session.commit()
            return {"message":"Employee record updated!"},200
        
        return {"message":"Employee not found!"},404
    
    def delete(self,id): 
        emp=Employee.query.filter_by(id=id).first()
        if emp:
            db.session.delete(emp)
            db.session.commit()
            return {"message":"Employee record deleted!"},200
        return {"message":"Employee not found!"},404
    
class EmployeeSeachApi(Resource):
    def get(self,id): 
        emp_data=Employee.query.filter_by(id=id).first()
        if emp_data:
            json_emp={"id":emp_data.id,"name":emp_data.name,"salary":emp_data.salary}
            return json_emp
        return {"message":"Employee id is not found!"},404


api.add_resource(EmployeeApi,"/myapi/employees",'/myapi/emp/update/<id>', '/myapi/emp/delete/<id>') #<127.0.0.1:5000/myapi/employees based  Method, it will hit get()/post()

api.add_resource(EmployeeSeachApi,"/myapi/employee/<id>") #searching operation


app.run(debug=True)