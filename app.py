"""Flask app for Cupcakes"""

from flask import Flask, render_template, flash, redirect
from sneakybeaky import SECRET_GEORGE
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = SECRET_GEORGE
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)

connect_db(app)

# GET /api/cupcakes
# Get data about all cupcakes.

@app.route('/api/cupcakes')
def list_cupcakes():
    """Get data about all cupcakes."""
    all_cupcakes = [cupcakes.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcake=all_cupcakes)


# GET /api/cupcakes/[cupcake-id]
# Get data about a single cupcake.

@app.route('/api/cupcakes/<int:id>')
def list_cupcake(id):
    """Get data about a single cupcake."""
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())


# POST /api/cupcakes
# Create a cupcake with flavor, size, rating and image data from the body of the request.

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    new_cupcake = Cupcake(
        flavor=request.json["flavor"],
        size=request.json["size"],
        rating=request.json["rating"],
        image=request.json["image"]
    )

    db.session.add(new_cupcake)
    db.session.commit()

    response_json = jsonify(cupcake=new_cupcake.serialize()) #RETURN TO THIS AND EXPLORE IT
    return (response_json, 201)