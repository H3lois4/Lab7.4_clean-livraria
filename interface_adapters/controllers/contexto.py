import uuid

from flask import current_app, session


def caso_de_uso(nome):
    return current_app.config["CASOS_DE_USO"][nome]


def cliente_id():
    if "cliente_id" not in session:
        session["cliente_id"] = uuid.uuid4().hex
    return session["cliente_id"]


def voltar(padrao):
    from flask import request
    return request.form.get("voltar") or padrao
