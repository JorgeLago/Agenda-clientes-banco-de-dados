from flask import render_template, request, redirect, session, flash, url_for
from agenda_cliente import app, db
from models import Pacientes, Usuarios

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

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    paciente = Pacientes.query.filter_by(id=id).first()
    return render_template('editar.html', titulo='Editando Agendamento', paciente=paciente)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    paciente = Pacientes.query.filter_by(id=request.form['id']).first()
    paciente.nome = request.form['nome']
    paciente.especialidade = request.form['especialidade']
    paciente.horario = request.form['horario']
    paciente.telefone = request.form['telefone']

    db.session.add(paciente)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    Pacientes.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Agendamento deletado com sucesso!')

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