from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Contractor')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
items = db.items

app = Flask(__name__)


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
    item = items.find_one({'_id': ObjectId(item_id)})
    return render_template('items_show.html', item=item)


@app.route('/items/<item_id>/edit')
def items_edit(item_id):
    """Display edit form"""
    item = items.find_one({'_id': ObjectId(item_id)})
    return render_template('items_edit.html', item=item, title='Edit item')


@app.route('/items/<item_id>', methods=['POST'])
def items_update(item_id):
    """Submit edited item"""
    updated_item = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'price': request.form.get('price'),
        'ratings': request.form.get('ratings')
    }
    items.update_one(
        {'_id': ObjectId(item_id)},
        {'$set': updated_item})
    return redirect(url_for('items_show', item_id=item_id))


@app.route('/items/<item_id>/delete', methods=['POST'])
def items_delete(item_id):
    """Delete single item."""
    items.delete_one({'_id': ObjectId(item_id)})
    return redirect(url_for('items_index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
