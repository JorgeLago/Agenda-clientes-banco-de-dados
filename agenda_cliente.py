from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'consultorio'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}: //{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = 'admin',
        servidor = 'localhost',
        database = 'agenda_cliente'
    )

db = SQLAlchemy(app)

class Pacientes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    especialidade = db.Column(db.String(30), nullable=False)
    horario = db.Column(db.String(10), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

class Usuarios(db.Model):
    nickname = db.Column(db.String(8), primary_key=True, autoincrement=True)
    nome = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

@app.route('/')
def index():
    lista = Pacientes.query.order_by(Pacientes.id)
    return render_template('lista.html', titulo='Paciente', paciente=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Paciente')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    especialidade = request.form['especialidade']
    horario = request.form['horario']
    telefone = request.form['telefone']
   
    paciente = Pacientes.query.filter_by(nome=nome).first()

    if paciente:
        flash("Paciente já tem agendamento!")
        return redirect(url_for('index'))
    
    novo_paciente = Pacientes(nome=nome, especialidade=especialidade, horario=horario, telefone=telefone)
    db.session.add(novo_paciente)
    db.session.commit()
   
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

app.run(debug=True)