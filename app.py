from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

client = MongoClient()
db = client.Pokemart
items = db.items

app = Flask(__name__)


# @app.route('/')
# def index():
#     """Return homepage."""
#     return render_template('home.html', msg='Flask is Cool!!')


# mock items - delete later ₽
# items = [
#     {'title': 'Pokeball',
#         'description': 'A standard pokeball with a 50% success rate!', 'price': '200'},
#     {'title': 'Great Ball',
#         'description': 'An upgraded pokeball with a 65% success rate!', 'price': '400'},
#     {'title': 'Ultra Ball',
#         'description': 'The highest grade of pokeball with a 80% success rate!', 'price': '800'}
# ]


@app.route('/')
def items_index():
    """Display all itms"""
    return render_template("items_index.html", items=items.find())


@app.route('/items', methods=['POST'])
def items_submit():
    """Submit a new item."""
    item = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'price': request.form.get('price'),
        'ratings': request.form.get('ratings')
    }
    item_id = items.insert_one(item).inserted_id
    return redirect(url_for('items_show', item_id=item_id))


@app.route('/items/new')
def items_new():
    """Add new Item
    TODO: Lock this behind amin login after flask login set up """
    return render_template('items_new.html', item={}, title="New Item")


@app.route('/items/<item_id>')
def items_show(item_id):
    """Show an individual item."""
    item = item.find_one({'_id': ObjectId(item_id)})
    return render_template('items_show.html', item=item)


if __name__ == '__main__':
    app.run(debug=True)
