from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from entities import ErroDeNegocio, NaoEncontrado

from ..presenters import apresentar_livro, apresentar_loja, apresentar_notificacao
from .contexto import caso_de_uso, cliente_id, voltar

avisos_bp = Blueprint("avisos", __name__)


@avisos_bp.post("/avisos")
def cadastrar():
    isbn, loja_id = request.form.get("isbn", ""), request.form.get("loja_id", "")
    try:
        livro, loja = caso_de_uso("cadastrar_aviso").executar(cliente_id(), isbn, loja_id)
        flash(f"Você será avisado quando {livro.titulo} voltar à {loja.nome}.")
    except NaoEncontrado as erro:
        abort(404, description=str(erro))
    except ErroDeNegocio as erro:
        flash(str(erro), "erro")
    return redirect(voltar(url_for("avisos.notificacoes")))


@avisos_bp.get("/notificacoes")
def notificacoes():
    itens = caso_de_uso("listar_notificacoes").executar(cliente_id())
    return render_template("avisos/notificacoes.html",
                           notificacoes=[apresentar_notificacao(n) for n in itens])


@avisos_bp.get("/estoque")
def formulario_estoque():
    livros = [apresentar_livro(l) for l in caso_de_uso("buscar_livros").executar("")]
    lojas = [apresentar_loja(l) for l in caso_de_uso("listar_lojas").executar()]
    return render_template("avisos/estoque.html", livros=livros, lojas=lojas)


@avisos_bp.post("/estoque")
def atualizar_estoque():
    try:
        quantidade = int(request.form.get("quantidade", ""))
    except ValueError:
        flash("Quantidade inválida", "erro")
        return redirect(url_for("avisos.formulario_estoque"))
    try:
        _, notificados = caso_de_uso("atualizar_estoque").executar(
            request.form.get("isbn", ""), request.form.get("loja_id", ""), quantidade)
        extra = f" {notificados} cliente(s) notificado(s)." if notificados else ""
        flash("Estoque atualizado." + extra)
    except NaoEncontrado as erro:
        abort(404, description=str(erro))
    except ErroDeNegocio as erro:
        flash(str(erro), "erro")
    return redirect(url_for("avisos.formulario_estoque"))
