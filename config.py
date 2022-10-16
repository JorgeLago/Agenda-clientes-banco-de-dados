SECRET_KEY = 'consultorio'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}: //{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'admin',
        servidor = '127.0.0.1',
        database = 'agenda_cliente'
    )