from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

# DB Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///personal_shopper.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    categories = db.Column(db.String(255))
    favorite_colors = db.Column(db.String(255))
    price_preference = db.Column(db.String(50))
    shopping_for_others = db.Column(db.Boolean, default=False)
    wishlist_auto_update = db.Column(db.Boolean, default=False)

# Create the database and the table
with app.app_context():
    db.create_all()

@app.route('/start', methods=['POST'])
def start_conversation():
    data = request.json
    user_id = data/get('user_id')

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"message": "Hi, I'm Rayne, your personal shopper bot. I can help you quickly find items that match your personal interests and style. May I ask how you would like me to address you?"})

    return jsonify({"message": "Welcome back, {user.name}! Let's find some products for you."})

@app.route('/set_user_info', methods=[POST])
def set_user_info():
    data = request.json
    user_id = data.get('user_id')
    name = data.get('name')

    user = User.query.filter_by(id=user_id).first()
    if not user:
        user = User(name=name)
        db.session.add(user)
    else:
        user.name = name

    db.session.commit()

    return jsonify({"message": f"Nice to meet you, {name}! Let's start with a few questions to help me tailor a curated list of products to show you."})

@app.route('/set_preferences', methods=[POST])
def set_preferences():
    data = request.jsonuser_id = data.get('user_id')
    user_id = data.get('user_id')
    categories = json.dumps(data.get('categories'))
    favorite_colors = json.dumps(data.get('favorite_colors'))
    price_preference = data.get('price_preference')
    shopping_for_others = data.get('shopping_for_others')
    wishlist_auto_update = data.get('wishlist_auto_update')

    user = User.query.get(user_id)
    user.categories = categories
    user.favorite_colors = favorite_colors
    user.price_preference = price_preference
    user.shopping_for_others = shopping_for_others
    user.wishlist_auto_update = wishlist_auto_update

    db.session.commit()

    return jsonify({"message": "Great, let's get started!"})

@app.route('/recommend/<int:user_id>', methods=['GET'])
def recommend(user_id):
    user = User.query.get(user_id)
    # Here you would connect to your product recommendation logic
    # This is a mock response

    recommendations = [
        {"product_id": 1, "name": "Stylish Handbag", "price": 25},
        {"product_id": 2, "name": "Elegant Bracelet", "price": 75},
        {"product_id": 3, "name": "Colorful Skirt", "price": 50}
    ]

    return jsonify(recommendations)

if __name__ == '__min__':
    app.run(debug=True)

    