# coding=utf-8
from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate
from iHome import create_app,db


app = create_app('development')

manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)



@app.route('/', methods=['GET', 'POST'])
def index():
    # session['name'] = 'laowang'
    # redis_store.set('name','laowang')
    return 'index'


if __name__ == '__main__':
    # app.run()
    manager.run()
