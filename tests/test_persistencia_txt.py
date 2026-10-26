"""Os repositórios TXT gravam e leem os dados de verdade em arquivos."""
from datetime import datetime

from entities import AvisoReposicao, ItemEstoque, Notificacao
from frameworks_drivers.persistencia import (RepositorioAvisosTxt, RepositorioEstoqueTxt,
                                             RepositorioLivrosTxt, RepositorioLojasTxt,
                                             RepositorioNotificacoesTxt,
                                             RepositorioPreferenciasTxt, criar_dados_iniciais)


def test_dados_iniciais_criam_arquivos(tmp_path):
    criar_dados_iniciais(tmp_path)
    assert {p.name for p in tmp_path.iterdir()} == {"livros.txt", "lojas.txt", "estoque.txt"}
    assert "Dom Casmurro" in (tmp_path / "livros.txt").read_text(encoding="utf-8")
    assert len(RepositorioLivrosTxt(tmp_path).listar()) == 4
    assert RepositorioLojasTxt(tmp_path).buscar_por_id("paulista").nome == "Livraria Paulista"


def test_dados_iniciais_nao_sobrescrevem(tmp_path):
    criar_dados_iniciais(tmp_path)
    RepositorioEstoqueTxt(tmp_path).salvar(ItemEstoque("9788535902775", "pinheiros", 9))
    criar_dados_iniciais(tmp_path)
    assert RepositorioEstoqueTxt(tmp_path).buscar("9788535902775", "pinheiros").quantidade == 9


def test_estoque_persiste_entre_instancias(tmp_path):
    criar_dados_iniciais(tmp_path)
    RepositorioEstoqueTxt(tmp_path).salvar(ItemEstoque("9788535902775", "pinheiros", 7))
    assert RepositorioEstoqueTxt(tmp_path).buscar("9788535902775", "pinheiros").quantidade == 7
    assert "9788535902775|pinheiros|7" in (tmp_path / "estoque.txt").read_text(encoding="utf-8")


def test_preferencias(tmp_path):
    RepositorioPreferenciasTxt(tmp_path).definir_loja_favorita("ana", "pinheiros")
    RepositorioPreferenciasTxt(tmp_path).definir_loja_favorita("ana", "paulista")
    assert RepositorioPreferenciasTxt(tmp_path).loja_favorita("ana") == "paulista"
    assert (tmp_path / "preferencias.txt").read_text(encoding="utf-8") == "ana|paulista\n"


def test_avisos(tmp_path):
    repo, aviso = RepositorioAvisosTxt(tmp_path), AvisoReposicao("ana", "1", "a")
    repo.salvar(aviso)
    assert RepositorioAvisosTxt(tmp_path).existe(aviso)
    assert RepositorioAvisosTxt(tmp_path).pendentes("1", "a") == [aviso]
    repo.remover(aviso)
    assert not RepositorioAvisosTxt(tmp_path).existe(aviso)


def test_notificacoes(tmp_path):
    n = Notificacao("ana", datetime(2026, 10, 25, 14, 30), "Chegou | o livro")
    RepositorioNotificacoesTxt(tmp_path).salvar(n)
    [lida] = RepositorioNotificacoesTxt(tmp_path).do_cliente("ana")
    assert lida.criada_em == n.criada_em and lida.mensagem == "Chegou / o livro"
