from flask import Flask, render_template, request , redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from forms import CategoriaForm, produtoForm, FornecedorForm, CadastroForm, LoginForm
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# cria a instância do Flask
app = Flask(__name__)

# Configura o banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
if not app.config['SECRET_KEY']:
    raise ValueError("A chave SECRET_KEY não está definida. Por favor, defina-a no arquivo .env")

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f"Usuario('{self.username} - {self.email}')"

class Fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    produtos = db.relationship('Produto', backref='fornecedor', lazy=True)

    def __repr__(self):
        return f"Fornecedor('{self.nome}', '{self.telefone}')"
    
class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    produtos = db.relationship('Produto' , backref='categoria', lazy=True)

    def __repr__(self):
        return f"Categoria('{self.nome}')"
    
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    codigo_interno = db.Column(db.String(50), nullable=False)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)

    def __repr__(self):
        return f"Produto('{self.nome}', '{self.preco}', '{self.codigo_interno}')"
# Rota Home
@app.route('/')
def home():
    produtos = Produto.query.all()
    fornecedores = Fornecedor.query.all()
    categorias = Categoria.query.all()

    total_produtos = len(produtos)
    total_fornecedores = len(fornecedores)
    total_categorias = len(categorias)

    valor_total_estoque = sum(produto.preco for produto in produtos)
    return render_template('home.html', total_produtos=total_produtos, total_fornecedores=total_fornecedores,
                           total_categorias=total_categorias, valor_total_estoque=valor_total_estoque)
# Rota que lista todas as categorias disponíveis
@app.route('/categorias')
def listar_categorias():
    categorias = Categoria.query.all()
    return render_template('lista_categorias.html', categorias=categorias)

# Rota para criar uma nova categoria
@app.route('/categoria/criar/', methods=['GET', 'POST'])
@login_required
def criar_categoria():
    form = CategoriaForm()
    if form.validate_on_submit():
        nome = form.nome.data
        nova_categoria = Categoria(nome=nome)
        db.session.add(nova_categoria)
        db.session.commit()
        return redirect(url_for('listar_categorias'))
    return render_template('nova_categoria.html', form=form)

#Rota para atualizar uma categoria
@app.route('/categoria/atualizar/<int:categoria_id>/', methods=['GET', 'POST'])
@login_required
def atualizar_categoria(categoria_id):
    categoria = Categoria.query.get_or_404(categoria_id)
    form = CategoriaForm(obj=categoria)
    if form.validate_on_submit():
        categoria.nome = form.nome.data
        db.session.commit()
        flash("Categoria atualizada com sucesso.", "success")
        return redirect(url_for('listar_categorias'))

    return render_template('atualizar_categoria.html', form=form, categoria=categoria)


# Rota para deletar uma categoria
@app.route('/categoria/deletar/<int:categoria_id>/')
@login_required
def deletar_categoria(categoria_id):
    categoria = Categoria.query.get_or_404(categoria_id)
    if len(categoria.produtos) > 0:
        flash("Não é possível deletar uma categoria que possui produtos associados.", "error")
        return redirect(url_for('listar_categorias'))
    db.session.delete(categoria)
    db.session.commit()
    flash("Categoria deletada com sucesso.", "success")
    return redirect(url_for('listar_categorias'))

# Rota que lista todos os fornecedores disponíveis
@app.route('/fornecedores')
def listar_fornecedores():
    fornecedores = Fornecedor.query.all()
    return render_template('lista_fornecedores.html', fornecedores=fornecedores)

# Rota para criar um novo fornecedor
@app.route('/fornecedor/criar/', methods=['GET', 'POST'])
@login_required
def criar_fornecedor():
    form = FornecedorForm()
    if form.validate_on_submit():
        nome = form.nome.data
        telefone = form.telefone.data
        novo_fornecedor = Fornecedor(nome=nome, telefone=telefone)
        db.session.add(novo_fornecedor)
        db.session.commit()
        return redirect(url_for('listar_fornecedores'))
    return render_template('novo_fornecedor.html', form=form)

#Rota para atualizar um fornecedor
@app.route('/fornecedor/atualizar/<int:fornecedor_id>/', methods=['GET', 'POST'])
@login_required
def atualizar_fornecedor(fornecedor_id):    
    fornecedor = Fornecedor.query.get_or_404(fornecedor_id)
    form = FornecedorForm(obj=fornecedor)
    if form.validate_on_submit():
        fornecedor.nome = form.nome.data
        fornecedor.telefone = form.telefone.data
        db.session.commit()
        flash("Fornecedor atualizado com sucesso.", "success")
        return redirect(url_for('listar_fornecedores'))

    return render_template('atualizar_fornecedor.html', form=form, fornecedor=fornecedor)

