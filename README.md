📦 Gerenciador de Estoque Web - Backend Focus
<div align="center"> <img src="https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white" alt="Python"> <img src="https://img.shields.io/badge/Flask-2.0+-000000?logo=flask&logoColor=white" alt="Flask"> <img src="https://img.shields.io/badge/SQLAlchemy-ORM-red?logo=sqlalchemy&logoColor=white" alt="SQLAlchemy"> <img src="https://img.shields.io/badge/PostgreSQL-Managed-4479A1?logo=postgresql&logoColor=white" alt="PostgreSQL"> <img src="https://img.shields.io/badge/Render-Cloud_Deploy-46E3B7?logo=render&logoColor=white" alt="Render"> </div>

Foco do Projeto: Esta aplicação foi desenvolvida para demonstrar competências sólidas em Desenvolvimento Backend, incluindo modelagem de dados relacionais, segurança de rotas e integração com serviços de nuvem.

📺 Demonstração
<div align="center"> <img src="https://github.com/user-attachments/assets/33f1cab2-2e4c-4b63-b1cd-2a04c1f6c858" alt="GIF de Demonstração" width="850px"> <p><i>Interface integrada ao banco de dados PostgreSQL com persistência em nuvem.</i></p> </div>

⚙️ Destaques da Arquitetura Backend
Neste projeto, foquei em implementar padrões de mercado para garantir uma aplicação segura e escalável:

Modelagem Relacional: Utilizei o SQLAlchemy ORM para gerenciar relacionamentos complexos entre as entidades de Usuários, Produtos, Categorias e Fornecedores, garantindo a integridade referencial do banco de dados.

Segurança e Autenticação: Implementação de hashing de senhas com Bcrypt e proteção de rotas via Session, impedindo acessos não autorizados ao backend.

Ambientes Dinâmicos: Configuração de suporte para múltiplos bancos de dados (SQLite para desenvolvimento ágil e PostgreSQL para ambiente de produção no Render).

Lógica de Negócio: Centralização da lógica de CRUD e filtros dinâmicos no servidor, reduzindo a carga de processamento no cliente.

🛠️ Tech Stack & Ferramentas
Core: Python (Backend Logic)

Framework: Flask (Microframework escalável)

ORM: SQLAlchemy (Abstração e segurança contra SQL Injection)

Deploy: Render (Paas) com gerenciamento de variáveis de ambiente (.env)

Frontend: Jinja2 Templates e Bootstrap 5 (Interface responsiva)

🔗 Links Úteis
Deploy ao vivo: https://estoque-muca.onrender.com

Portfólio no LinkedIn: Murilo Silva

🚀 Como Executar o Ambiente de Desenvolvimento
Clone o repositório:

Bash

git clone https://github.com/MuriloSilva110/projeto_estoque_web.git
cd projeto_estoque_web
Configuração do Ambiente Virtual:

Bash

python -m venv venv
# Ativação no Windows:
venv\Scripts\activate
Dependências e Execução:

Bash

pip install -r requirements.txt
python app.py
<p align="center">Estudante de ADS na Universidade Santo Amaro (Unisa) 🚀</p>
