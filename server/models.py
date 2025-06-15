from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData()
db = SQLAlchemy(metadata = metadata)

class Hero(db.Model,SerializerMixin):
    __tablename__ ='heroes'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    
    serialize_rules = ('-hero_powers.hero',)

    #Relationship
    hero_powers = db.relationship('Hero_power', back_populates ="hero", cascade='all,  delete-orphan')

    # Association proxy to get powers for this hero through heropowers
    powers = association_proxy('hero_powers', 'power',
                                 creator=lambda power_obj: Hero_power(power=power_obj))

class Power(db.Model,SerializerMixin):
    __tablename__ ='powers'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    serialize_rules = ('-hero_powers.power',)

    #Relationship
    hero_powers = db.relationship('Hero_power', back_populates ="power", cascade='all,  delete-orphan')

    #Validation
    @validates("description")
    def validate_description(self, key, value):
        if not value or len(value) < 20:
            raise ValueError("Description must be at least 20 characters long")
        return value

    # Association proxy to get heroes for this power through heropowers
    heroes = association_proxy('hero_powers', 'hero',
                                  creator=lambda hero_obj: Hero_power(hero=hero_obj))


class Hero_power(db.Model,SerializerMixin):
    __tablename__ ='hero_powers'
    id = db.Column(db.Integer, primary_key = True)
    strength = db.Column(db.String)
    hero_id = db.Column(db.Integer, db.ForeignKey("heroes.id"))
    power_id = db.Column(db.Integer, db.ForeignKey("powers.id"))

    serialize_rules = ('-hero.hero_powers', '-power.hero_powers',)

    #Relationships
    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')

    #Validation
    @validates('strength')
    def validate_strength(self, key, strength):
        valid_strengths = ['Strong', 'Weak', 'Average']
        if strength not in valid_strengths:
            raise ValueError("Strength must be 'Strong', 'Weak', or 'Average'")
        return strength
