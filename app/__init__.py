
import os

from flask import Flask, render_template, request, redirect, url_for, flash

from app.database import (
    criar_tabela,
    inserir_produto,
    listar_produtos,
    atualizar_produto,
    buscar_produto,
    inserir_negociacao,
    listar_negociacoes,
    atualizar_status_negociacao,
    excluir_produto,
    excluir_negociacao
)


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY",
        "chave-desenvolvimento-mm"
    )

    criar_tabela(app)

    @app.route("/")
    def inicio():
        return render_template("base.html")

    # CADASTRAR PRODUTO
    @app.route("/produtos/cadastrar", methods=["GET", "POST"])
    def cadastrar_produto():
        if request.method == "POST":
            nome = request.form.get("nome", "").strip()
            modelo = request.form.get("modelo", "").strip()
            caracteristicas = request.form.get("caracteristicas", "").strip()
            preco = request.form.get("preco", "").strip()
            disponibilidade = request.form.get("disponibilidade", "")

            if not nome or not modelo or not caracteristicas or not preco:
                flash("Preencha todos os campos.", "error")
                return render_template("cadastrar_produto.html")

            try:
                preco = preco.replace("R$", "").replace(".", "").replace(",", ".").strip()
                preco = float(preco)
            except ValueError:
                flash("Informe um preço válido.", "error")
                return render_template("cadastrar_produto.html")

            if preco <= 0:
                flash("O preço deve ser maior que zero.", "error")
                return render_template("cadastrar_produto.html")

            produto = {
                "nome": nome,
                "modelo": modelo,
                "caracteristicas": caracteristicas,
                "preco": preco,
                "disponibilidade": disponibilidade
            }

            inserir_produto(app, produto)
            flash("Produto cadastrado com sucesso!", "success")

            return redirect(url_for("consultar_produtos"))

        return render_template("cadastrar_produto.html")

    # CONSULTAR PRODUTOS
    @app.route("/produtos")
    def consultar_produtos():
        termo = request.args.get("busca", "").strip()
        produtos = listar_produtos(app, termo)

        return render_template(
            "consultar_produtos.html",
            produtos=produtos,
            termo=termo
        )

    # EDITAR PRODUTO
    @app.route("/produtos/<int:produto_id>/editar", methods=["GET", "POST"])
    def editar_produto(produto_id):
        produto = buscar_produto(app, produto_id)

        if produto is None:
            flash("Produto não encontrado.", "error")
            return redirect(url_for("consultar_produtos"))

        if request.method == "POST":
            nome = request.form.get("nome", "").strip()
            modelo = request.form.get("modelo", "").strip()
            caracteristicas = request.form.get("caracteristicas", "").strip()
            preco = request.form.get("preco", "").strip()
            disponibilidade = request.form.get("disponibilidade", "")

            if not nome or not modelo or not caracteristicas or not preco:
                flash("Preencha todos os campos.", "error")
                return render_template("editar_produto.html", produto=produto)

            try:
                preco = preco.replace("R$", "").replace(".", "").replace(",", ".").strip()
                preco = float(preco)
            except ValueError:
                flash("Informe um preço válido.", "error")
                return render_template("editar_produto.html", produto=produto)

            if preco <= 0:
                flash("O preço deve ser maior que zero.", "error")
                return render_template("editar_produto.html", produto=produto)

            dados_produto = {
                "nome": nome,
                "modelo": modelo,
                "caracteristicas": caracteristicas,
                "preco": preco,
                "disponibilidade": disponibilidade
            }

            atualizar_produto(app, produto_id, dados_produto)
            flash("Produto atualizado com sucesso!", "success")

            return redirect(url_for("consultar_produtos"))

        return render_template("editar_produto.html", produto=produto)

    # CADASTRAR NEGOCIAÇÃO
    @app.route("/negociacoes", methods=["GET", "POST"])
    def negociacoes():

        # Exibir somente produtos disponíveis
        produtos = [
            produto for produto in listar_produtos(app)
            if produto["disponibilidade"] == "Em estoque"
        ]

        if request.method == "POST":
            cliente = request.form.get("cliente", "").strip()
            produto_id = request.form.get("produto_id", "").strip()
            data = request.form.get("data", "").strip()

            if not cliente or not produto_id or not data:
                flash("Preencha todos os campos.", "error")
                return render_template(
                    "negociacoes.html",
                    produtos=produtos,
                    negociacoes=listar_negociacoes(app)
                )

            try:
                produto_id = int(produto_id)
            except ValueError:
                flash("Selecione um produto válido.", "error")
                return redirect(url_for("negociacoes"))

            produto = buscar_produto(app, produto_id)

            if produto is None:
                flash("Produto não encontrado.", "error")
                return redirect(url_for("negociacoes"))

            if produto["disponibilidade"] != "Em estoque":
                flash(
                    "Não é possível cadastrar interesse em um produto indisponível.",
                    "error"
                )
                return redirect(url_for("negociacoes"))

            inserir_negociacao(app, {
                "cliente": cliente,
                "produto_id": produto_id,
                "data": data
            })

            flash("Negociação cadastrada com sucesso!", "success")
            return redirect(url_for("negociacoes"))

        return render_template(
            "negociacoes.html",
            produtos=produtos,
            negociacoes=listar_negociacoes(app)
        )

    # ATUALIZAR STATUS DA NEGOCIAÇÃO
    @app.route("/negociacoes/<int:negociacao_id>/status", methods=["POST"])
    def alterar_status(negociacao_id):
        status = request.form.get("status", "")

        status_permitidos = [
            "Novo",
            "Em negociação",
            "Concluído",
            "Cancelado"
        ]

        if status not in status_permitidos:
            flash("Status inválido.", "error")
            return redirect(url_for("negociacoes"))

        atualizar_status_negociacao(app, negociacao_id, status)
        flash("Status atualizado com sucesso!", "success")

        return redirect(url_for("negociacoes"))

    # EXCLUIR NEGOCIAÇÃO
    @app.route("/negociacoes/<int:negociacao_id>/excluir", methods=["POST"])
    def excluir_negociacao_rota(negociacao_id):
        excluida = excluir_negociacao(app, negociacao_id)

        if not excluida:
            flash(
                "Esta negociação não pode ser excluída. "
                "Somente negociações com status Novo ou Cancelado podem ser excluídas.",
                "error"
            )
            return redirect(url_for("negociacoes"))

        flash("Negociação excluída com sucesso!", "success")
        return redirect(url_for("negociacoes"))

    # EXCLUIR PRODUTO
    @app.route("/produtos/<int:produto_id>/excluir", methods=["POST"])
    def excluir_produto_rota(produto_id):
        produto = buscar_produto(app, produto_id)

        if produto is None:
            flash("Produto não encontrado.", "error")
            return redirect(url_for("consultar_produtos"))

        excluido = excluir_produto(app, produto_id)

        if not excluido:
            flash(
                "Este produto possui negociações vinculadas e não pode ser excluído.",
                "error"
            )
            return redirect(url_for("consultar_produtos"))

        flash("Produto excluído com sucesso!", "success")
        return redirect(url_for("consultar_produtos"))

    return app
