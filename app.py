from enum import unique
from operator import attrgetter
from re import A
from threading import active_count
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cliente.db"
db = SQLAlchemy(app)


class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(14), unique=True)
    password = db.Column(db.String(14), unique=True)
    nome = db.Column(db.String(24))
    email = db.Column(db.String(18))
    idade = db.Column(db.String(3))
    ativo = db.Column(db.String(1))
    turma = db.Column(db.String(14))

    def __init__(self, username, password, nome, email, idade, ativo, turma):
        self.usernome = username
        self.password = password
        self.nome = nome
        self.email = email
        self.idade = idade
        self.ativo = ativo 
        self.turma = turma


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    verificaUsuario = Aluno.query.filter_by(username = request.form['usuario'])
    verificaSenha = Aluno.query.filter_by(password = request.form['senha'])

    id = Aluno.id

    if verificaUsuario == True and verificaSenha == True and request.method == 'POST':
        return redirect(url_for('index'))
        return render_template('paginaPrincipal.html', id=id)
    else:
        return redirect(url_for('index'))
        return render_template('index.html')

@app.route('/cadastro', methods=['GET, POST'])
def cadastro():
    if request.method == 'POST':
        usuario = Aluno(request.form['nomeUsuario'], request.form['senha'], request.form['nomeCompleto'], 
        request.form['email'], request.form['idade'], request.form['ativo'], request.form['turma'])

        db.session.add(usuario)
        db.commit()
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/paginaPrincipal/<int:id>', methods=['GET, POST'])
def paginaPrincipal(id):
    usuarios = Aluno.query.all()

    if request.method == 'GET':
        return redirect(url_for('index'))

    return render_template('paginaPrincipal.html', usuarios=usuarios)

@app.route('/editarAluno/<int:id>', methods=['GET, POST'])
def editarAluno(id):
    aluno = Aluno.query.get(id)

    if request.method == 'POST':
        aluno.nome = request.form['nome']
        aluno.turma = request.form['turma']
        aluno.idade = request.form['idade']
        aluno.ativo = request.form['ativo']

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit.html', aluno=aluno)
    
@app.route('/excluirAluno/<int:id>', methods=['GET, POST'])
def excluirAluno(id):
    aluno = Aluno.query.get(id)

    db.session.delete(aluno)
    db.session.commit()

    return redirect(url_for('index'))
    return render_template('paginaPrincipal.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)