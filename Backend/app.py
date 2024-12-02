from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Change to a more secure secret in production

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), nullable=False)

# Create the database
with app.app_context():
    db.create_all()

# Serve the login and registration page
@app.route('/')
def index():
    return render_template('index.html')

# Serve the dashboard page
@app.route('/dashboard')
@jwt_required()
def dashboard():
    current_user = get_jwt_identity()  # Get the current logged-in user
    user = User.query.filter_by(username=current_user).first()
    return jsonify(role=user.role)

# Register user route
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_password, role=data['role'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message="User registered successfully!"), 201

# Login route to get JWT token
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.username)
        return jsonify(access_token=access_token), 200

    return jsonify(message="Invalid username or password"), 401

# Admin can assign roles (for demonstration purposes)
@app.route('/admin/assign_role', methods=['POST'])
@jwt_required()
def assign_role():
    current_user = get_jwt_identity()  # Get the current logged-in user
    user = User.query.filter_by(username=current_user).first()

    if user.role != "Admin":
        return jsonify(message="You do not have permission to assign roles."), 403

    data = request.get_json()
    user_to_update = User.query.filter_by(username=data['username']).first()
    
    if user_to_update:
        user_to_update.role = data['role']
        db.session.commit()
        return jsonify(message=f"Role of {data['username']} updated to {data['role']}."), 200
    else:
        return jsonify(message="User not found."), 404

if __name__ == '__main__':
    app.run(debug=True, port=5001)
