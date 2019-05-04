from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from sqlalchemy.dialects.postgresql import HSTORE
from sqlalchemy.ext.mutable import MutableDict

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
 
db = SQLAlchemy(app)
ma = Marshmallow(app)

#create a fields in database
class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    sprite = db.Column(db.String(150))
    #cardColours = db.Column(db.String(120))
    cardColours=db.Column(MutableDict.as_mutable(HSTORE))

    def __init__(self, name, sprite, cardColours):
        self.name=name
        self.sprite=sprite
        self.cardColours=cardColours

#Pokemon Schema
class PokemonSchema(ma.Schema):
    class Meta:
        # Fields to display
        fields=('id','name','sprite','cardColours')

#Init Schema
Pokemon_Schema=PokemonSchema()

#create a new Pokemon
@app.route("/api/pokemon/", methods=["POST"])
def create_Pokemon():
    pokemon=request.json['pokemon']

    name=pokemon['name']
    sprite=pokemon['sprite']
    cardColours=pokemon['cardColours']
    new_pokemon = Pokemon(name, sprite, cardColours)    

    db.session.add(new_pokemon)
    db.session.commit()
   
    return Pokemon_Schema.jsonify({"pokemon":new_pokemon})
    #return Pokemon_Schema.jsonify(new_pokemon)
 
#Run server 
if __name__=='__main__':
    db.create_all()
    app.run(debug=True,port=8006)
