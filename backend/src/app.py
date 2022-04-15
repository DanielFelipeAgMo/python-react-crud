from flask import Flask,request,Response,jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/python-flask-mongodb'
mongo = PyMongo(app)

CORS(app)
db = mongo.db.users

@app.route('/users', methods=['POST'])
def crearUsuario():
    id = db.insert_one({
        "name": request.json['name'],
        "email": request.json['email'],
        "password": request.json['password']
    })
    return jsonify({"id": str(id.inserted_id)})
    
    

@app.route('/users', methods=['GET'])
def consultarUsuarios():
    usuarios =[]
    for usuario in db.find():
        usuarios.append({
            "id": str(usuario['_id']),
            "name": usuario['name'],
            "email": usuario['email'],
            "password": usuario['password']
        })
    return jsonify(usuarios)

@app.route('/user/<id>', methods=['GET'])
def consultarUsuario(id):
    usuario = db.find_one({"_id": ObjectId(id)})
    return jsonify({
        "id": str(ObjectId(usuario['_id'])),
        "name": usuario['name'],
        "email": usuario['email'],
        "password": usuario['password']
    })

@app.route('/users/<id>', methods=['DELETE'])
def borrarUsuario(id):
    db.delete_one({"_id": ObjectId(id)})   
    return jsonify({"msg":" >El usuario ha sido borrado"})

@app.route('/users/<id>', methods=['PUT'])
def actualizarUsuario(id):
    db.update_one({"_id": ObjectId(id)},{
        "$set": {
            "name": request.json['name'],
            "email": request.json['email'],
            "password": request.json['password']
        }
    })
    return jsonify({"msg":" >El usuario ha sido actualizado"})

    

if __name__ == "__main__":
    app.run(debug=True)