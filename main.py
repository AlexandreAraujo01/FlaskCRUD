"Api"
from flask import Flask
from flask import jsonify, make_response,request
from mongo import MongoConector

db = MongoConector()
app = Flask(__name__)



@app.route("/AllTasks")
def all_tasks():
    "return all tasks"
    tasks = db.get_all_tasks()
    return make_response(jsonify(tasks=str(tasks)),200)

@app.route("/PostTask",methods=["POST"])
def post_task():
    "cadastra uma task"
    data = request.get_json()
    status = data.get("status","todo")
    response = db.post_task(data["name"],status)
    return make_response(response[0],response[1])

@app.route("/DeleteTask", methods=["DELETE"])
def delete_task():
    "deleta uma tarefa"
    data = request.get_json()
    db.delete_task(data["name"])
    return make_response(f'tarefa {data["name"]} deletada')

@app.route("/UpdateStatus",methods=["PUT"])
def new_status():
    "update task status"
    data = request.get_json()
    response = db.change_status(data["name"],data["status"])
    return make_response(response[0],response[1])










if __name__ == "__main__":
    app.run(debug=True)

