from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/gradebook"  # Update with your MongoDB URI
mongo = PyMongo(app)

@app.route("/results", methods=["GET"])
def get_results():
    results = list(mongo.db.gradebook.find({}, {"_id": 0}))
    return jsonify({"results": results})

@app.route("/results", methods=["POST"])
def add_result():
    data = request.json
    mongo.db.gradebook.insert_one(data)
    return jsonify({"message": "Result added successfully"})

@app.route("/results/<roll_no>", methods=["PUT"])
def update_result(roll_no):
    data = request.json
    mongo.db.gradebook.update_one({"roll_no": roll_no}, {"$set": data})
    return jsonify({"message": "Result updated successfully"})

@app.route("/results/<roll_no>", methods=["DELETE"])
def delete_result(roll_no):
    mongo.db.gradebook.delete_one({"roll_no": roll_no})
    return jsonify({"message": "Result deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True)
