from flask import Blueprint, abort, render_template, request

from entities import NaoEncontrado

from ..presenters import apresentar_disponibilidade, apresentar_livro
from .contexto import caso_de_uso, cliente_id

livros_bp = Blueprint("livros", __name__)


@livros_bp.get("/")
def buscar():
    termo = request.args.get("q", "")
    livros = caso_de_uso("buscar_livros").executar(termo)
    return render_template("livros/busca.html", termo=termo,
                           livros=[apresentar_livro(l) for l in livros])


@livros_bp.get("/livros/<isbn>")
def detalhe(isbn):
    try:
        livro, itens = caso_de_uso("consultar_disponibilidade").executar(isbn, cliente_id())
    except NaoEncontrado as erro:
        abort(404, description=str(erro))
    return render_template("livros/detalhe.html", livro=apresentar_livro(livro),
                           lojas=apresentar_disponibilidade(itens))
