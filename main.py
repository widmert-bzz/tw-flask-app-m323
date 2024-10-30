from datetime import datetime

from flask import Flask
from flask_login import LoginManager

from birthdays_blueprint import birthdays_blueprint
from user_blueprint import user_blueprint

app = Flask(__name__)
app.secret_key = 'supersecretkey'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    from user_dao import UserDao
    user_dao = UserDao('todo_example.db')
    return user_dao.get_user_by_id(int(user_id))


app.register_blueprint(birthdays_blueprint)
app.register_blueprint(user_blueprint)


def generate_testdata():
    from birthday import Birthday
    from user import User
    from birthdays_dao import BirthdaysDao
    from user_dao import UserDao

    todo_dao = BirthdaysDao('todo_example.db')
    user_dao = UserDao('todo_example.db')

    # Generate user
    user_dao.create_user_table()
    user_dao.add_user(User(1, 'admin', 'admin@example', 'admin'))
    user_dao.add_user(User(2, 'user', 'user@example', 'user'))

    # Generate
    todo_dao.create_table()
    todo_dao.add_item(Birthday(1, 1, "Anna", datetime(2006, 1, 1)))
    todo_dao.add_item(Birthday(2, 1, "Marius", datetime(2005, 1, 12)))
    todo_dao.add_item(Birthday(3, 1, "Fridolin", datetime(2001, 1, 1)))
    todo_dao.add_item(Birthday(4, 1, "Mathilda", datetime(2002, 12, 1)))

    todo_dao.close()
    user_dao.close()


if __name__ == '__main__':
    generate_testdata()
    app.run(debug=True)
