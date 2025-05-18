from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")

    if not username:
        return jsonify({"error": "Invalid data"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "User already exists"}), 409

    new_user = User(username=username)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": f"User {username} registered"}), 201


@app.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([user.username for user in users])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
