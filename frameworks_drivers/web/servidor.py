"""Configuração do Flask: templates, arquivos estáticos e rotas dos controllers."""
from pathlib import Path

from flask import Flask, render_template

from interface_adapters.controllers import avisos_bp, livros_bp, lojas_bp

PASTA = Path(__file__).parent


def criar_servidor_web(casos_de_uso, chave_secreta="troque-esta-chave"):
    app = Flask(__name__, template_folder=str(PASTA / "templates"),
                static_folder=str(PASTA / "static"))
    app.config["SECRET_KEY"] = chave_secreta
    app.config["CASOS_DE_USO"] = casos_de_uso
    for blueprint in (livros_bp, lojas_bp, avisos_bp):
        app.register_blueprint(blueprint)

    @app.errorhandler(404)
    def nao_encontrado(erro):
        return render_template("erro.html", mensagem=erro.description), 404

    return app
