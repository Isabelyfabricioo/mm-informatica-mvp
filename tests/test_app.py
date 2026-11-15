
import pytest
import app.database as database
from app import create_app


@pytest.fixture
def client(tmp_path, monkeypatch):
    banco_teste = tmp_path / "teste_mm_informatica.db"

    monkeypatch.setattr(
        database,
        "caminho_banco",
        lambda app: str(banco_teste)
    )

    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def cadastrar_produto(client):
    return client.post(
        "/produtos/cadastrar",
        data={
            "nome": "Notebook",
            "modelo": "Dell Inspiron",
            "caracteristicas": "8GB RAM, SSD 256GB",
            "preco": "R$ 2.500,00",
            "disponibilidade": "Em estoque"
        },
        follow_redirects=True
    )


def test_pagina_inicial(client):
    resposta = client.get("/")
    assert resposta.status_code == 200


def test_acessar_cadastro_produto(client):
    resposta = client.get("/produtos/cadastrar")
    assert resposta.status_code == 200


def test_cadastrar_produto(client):
    resposta = cadastrar_produto(client)

    assert resposta.status_code == 200

    produtos = database.listar_produtos(client.application)

    assert len(produtos) == 1
    assert produtos[0]["nome"] == "Notebook"


def test_consultar_produtos(client):
    cadastrar_produto(client)

    resposta = client.get("/produtos")

    assert resposta.status_code == 200
    assert b"Notebook" in resposta.data


def test_acessar_negociacoes(client):
    resposta = client.get("/negociacoes")
    assert resposta.status_code == 200


def test_acessar_edicao_produto(client):
    cadastrar_produto(client)

    produtos = database.listar_produtos(client.application)
    produto_id = produtos[0]["id"]

    resposta = client.get(f"/produtos/{produto_id}/editar")

    assert resposta.status_code == 200


def test_excluir_produto_sem_negociacoes(client):
    cadastrar_produto(client)

    produtos = database.listar_produtos(client.application)
    produto_id = produtos[0]["id"]

    resposta = client.post(
        f"/produtos/{produto_id}/excluir",
        follow_redirects=True
    )

    assert resposta.status_code == 200

    produtos = database.listar_produtos(client.application)
    assert len(produtos) == 0
