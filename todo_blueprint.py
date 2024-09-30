from flask import Blueprint, jsonify, request, render_template
from flask_login import login_required, current_user
from todo_dao import TodoDao
from todo_item import TodoItem

todo_blueprint = Blueprint('todo_blueprint', __name__)
todo_dao = TodoDao('todo_example.db')

@todo_blueprint.route('/todos', methods=['GET'])
@login_required
def get_all_todos():
    items = todo_dao.get_all_items(current_user.id)
    return render_template('index.html', todos=items)

@todo_blueprint.route('/todos/<int:item_id>', methods=['GET'])
@login_required
def get_todo(item_id):
    item = todo_dao.get_item(item_id, current_user.id)
    if item:
        return jsonify(item.__dict__), 200
    else:
        return jsonify({"message": "Item not found"}), 404

@todo_blueprint.route('/todos', methods=['GET'])
@login_required
def get_all_todos():
    items = todo_dao.get_all_items(current_user.id)
    return render_template('index.html', todos=items)

@todo_blueprint.route('/todos/<int:item_id>', methods=['PUT'])
@login_required
def update_todo(item_id):
    data = request.get_json()
    updated_item = TodoItem(item_id, data['title'], data['is_completed'], current_user.id)
    if todo_dao.update_item(updated_item):
        return jsonify({"message": "Item updated"}), 200
    else:
        return jsonify({"message": "Item not found or not updated"}), 404

@todo_blueprint.route('/todos/<int:item_id>', methods=['DELETE'])
@login_required
def delete_todo(item_id):
    if todo_dao.delete_item(item_id, current_user.id):
        return jsonify({"message": "Item deleted"}), 200
    else:
        return jsonify({"message": "Item not found or not deleted"}), 404
