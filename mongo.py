from pymongo import MongoClient


class MongoConector:
    "class to connect with MongoDB"
    def __init__(self) -> None:
        self.client = MongoClient("mongodb://localhost:27017/")
        self.database = self.client["todo"]
        self.collection = self.database["tasks"]

    def get_all_tasks(self) -> list:
        "get all current tasks"
        tasks = self.collection.find()
        return list(tasks)

    def get_single_task(self,task_name: str) -> str:
        "get a task based on name"
        task = self.collection.find_one({"name": task_name})
        return task

    def post_task(self,task: dict) -> str:
        "insert a task in database"
        repeated = self.collection.count_documents({"name": task['name'], "status": "todo"})
     # repeated verify if the currently task is alredy in database.
        if repeated > 0:
            return f"alredy exist a task with the same name: {task['name']}"
        self.collection.insert_one(task)
        return f"task {task['name']} included"

    def delete_task(self,task_name: str) -> None:
        "delete a task in database"
        self.collection.delete_one({"name":task_name,"status": "todo"})

    def change_status(self,task_name: str,status: str) -> None:
        "change the status of task"
        new_status = {"$set": {"status": status}}
        self.collection.update_one({"name": task_name},new_status)

