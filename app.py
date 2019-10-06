from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    """Return homepage."""
    return render_template('home.html', msg='Flask is Cool!!')


# mock items - delete later ₽
items = [
    {'title': 'Pokeball',
        'description': 'A standard pokeball with a 50% success rate!', 'price': '200'},
    {'title': 'Great Ball',
        'description': 'An upgraded pokeball with a 65% success rate!', 'price': '400'},
    {'title': 'Ultra Ball',
        'description': 'The highest grade of pokeball with a 80% success rate!', 'price': '800'}
]


@app.route('/items')
def items_index():
    """Display all itms"""
    return render_template("items_index.html", items=items)


if __name__ == '__main__':
    app.run(debug=True)
