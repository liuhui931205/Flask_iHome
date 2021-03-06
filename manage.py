# coding=utf-8
from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate
from iHome import create_app,db
from iHome import models

app = create_app('development')

manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    # app.run()
    print app.url_map
    manager.run()
