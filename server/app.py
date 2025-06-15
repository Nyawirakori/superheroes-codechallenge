from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from models import db,Hero,Power,Hero_power

app = Flask(__name__)

#Our connection to the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'

#Prevents SQLAlchemy from trackking all modifications in order to use less memory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app,db)

db.init_app(app)

#Getting all heroes
@app.route('/heroes', methods=["GET"])
def get_heroes():
    heroes = []

    for hero in Hero.query.all():
        heroes.append(hero.to_dict(only=("id", "name", "super_name")))

    return make_response(heroes, 200)

#Getting all powers
@app.route('/powers', methods=["GET"])
def get_powers():
    powers = []

    for power in Power.query.all():
        powers.append(power.to_dict(only=("id", "name", "description")))

    return make_response(powers, 200)

#Getting heroes by id
@app.route('/heroes/<int:id>', methods=["GET"])
def get_hero_by_id(id):
    hero = Hero.query.get(id)

    if hero:
        return make_response(hero.to_dict(rules=('hero_powers', 'hero_powers.power')), 200)
    else:
        return make_response({"error": "Hero not found"}, 404)


#Getting powers by id
@app.route('/powers/<int:id>', methods=["GET"])
def get_power_by_id(id):
    power = Power.query.get(id)
    if power:
        return make_response(power.to_dict(only=("id", "name", "description")), 200)
    else:
        return make_response({"error": "Power not found"}, 404)


#PATCH Request on power
@app.route('/powers/<int:id>', methods=["PATCH"])
def update_power(id):
    power = Power.query.get(id)

    if not power:
        return make_response({"error": "Power not found"}, 404)

    data = request.get_json()

    try:
        if "description" in data:
            power.description = data["description"]  

        db.session.commit()

        return make_response(
            power.to_dict(only=("id", "name", "description")), 200
        )

    except Exception as e:
        return make_response({"errors": [str(e)]}, 400)


# Create HeroPower(POST Request)
@app.route('/hero_powers', methods=["POST"])
def create_hero_power():
    data = request.get_json()
    try:
        hero_power = Hero_power(
            strength=data["strength"],
            hero_id=data["hero_id"],
            power_id=data["power_id"]
        )
        db.session.add(hero_power)
        db.session.commit()
        return make_response(hero_power.to_dict(rules=('hero', 'power')), 201)
    except Exception as e:
        return make_response({"errors": [str(e)]}, 400)


if __name__ == '__main__':
    app.run(port=5555, debug = True)
