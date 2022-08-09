"class MongoDB"
from  datetime import datetime
from pymongo import MongoClient
import bson.json_util as json_util




class MongoConector:
    "class to connect with MongoDB"
    def __init__(self) -> None:
        self.client = MongoClient("mongodb://localhost:27017/")
        self.database = self.client["todo"]
        self.collection = self.database["tasks"]

    def get_all_tasks(self) -> list:
        "get all current tasks"
        tasks = self.collection.find()
        return json_util.dumps(list(tasks))

    def get_single_task(self,task_name: str) -> str:
        "get a task based on name"
        task = self.collection.find_one({"name": task_name})
        return json_util.dumps(task)

    def post_task(self,task:str,status:str) -> str:
        "insert a task in database"
        repeated = self.collection.count_documents({"name": task})
     # repeated verify if the currently task is already in database.
        if repeated > 0:
            return [f"already exist a task with the same name: {task}",200]
        self.collection.insert_one({"name": task,"date": datetime.now(),"status": status})
        return [f"task {task} included",200]

    def delete_task(self,task_name: str) -> None:
        "delete a task in database"
        self.collection.delete_one({"name":task_name})

    def delete_many(self,name: str) -> None:
        "delete all tasks"
        self.collection.delete_many({"name": name})

    def change_status(self,task_name: str,status: str) -> str:
        "change the status of task"
        new_status = {"$set": {"status": status}}
        finded = self.collection.count_documents({"name": task_name})
        if finded > 0:
            self.collection.update_one({"name": task_name},new_status)
            return [f"task: {task_name} teve o status atualizado para {status}",201]
        else:
            return [f"task {task_name} não encontrada.",404]
