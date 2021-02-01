from flask import Blueprint, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
from decorator import token_required
import firebase_admin
example_blueprint = Blueprint('example_blueprint', __name__)


cred = credentials.ApplicationDefault()
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
    'projectId': 'springmltraining',
    })

db = firestore.client()
table_ref = db.collection('tennis_players')


@example_blueprint.route('/')
def index():
    return "This is API APPSSSS"

@example_blueprint.route('/add', methods=['POST'])
@token_required
def create():
    
    try:
        if request.is_json:
            id = request.json.get('id', None)
            if id:
                if table_ref.document(str(id)).get().exists:
                    return  jsonify({"failure":"Document with same ID already exists"}), 400
                table_ref.document(str(id)).set(request.json)
                return jsonify({"success": True}), 200
            else:
                return jsonify({"failure":"No Id received in JSON"}), 400
        else:
            return jsonify({"failure":"No JSON Received"}), 400

    except Exception as e:
        return f"An Error Occured: {e}"

@example_blueprint.route('/update', methods=['PUT'])
@token_required
def update():
    
    try:
        if request.is_json:
            id = request.json.get('id',None)
            if id:
                if table_ref.document(str(id)).get().exists:
                    table_ref.document(str(id)).update(request.json)
                    return jsonify({"success": True}), 200
                else:
                    return  jsonify({"failure":"Document with the given ID does not exists"}), 400
            else:
                return jsonify({"failure":"No Id received in JSON"}), 400
        else:
            return jsonify({"failure":"No JSON Received"}), 400
    except Exception as e:
        return f"An Error Occured: {e}"

@example_blueprint.route('/list', methods=['GET'])
@token_required
def read():
    try:
        if request.is_json:
            id = request.json.get('id', None) 
            if id:
                todo = table_ref.document(str(id)).get()
                print(todo.to_dict())
                return jsonify(todo.to_dict()), 200

        all_todos = [doc.to_dict() for doc in table_ref.stream()]
        return jsonify(all_todos), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@example_blueprint.route('/delete', methods=['DELETE'])
@token_required
def delete():
    
    try:
        if request.is_json:
            id = request.json.get('id',None) 
            if id:
                if table_ref.document(str(id)).get().exists:
                    table_ref.document(str(id)).delete()
                    return jsonify({"success": True}), 200
                else:
                    return  jsonify({"failure":"Document with the given ID does not exists"}), 400
            else:
                return jsonify({"Failure":"No id in JSON"}), 400
        else:
            return jsonify({"Failure":"No JSON Received"}), 400        

    except Exception as e:
        return f"An Error Occured: {e}"

@example_blueprint.route('/filter', methods=['GET'])
@token_required
def filter():
    try:
            if request.is_json:
                filter_by = request.json.get('filter_by',None) 
                value = request.json.get('value',None) 
                if filter_by and value:
                    if filter_by in ['seeded_player']:
                        query = table_ref.where(str(filter_by), u'==',value).stream()
                        all_todos = [doc.to_dict() for doc in query]
                        return jsonify(all_todos), 200
                    else:
                        return  jsonify({"failure":"Invalid Filter"}), 400
                    
                else:
                    return jsonify({"Failure":"No Filter/value given"}), 400
            else:
                return jsonify({"Failure":"No JSON Received"}), 400        

    except Exception as e:
            return f"An Error Occured: {e}"        


