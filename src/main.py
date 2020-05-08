"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, Family
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = "development"
app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "hello": "world"
    }

    return jsonify(response_body), 200

@app.route('/members', methods=['GET'])
def getFamily():
    family = Family("Doe")
    familyMembers = family.get_all_members()
    luckyNumbers = []
    for member in familyMembers:
        luckyNumbers = luckyNumbers + member['lucky_numbers']
    response_body = {
        "family_name": family.last_name,
        "members": familyMembers,
        "lucky_numbers": luckyNumbers,
        "sum_of_lucky": sum(luckyNumbers)
    }
    return jsonify(response_body), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def getMember(member_id = None):
    family = Family('Doe')
    member_id = request.view_args['member_id']
    member = family.get_member(member_id)
    return jsonify(member)

@app.route('/member', methods=['POST'])
def newMember():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    family = Family('Doe')
    name = request.json.get('name', None)
    if not name:
        return({"msg": "Missing name parameter"})
    age = request.json.get('age', None)
    if not age: 
        return({"msg": "Missing age parameter"})
    lucky_numbers = request.json.get('lucky_numbers', None)
    if not lucky_numbers:
        return({"msg": "Missing lucky numbers"})
    new_member = {
        "id": family._generateId(),
        "first_name": name,
        "age": age,
        "lucky_numbers": lucky_numbers
    }
    family.add_member(new_member)
    return jsonify(family.get_all_members())

@app.route('/member/<int:member_id>', methods=['DELETE'])
def deleteMember(member_id = None):
    family = Family('Doe')
    member_id = request.view_args['member_id']
    family.delete_member(member_id)
    return jsonify(family.get_all_members())


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
