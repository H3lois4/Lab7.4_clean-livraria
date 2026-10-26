from flask import Blueprint, abort, flash, redirect, render_template, url_for

from entities import NaoEncontrado

from ..presenters import apresentar_loja
from .contexto import caso_de_uso, cliente_id, voltar

lojas_bp = Blueprint("lojas", __name__, url_prefix="/lojas")


def _favorita():
    return caso_de_uso("obter_loja_favorita").executar(cliente_id())


@lojas_bp.get("/")
def listar():
    favorita = _favorita()
    lojas = [apresentar_loja(l, favorita) for l in caso_de_uso("listar_lojas").executar()]
    return render_template("lojas/lista.html", lojas=lojas)


@lojas_bp.get("/<loja_id>")
def detalhe(loja_id):
    try:
        loja = caso_de_uso("ver_loja").executar(loja_id)
    except NaoEncontrado as erro:
        abort(404, description=str(erro))
    return render_template("lojas/detalhe.html", loja=apresentar_loja(loja, _favorita()))


@lojas_bp.post("/<loja_id>/favorita")
def favoritar(loja_id):
    try:
        loja = caso_de_uso("definir_loja_favorita").executar(cliente_id(), loja_id)
    except NaoEncontrado as erro:
        abort(404, description=str(erro))
    flash(f"{loja.nome} agora é sua loja favorita.")
    return redirect(voltar(url_for("lojas.listar")))