# Rota para deletar um fornecedor
@app.route('/fornecedor/deletar/<int:fornecedor_id>/')
@login_required
def deletar_fornecedor(fornecedor_id):
    fornecedor = Fornecedor.query.get_or_404(fornecedor_id)
    if len(fornecedor.produtos) > 0:
        flash("Não é possível deletar um fornecedor que possui produtos associados.", "error")
        return redirect(url_for('listar_fornecedores'))
    db.session.delete(fornecedor)
    db.session.commit()
    flash("Fornecedor deletado com sucesso.", "success")
    return redirect(url_for('listar_fornecedores'))

# Rota que lista todos os produtos disponíveis
@app.route('/produtos')
def listar_produtos():
    termo = request.args.get('q')
    categoria_id = request.args.get('cat')
    fornecedor_id = request.args.get('forn')

    query = Produto.query

    if termo: 
        query = query.filter(Produto.nome.ilike(f'%{termo}%'))
    if categoria_id and categoria_id != '':
        query = query.filter_by(categoria_id=int(categoria_id))
    if fornecedor_id and fornecedor_id != '':
        query = query.filter_by(fornecedor_id=int(fornecedor_id))

    produtos = query.all()
    categorias = Categoria.query.all()
    fornecedores = Fornecedor.query.all()

    return render_template('lista_produtos.html', produtos=produtos, categorias=categorias, fornecedores=fornecedores)

# Rota que exibi os detalhes de um produto
@app.route('/produto/<int:produto_id>/')
def detalhes_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    return render_template('detalhes_produto.html', produto=produto)

# Rota para criar um novo produto
@app.route('/produto/criar/', methods=['GET', 'POST'])
@login_required
def criar_produto():
    form = produtoForm()
    form.fornecedor_id.choices = [(f.id, f.nome) for f in Fornecedor.query.all()]
    form.categoria_id.choices = [(c.id, c.nome) for c in Categoria.query.all()]
    if form.validate_on_submit():
        nome = form.nome.data
        preco = form.preco.data
        codigo_interno = form.codigo_interno.data
        fornecedor_id = form.fornecedor_id.data
        categoria_id = form.categoria_id.data

        novo_produto = Produto(nome=nome, preco=preco, codigo_interno=codigo_interno,
                               fornecedor_id=fornecedor_id, categoria_id=categoria_id)
        db.session.add(novo_produto)
        db.session.commit()
        return redirect(url_for('listar_produtos'))

    return render_template('novo_produto.html', form=form)

#Rota para deletar um produto
@app.route('/produto/deletar/<int:produto_id>/')
@login_required
def deletar_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for('listar_produtos'))

# Rota para atualizar um produto
@app.route('/produto/atualizar/<int:produto_id>/', methods=['GET', 'POST'])
@login_required
def atualizar_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    form = produtoForm(obj=produto)
    form.fornecedor_id.choices = [(f.id, f.nome) for f in Fornecedor.query.all()]
    form.categoria_id.choices = [(c.id, c.nome) for c in Categoria.query.all()]
    if form.validate_on_submit():
        produto.nome = form.nome.data
        produto.preco = form.preco.data
        produto.codigo_interno = form.codigo_interno.data
        produto.fornecedor_id = form.fornecedor_id.data
        produto.categoria_id = form.categoria_id.data
        db.session.commit()
        flash("Produto atualizado com sucesso.", "success")
        return redirect(url_for('listar_produtos'))
    
    if request.method == 'GET':
        form.fornecedor_id.data = produto.fornecedor_id
        form.categoria_id.data = produto.categoria_id


    return render_template('atualizar_produto.html', form=form, produto=produto)

# rOTA DE CADASTRO
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = CadastroForm()
    if form.validate_on_submit():
        senha_criptografada = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
        usuario = Usuario(username=form.username.data, email=form.email.data, password=senha_criptografada)
        db.session.add(usuario)
        db.session.commit()
        flash('Sua conta foi criada! Você já pode fazer login.', 'success')
        return redirect(url_for('login'))
    return render_template('cadastro.html', form=form, title='Cadastro')

# ROTA DE LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.password, form.senha.data):
            login_user(usuario, remember=form.lembrar.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login não realizado. Verifique email e senha.', 'error')
    return render_template('login.html', form=form, title='Login')

# ROTA DE LOGOUT
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
# Inicializa o app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)