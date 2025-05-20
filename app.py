from flask import Flask, jsonify, request

app = Flask(__name__)

# Données fictives en mémoire
tasks = [
    {"id": 1, "title": "Apprendre Flask", "done": False},
    {"id": 2, "title": "Créer une API", "done": False}
]

# Route de bienvenue
@app.route("/")
def index():
    return "Bienvenue sur l'API TODO Flask!"

# Obtenir toutes les tâches
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

# Obtenir une tâche par son id
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Tâche non trouvée"}), 404
    return jsonify(task)

# Ajouter une nouvelle tâche
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    if not data or "title" not in data:
        return jsonify({"error": "Le titre est requis"}), 400
    new_task = {
        "id": tasks[-1]["id"] + 1 if tasks else 1,
        "title": data["title"],
        "done": False
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

# Mettre à jour une tâche
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Tâche non trouvée"}), 404
    data = request.json
    task["title"] = data.get("title", task["title"])
    task["done"] = data.get("done", task["done"])
    return jsonify(task)

# Supprimer une tâche
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"message": "Tâche supprimée"}), 200

if __name__ == "__main__":
    app.run(debug=True)
