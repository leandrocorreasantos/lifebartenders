import sys
import errno
import csv
from lifebartenders import app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from models import City, State, User, user_manager


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def seed():
    # seed user
    user = User(**{
        'username': 'admin',
        'password': user_manager.hash_password('123456'),
        'email': 'admin@lifebartenders.com'}
    )
    db.session.add(user)
    db.session.commit()

    # Seed states
    states_data = [
        {'id': 1, 'name': 'Acre', 'fs': 'AC'},
        {'id': 2, 'name': 'Alagoas', 'fs': 'AL'},
        {'id': 3, 'name': 'Amapá', 'fs': 'AP'},
        {'id': 4, 'name': 'Amazonas', 'fs': 'AM'},
        {'id': 5, 'name': 'Bahia', 'fs': 'BA'},
        {'id': 6, 'name': 'Ceará', 'fs': 'CE'},
        {'id': 7, 'name': 'Distrito Federal', 'fs': 'DF'},
        {'id': 8, 'name': 'Espírito Santo', 'fs': 'ES'},
        {'id': 9, 'name': 'Goiás', 'fs': 'GO'},
        {'id': 10, 'name': 'Maranhão', 'fs': 'MA'},
        {'id': 11, 'name': 'Mato Grosso', 'fs': 'MT'},
        {'id': 12, 'name': 'Mato Grosso do Sul', 'fs': 'MS'},
        {'id': 13, 'name': 'Minas Gerais', 'fs': 'MG'},
        {'id': 14, 'name': 'Pará', 'fs': 'PA'},
        {'id': 15, 'name': 'Paraíba', 'fs': 'PB'},
        {'id': 16, 'name': 'Paraná', 'fs': 'PR'},
        {'id': 17, 'name': 'Pernambuco', 'fs': 'PE'},
        {'id': 18, 'name': 'Piauí', 'fs': 'PI'},
        {'id': 19, 'name': 'Rio de Janeiro', 'fs': 'RJ'},
        {'id': 20, 'name': 'Rio Grande do Norte', 'fs': 'RN'},
        {'id': 21, 'name': 'Rio Grande do Sul', 'fs': 'RS'},
        {'id': 22, 'name': 'Rondônia', 'fs': 'RO'},
        {'id': 23, 'name': 'Roraima', 'fs': 'RR'},
        {'id': 24, 'name': 'Santa Catarina', 'fs': 'SC'},
        {'id': 25, 'name': 'São Paulo', 'fs': 'SP'},
        {'id': 26, 'name': 'Sergipe', 'fs': 'SE'},
        {'id': 27, 'name': 'Tocantins', 'fs': 'TO'},
    ]
    for states in states_data:
        state = State(**states)
        try:
            db.session.add(state)
            db.session.commit()
        except Exception as e:
            print('Error while seed states: {}'.format(e))
    states_ids = {
        'AC': 1, 'AL': 2, 'AP': 3, 'AM': 4, 'BA': 5, 'CE': 6, 'DF': 7, 'ES': 8,
        'GO': 9, 'MA': 10, 'MT': 11, 'MS': 12, 'MG': 13, 'PA': 14, 'PB': 15,
        'PR': 16, 'PE': 17, 'PI': 18, 'RJ': 19, 'RN': 20, 'RS': 21, 'RO': 22,
        'RR': 23, 'SC': 24, 'SP': 25, 'SE': 26, 'TO': 27
    }

    # loading cities
    with open("seeds/cities.csv") as list_cities:
        city_item = csv.reader(list_cities, delimiter=',')
        for cities in city_item:
            city = City(
                id=cities[0],
                name=cities[1],
                state_id=states_ids[cities[2]]
            )
            try:
                db.session.add(city)
                db.session.commit()
            except Exception as e:
                print('Error while seed cities: {}'.format(e))


if __name__ == '__main__':
    if not app.debug:
        print('App is in production mode. Migration skipped')
        sys.exit(errno.EACCES)
    manager.run()
