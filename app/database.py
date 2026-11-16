
import sqlite3
import os


# Local onde o banco de dados será armazenado
def caminho_banco(app):
    os.makedirs(app.instance_path, exist_ok=True)

    return os.path.join(
        app.instance_path,
        "mm_informatica.db"
    )


# Criar as tabelas do banco de dados
def criar_tabela(app):
    conexao = sqlite3.connect(caminho_banco(app))

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            modelo TEXT NOT NULL,
            caracteristicas TEXT NOT NULL,
            preco REAL NOT NULL,
            disponibilidade TEXT NOT NULL
        )
    """)

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS negociacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT NOT NULL,
            produto_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Novo',
            FOREIGN KEY (produto_id) REFERENCES produtos(id)
        )
    """)

    conexao.commit()
    conexao.close()


# Salvar um produto no banco de dados
def inserir_produto(app, produto):
    conexao = sqlite3.connect(caminho_banco(app))

    conexao.execute("""
        INSERT INTO produtos (
            nome, modelo, caracteristicas, preco, disponibilidade
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        produto["nome"],
        produto["modelo"],
        produto["caracteristicas"],
        produto["preco"],
        produto["disponibilidade"]
    ))

    conexao.commit()
    conexao.close()


# Consultar produtos com opção de pesquisa
def listar_produtos(app, termo=""):
    conexao = sqlite3.connect(caminho_banco(app))
    conexao.row_factory = sqlite3.Row

    produtos = conexao.execute("""
        SELECT * FROM produtos
        WHERE nome LIKE ? OR modelo LIKE ?
        ORDER BY id DESC
    """, (f"%{termo}%", f"%{termo}%")).fetchall()

    conexao.close()
    return produtos


# Atualizar um produto cadastrado
def atualizar_produto(app, produto_id, produto):
    conexao = sqlite3.connect(caminho_banco(app))

    conexao.execute("""
        UPDATE produtos
        SET nome = ?,
            modelo = ?,
            caracteristicas = ?,
            preco = ?,
            disponibilidade = ?
        WHERE id = ?
    """, (
        produto["nome"],
        produto["modelo"],
        produto["caracteristicas"],
        produto["preco"],
        produto["disponibilidade"],
        produto_id
    ))

    conexao.commit()
    conexao.close()


# Buscar um produto específico pelo ID
def buscar_produto(app, produto_id):
    conexao = sqlite3.connect(caminho_banco(app))
    conexao.row_factory = sqlite3.Row

    produto = conexao.execute("""
        SELECT * FROM produtos
        WHERE id = ?
    """, (produto_id,)).fetchone()

    conexao.close()
    return produto


# Cadastrar uma negociação
def inserir_negociacao(app, negociacao):
    conexao = sqlite3.connect(caminho_banco(app))

    conexao.execute("""
        INSERT INTO negociacoes (
            cliente, produto_id, data, status
        )
        VALUES (?, ?, ?, ?)
    """, (
        negociacao["cliente"],
        negociacao["produto_id"],
        negociacao["data"],
        "Novo"
    ))

    conexao.commit()
    conexao.close()


# Consultar negociações cadastradas
def listar_negociacoes(app):
    conexao = sqlite3.connect(caminho_banco(app))
    conexao.row_factory = sqlite3.Row

    negociacoes = conexao.execute("""
        SELECT
            negociacoes.id,
            negociacoes.cliente,
            negociacoes.data,
            negociacoes.status,
            produtos.nome AS produto,
            produtos.modelo AS modelo
        FROM negociacoes
        INNER JOIN produtos
            ON negociacoes.produto_id = produtos.id
        ORDER BY negociacoes.id DESC
    """).fetchall()

    conexao.close()
    return negociacoes


# Atualizar o status de uma negociação
def atualizar_status_negociacao(app, negociacao_id, status):
    conexao = sqlite3.connect(caminho_banco(app))

    conexao.execute("""
        UPDATE negociacoes
        SET status = ?
        WHERE id = ?
    """, (status, negociacao_id))

    conexao.commit()
    conexao.close()


def excluir_produto(app, produto_id):
    conexao = sqlite3.connect(caminho_banco(app))

    try:
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM negociacoes WHERE produto_id = ?",
            (produto_id,)
        )

        quantidade = cursor.fetchone()[0]

        if quantidade > 0:
            return False

        cursor.execute(
            "DELETE FROM produtos WHERE id = ?",
            (produto_id,)
        )

        conexao.commit()

        return cursor.rowcount > 0

    finally:
        conexao.close()
