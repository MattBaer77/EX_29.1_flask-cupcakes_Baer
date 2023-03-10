"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template, flash, redirect
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




@app.route('/')
def index_page():
    """Return an HTML page. This page should be entirely static (the route should just render the template, without providing any information on cupcakes in the database). It should show simply have an empty list where cupcakes should appear and a form where new cupcakes can be added."""

    return render_template('index.html')


# **********
# RESTFUL CUPCAKES JSON API
# **********

# GET /api/cupcakes
# Get data about all cupcakes.

@app.route('/api/cupcakes')
def list_cupcakes():
    """Get data about all cupcakes."""
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)


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


# PATCH /api/cupcakes/[cupcake-id]
# This should raise a 404 if the cupcake cannot be found.
# Update a cupcake with the id passed in the URL and flavor, size, rating and image data from the body of the request. You can always assume that the entire cupcake object will be passed to the backend.

@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    """Update a cupcake with the id passed in the URL and flavor, size, rating and image data from the body of the request. You can always assume that the entire cupcake object will be passed to the backend."""

    cupcake = Cupcake.query.get_or_404(id)

    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())


# DELETE /api/cupcakes/[cupcake-id]
# This should raise a 404 if the cupcake cannot be found.
# Delete cupcake with the id passed in the URL. Respond with JSON like {message: "Deleted"}.

@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    """Delete cupcake with the id passed in the URL. Respond with JSON like {message: "Deleted"}."""

    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")