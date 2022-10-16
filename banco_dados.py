import mysql.connector
from mysql.connector import errorcode

print("Conectando...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='admin'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `agenda_cliente`;")

cursor.execute("CREATE DATABASE `agenda_cliente`;")

cursor.execute("USE `agenda_cliente`;")


TABLES = {}
TABLES['Pacientes'] = ('''
      CREATE TABLE `pacientes` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) NOT NULL,
      `especialidade` varchar(30) NOT NULL,
      `horario` varchar(10) NOT NULL,
      `telefone` varchar(20) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Usuarios'] = ('''
      CREATE TABLE `usuarios` (
      `nome` varchar(20) NOT NULL,
      `nickname` varchar(8) NOT NULL,
      `senha` varchar(100) NOT NULL,
      PRIMARY KEY (`nickname`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')

usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)'
usuarios = [
      ("Jorge Lago", "lagojorge", "senha123"),
      ("Bruna Surama", "Susu", "321senha"),
      ("Eloah Lago", "elolago", "princesa123")
]
cursor.executemany(usuario_sql, usuarios)

cursor.execute('select * from agenda_cliente.usuarios')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])


pacientes_sql = 'INSERT INTO pacientes (nome, especialidade, horario, telefone) VALUES (%s, %s, %s)'
pacientes = [
      ('Roberta Silva', 'Dentista', '09:30', '9833044554'),
      ('Cláudia Mendes', 'Ortopedista', '10:20', '9890094334'),
]
cursor.executemany(pacientes_sql, pacientes)

cursor.execute('select * from agenda_cliente.pacientes')
print(' -------------  Pacientes:  -------------')
for pacientes in cursor.fetchall():
    print(pacientes[1])

conn.commit()

cursor.close()
conn.close()