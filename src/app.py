"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")

john = {
    "first_name": "John",
    "last_name": jackson_family.last_name,
    "age": 33,
    "lucky_numbers": [7, 13, 22],
}

jane = {
    "first_name": "Jane",
    "last_name": jackson_family.last_name,
    "age": 35,
    "lucky_numbers": [10, 14, 3],
}

jimmy = {
    "first_name": "Jimmy",
    "last_name": jackson_family.last_name,
    "age": 5,
    "lucky_numbers": [1],
}

jackson_family.add_member(john)
jackson_family.add_member(jane)
jackson_family.add_member(jimmy)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_get_all():
    family_members = jackson_family.get_all_members()
    return jsonify(family_members), 200

@app.route('/member/<int:id>', methods=['GET'])
def handle_get_one(id):
    family_member = jackson_family.get_member(id)
    return jsonify(family_member), 200

@app.route('/member', methods=['POST'])
def handle_add_new():
    family_member = request.json
    jackson_family.add_member(family_member)
    if family_member is not None:
        return jsonify({"Message": f"Success! New family member {family_member} added."}), 200
    else:
        return jsonify({"Error": "Hmmm... looks like that family member already exists."}), 404

@app.route('/member/<int:id>', methods=['DELETE'])
def handle_delete(id):
    family_member = jackson_family.get_member(id)
 
    if family_member:
        jackson_family.delete_member(id)
        return jsonify({"Message": f"Success! Memeber {family_member} deleted.", "done": True}), 200
    else:
        return jsonify({"Error": "Delete Failed. No family member found with the provided ID.", "done": True}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)