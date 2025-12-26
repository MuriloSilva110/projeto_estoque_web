from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email , EqualTo, ValidationError

class CategoriaForm(FlaskForm):
    nome = StringField('Nome da Categoria', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Criar Categoria')

class FornecedorForm(FlaskForm):
    nome = StringField('Nome do Fornecedor', validators=[DataRequired()])
    telefone = StringField('Telefone', validators=[DataRequired()])
    submit = SubmitField('Salvar Fornecedor')
    
class produtoForm(FlaskForm):
    nome = StringField('Nome do Produto', validators=[DataRequired(), Length(min=2, max=100)])
    preco = FloatField('Preço do Produto', validators=[DataRequired()])
    codigo_interno = StringField('Código Interno', validators=[DataRequired(), Length(min=1, max=50)])
    fornecedor_id = SelectField('Fornecedor', coerce=int, validators=[DataRequired()])
    categoria_id = SelectField('Categoria', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Criar Produto')

class CadastroForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirm_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])
    submit = SubmitField('Cadastrar')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    lembrar = BooleanField('Lembrar de mim')
    submit = SubmitField('Login')