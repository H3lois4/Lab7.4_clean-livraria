"""Fluxo completo pela interface web, gravando em uma pasta TXT temporária."""
import pytest

from app import create_app

DOM = "9788535902775"


@pytest.fixture
def cliente(tmp_path):
    app = create_app(tmp_path)
    app.config["TESTING"] = True
    return app.test_client()


def html(resp):
    return resp.get_data(as_text=True)


def test_busca(cliente):
    pagina = html(cliente.get("/?q=clarice"))
    assert "A Hora da Estrela" in pagina and "R$ 39,90" in pagina and "Dom Casmurro" not in pagina


def test_detalhe(cliente):
    pagina = html(cliente.get(f"/livros/{DOM}"))
    assert "3 em estoque" in pagina and "Esgotado" in pagina and "Avisar quando chegar" in pagina


def test_404(cliente):
    assert cliente.get("/livros/000").status_code == 404
    assert cliente.get("/lojas/centro").status_code == 404


def test_favoritar(cliente):
    cliente.post("/lojas/pinheiros/favorita")
    pagina = html(cliente.get("/livros/9788501114775"))
    assert pagina.index("Livraria Pinheiros") < pagina.index("Livraria Paulista")


def test_fluxo_aviso_de_reposicao(cliente, tmp_path):
    resp = cliente.post("/avisos", data={"isbn": DOM, "loja_id": "pinheiros"}, follow_redirects=True)
    assert "Você será avisado quando Dom Casmurro voltar à Livraria Pinheiros." in html(resp)
    assert "pinheiros" in (tmp_path / "avisos.txt").read_text(encoding="utf-8")

    resp = cliente.post("/estoque", data={"isbn": DOM, "loja_id": "pinheiros", "quantidade": "4"},
                        follow_redirects=True)
    assert "1 cliente(s) notificado(s)" in html(resp)
    assert "O livro Dom Casmurro voltou ao estoque na Livraria Pinheiros." in html(cliente.get("/notificacoes"))
    assert (tmp_path / "avisos.txt").read_text(encoding="utf-8") == ""


def test_aviso_de_livro_disponivel(cliente):
    resp = cliente.post("/avisos", data={"isbn": DOM, "loja_id": "paulista"}, follow_redirects=True)
    assert "O livro está disponível nesta loja" in html(resp)


def test_quantidade_invalida(cliente):
    resp = cliente.post("/estoque", data={"isbn": DOM, "loja_id": "paulista", "quantidade": "-2"},
                        follow_redirects=True)
    assert "Quantidade inválida" in html(resp)


def test_dados_persistem_apos_reiniciar(tmp_path):
    create_app(tmp_path).test_client().post(
        "/estoque", data={"isbn": DOM, "loja_id": "pinheiros", "quantidade": "6"})
    pagina = html(create_app(tmp_path).test_client().get(f"/livros/{DOM}"))
    assert "6 em estoque" in pagina
