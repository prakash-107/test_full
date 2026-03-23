import os

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)

# Connect to MongoDB Atlas
client = MongoClient(os.getenv("MONGO_URI"))
db = client["crud_db"]
items_collection = db["items"]

@app.route("/")
def home():
    return render_template("index.html")

# CRUD APIs
@app.route("/items", methods=["GET"])
def get_items():
    items = []
    for item in items_collection.find():
        items.append({"_id": str(item["_id"]), "name": item["name"]})
    return jsonify(items)

@app.route("/items", methods=["POST"])
def add_item():
    data = request.json
    result = items_collection.insert_one({"name": data["name"]})
    return jsonify({"_id": str(result.inserted_id), "name": data["name"]})

@app.route("/items/<id>", methods=["PUT"])
def update_item(id):
    data = request.json
    items_collection.update_one({"_id": ObjectId(id)}, {"$set": {"name": data["name"]}})
    return jsonify({"_id": id, "name": data["name"]})

@app.route("/items/<id>", methods=["DELETE"])
def delete_item(id):
    items_collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Item deleted"})

if __name__ == "__main__":
    app.run(debug=True)
