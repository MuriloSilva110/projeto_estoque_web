from app import app, db, Fornecedor, Categoria, Produto

def obter_ou_criar_fornecedor(nome, telefone):
    # Tenta achar no banco
    fornecedor = Fornecedor.query.filter_by(nome=nome).first()
    # Se não existir, cria
    if not fornecedor:
        fornecedor = Fornecedor(nome=nome, telefone=telefone)
        db.session.add(fornecedor)
        print(f"Fornecedor criado: {nome}")
    else:
        print(f"Fornecedor já existe: {nome}")
    return fornecedor

def obter_ou_criar_categoria(nome):
    categoria = Categoria.query.filter_by(nome=nome).first()
    if not categoria:
        categoria = Categoria(nome=nome)
        db.session.add(categoria)
        print(f"Categoria criada: {nome}")
    else:
        print(f"Categoria já existe: {nome}")
    return categoria

def criar_produto_se_nao_existir(nome, preco, codigo, fornecedor, categoria):
    produto = Produto.query.filter_by(codigo_interno=codigo).first()
    if not produto:
        produto = Produto(
            nome=nome, 
            preco=preco, 
            codigo_interno=codigo,
            fornecedor=fornecedor, # O SQLAlchemy pega o ID sozinho aqui
            categoria=categoria
        )
        db.session.add(produto)
        print(f"Produto criado: {nome}")
    else:
        print(f"Produto já existe: {nome}")

# --- A Mágica Acontece Aqui ---
with app.app_context():
    # 1. Criar Fornecedores
    f_samsung = obter_ou_criar_fornecedor("Samsung", "0800-1234")
    f_nike = obter_ou_criar_fornecedor("Nike", "11-9999-8888")
    f_apple = obter_ou_criar_fornecedor("Apple", "0800-APPLE")
    f_coca = obter_ou_criar_fornecedor("Coca-Cola", "0800-COCA")

    # 2. Criar Categorias
    c_eletronicos = obter_ou_criar_categoria("Eletrônicos")
    c_roupas = obter_ou_criar_categoria("Roupas")
    c_bebidas = obter_ou_criar_categoria("Bebidas")
    c_livros = obter_ou_criar_categoria("Livros")

    # Salva os pais primeiro para garantir que tenham IDs
    db.session.commit() 

    # 3. Criar Produtos (Usando os objetos que criamos acima)
    criar_produto_se_nao_existir("Galaxy S23", 4500.00, "SAM-S23", f_samsung, c_eletronicos)
    criar_produto_se_nao_existir("iPhone 14", 6500.00, "APP-IP14", f_apple, c_eletronicos)
    criar_produto_se_nao_existir("Tênis Air Max", 599.90, "NK-AIR", f_nike, c_roupas)
    criar_produto_se_nao_existir("Coca-Cola 2L", 9.50, "CC-2L", f_coca, c_bebidas)
    
    # Commit final para salvar os produtos
    db.session.commit()
    print("\n--- Banco de dados populado com sucesso! ---")