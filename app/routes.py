from flask import Blueprint, render_template, request, redirect, url_for

main = Blueprint('main', __name__)

# In-memory list to store items
items = []

@main.route('/')
def index():
    return render_template('index.html', items=items)

@main.route('/add', methods=['POST'])
def add_item():
    item = request.form.get('item')
    if item:
        items.append(item)
    return redirect(url_for('main.index'))