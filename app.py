from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI']='mongodb+srv://santiago_herrera:1234@cluster0.5l0k3.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
mongo = PyMongo(app)

CORS(app)

db = mongo.db.users

@app.route('/users', methods=['POST'])
def create_user():
    id = db.insert({
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password']
    })
    return jsonify(str(ObjectId(id)))


@app.route('/users', methods=['GET'])
def get_users():
    users = []
    for doc in db.find():
        users.append({
            '_id': str(ObjectId(doc['_id'])),
            'name': doc['name'],
            'email': doc['email'],
            'password': doc['password']
        })
    return jsonify(users)


@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = db.find_one({'_id': ObjectId(id)})
    return jsonify({
            '_id': str(ObjectId(user['_id'])),
            'name': user['name'],
            'email': user['email'],
            'password': user['password']
        })


@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    db.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg': 'user deleted'})

@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    db.update_one({'_id': ObjectId(id)},{'$set':{
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password']
    }}
    )
    return jsonify({'msg': 'user updated'})

@app.route('/')
def index():
    return '<h1> HELLO WORLD </H1>'

if __name__ == '__main__':
    app.run(port=5000)
    