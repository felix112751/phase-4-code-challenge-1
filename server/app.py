# #!/usr/bin/env python3

# from flask import Flask, request, jsonify
# from flask_migrate import Migrate
# from models import db, Hero, Power, HeroPower
# import os

# # Setup database URI
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.json.compact = False

# migrate = Migrate(app, db)
# db.init_app(app)

# @app.route('/')
# def index():
#     return '<h1>Code Challenge</h1>'

# # GET /heroes
# @app.route('/heroes', methods=['GET'])
# def get_heroes():
#     try:
#         heroes = Hero.query.all()
#         return jsonify([hero.to_dict() for hero in heroes]), 200
#     except Exception as e:
#         print(f"Error retrieving heroes: {e}")
#         return jsonify({"error": "Failed to retrieve heroes"}), 500


# # GET /heroes/<id>
# @app.route('/heroes/<int:id>', methods=['GET'])
# def get_hero(id):
#     hero = Hero.query.get(id)
#     if hero:
#         return jsonify(hero.to_dict()), 200
#     return jsonify({"error": "Hero not found"}), 404

# # GET /powers
# @app.route('/powers', methods=['GET'])
# def get_powers():
#     powers = Power.query.all()
#     return jsonify([power.to_dict() for power in powers]), 200

# # GET /powers/<id>
# @app.route('/powers/<int:id>', methods=['GET'])
# def get_power(id):
#     power = Power.query.get(id)
#     if power:
#         return jsonify(power.to_dict()), 200
#     return jsonify({"error": "Power not found"}), 404

# # PATCH /powers/<id>
# @app.route('/powers/<int:id>', methods=['PATCH'])
# def update_power(id):
#     power = Power.query.get(id)
#     if not power:
#         return jsonify({"error": "Power not found"}), 404

#     data = request.get_json()
#     if 'description' in data:
#         if not isinstance(data['description'], str) or len(data['description']) < 20:
#             return jsonify({"errors": ["Description must be at least 20 characters long."]}), 400
#         power.description = data['description']
#         db.session.commit()
#         return jsonify(power.to_dict()), 200
#     return jsonify({"error": "No fields provided for update"}), 400

# # POST /hero_powers
# @app.route('/hero_powers', methods=['POST'])
# def create_hero_power():
#     data = request.get_json()
#     required_fields = ['strength', 'hero_id', 'power_id']

#     # Check for missing fields
#     for field in required_fields:
#         if field not in data:
#             return jsonify({"errors": [f"Missing field: {field}"]}), 400

#     # Validate strength
#     valid_strengths = ['Strong', 'Weak', 'Average']
#     if data['strength'] not in valid_strengths:
#         return jsonify({"errors": ["Strength must be one of 'Strong', 'Weak', or 'Average'."]}), 400

#     # Create HeroPower instance
#     new_hero_power = HeroPower(
#         strength=data['strength'],
#         hero_id=data['hero_id'],
#         power_id=data['power_id']
#     )
    
#     db.session.add(new_hero_power)
#     db.session.commit()
#     return jsonify(new_hero_power.to_dict()), 201

# if __name__ == '__main__':
#     app.run(port=5002, debug=True)
