from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from pymongo import MongoClient
from bson import ObjectId


# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['JWT_SECRET_KEY'] = 'jwt_secret_key'

# Initialize JWT
jwt = JWTManager(app)

# Initialize MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['demo']
collection = db['data']

# Registration endpoint
@app.route('/register', methods=['POST'])
def register():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    password = request.json['password']

    # Check if email already exists
    if collection.find_one({'email': email}):
        return jsonify({'message': 'Email already exists'}), 400

    # Store user data in MongoDB
    user = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password
    }
    collection.insert_one(user)

    return jsonify({'message': 'Registration successful'}), 200

# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']

    # Check if user exists and password is correct
    user = collection.find_one({'email': email, 'password': password})
    if user:
        access_token = create_access_token(identity=email)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# Template endpoints
@app.route('/template', methods=['POST'])
@jwt_required()
def create_template():
    template_name = request.json['template_name']
    subject = request.json['subject']
    body = request.json['body']
    user_email = get_jwt_identity()

    # Store template data in MongoDB
    template = {
        'template_name': template_name,
        'subject': subject,
        'body': body,
        'user_email': user_email  # Associate template with the user
    }
    result = collection.insert_one(template)

    # Convert the ObjectId to a string
    template['_id'] = str(result.inserted_id)

    return jsonify({'message': 'Template created successfully', 'template': template}), 200

@app.route('/template', methods=['GET'])
@jwt_required()
def get_all_templates():
    user_email = get_jwt_identity()

    # Retrieve all templates associated with the user
    templates = list(collection.find({'user_email': user_email}))

    # Convert the ObjectId to a string for each template
    for template in templates:
        template['_id'] = str(template['_id'])

    return jsonify({'templates': templates}), 200

@app.route('/template/<template_id>', methods=['GET'])
@jwt_required()
def get_template(template_id):
    user_email = get_jwt_identity()

    # Retrieve the specific template associated with the user
    template = collection.find_one({'_id': ObjectId(template_id), 'user_email': user_email})
    if template:
        # Convert the ObjectId to a string
        template['_id'] = str(template['_id'])
        return jsonify({'template': template}), 200
    else:
        return jsonify({'message': 'Template not found'}), 404

@app.route('/template/<template_id>', methods=['PUT'])
@jwt_required()
def update_template(template_id):
    user_email = get_jwt_identity()
    template_name = request.json['template_name']
    subject = request.json['subject']
    body = request.json['body']

    # Update the specific template associated with the user
    result = collection.update_one(
        {'_id': ObjectId(template_id), 'user_email': user_email},
        {'$set': {'template_name': template_name, 'subject': subject, 'body': body}}
    )

    if result.modified_count > 0:
        return jsonify({'message': 'Template updated successfully'}), 200
    else:
        return jsonify({'message': 'Template not found'}), 404

@app.route('/template/<template_id>', methods=['DELETE'])
@jwt_required()
def delete_template(template_id):
    user_email = get_jwt_identity()

    # Delete the specific template associated with the user
    result = collection.delete_one({'_id': ObjectId(template_id), 'user_email': user_email})

    if result.deleted_count > 0:
        return jsonify({'message': 'Template deleted successfully'}), 200
    else:
        return jsonify({'message': 'Template not found'}), 404
    

    
# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
