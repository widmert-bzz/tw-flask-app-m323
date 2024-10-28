from flask import Blueprint, jsonify, request, render_template
from flask_login import login_required, current_user
from birthdays_dao import BirthdaysDao
from birthday import Birthday

birthdays_blueprint = Blueprint('todo_blueprint', __name__)
birthdays_dao = BirthdaysDao('todo_example.db')


@birthdays_blueprint.route('/todos', methods=['GET'])
@login_required
def get_all_todos():
    items = birthdays_dao.get_all_items(current_user.id)
    return render_template('index.html', todos=items)


@birthdays_blueprint.route('/todos/<int:item_id>', methods=['GET'])
@login_required
def get_todo(item_id):
    item = birthdays_dao.get_item(item_id, current_user.id)
    if item:
        return jsonify(item.__dict__), 200
    else:
        return jsonify({"message": "Item not found"}), 404


@birthdays_blueprint.route('/todos', methods=['POST'])
@login_required
def add_todo():
    name = request.form['name']
    date = request.form['date']
    new_item = Birthday(None, current_user.id, name, date)
    birthdays_dao.add_item(new_item)
    return jsonify({"message": "Todo item created"}), 201


@birthdays_blueprint.route('/todos/<int:item_id>', methods=['PUT'])
@login_required
def update_todo(item_id):
    data = request.get_json()
    updated_item = Birthday(item_id, data['title'], data['is_completed'], current_user.id)
    if birthdays_dao.update_item(updated_item):
        return jsonify({"message": "Item updated"}), 200
    else:
        return jsonify({"message": "Item not found or not updated"}), 404


@birthdays_blueprint.route('/todos/<int:item_id>', methods=['DELETE'])
@login_required
def delete_todo(item_id):
    if birthdays_dao.delete_item(item_id, current_user.id):
        return jsonify({"message": "Item deleted"}), 200
    else:
        return jsonify({"message": "Item not found or not deleted"}), 404
