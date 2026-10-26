"""Casos de uso testados com repositórios em memória (sem TXT, sem Flask)."""
import pytest

from entities import ErroDeNegocio, NaoEncontrado
from tests.fakes import (AvisosMemoria, NotificacoesMemoria, PreferenciasMemoria, RelogioFixo,
                         dados_exemplo)
from use_cases import (AtualizarEstoque, BuscarLivros, CadastrarAvisoReposicao,
                       ConsultarDisponibilidade, DefinirLojaFavorita, ListarNotificacoes,
                       ObterLojaFavorita, VerLoja)


@pytest.fixture
def ctx():
    livros, lojas, estoque = dados_exemplo()
    prefs, avisos, notificacoes = PreferenciasMemoria(), AvisosMemoria(), NotificacoesMemoria()
    return {
        "buscar": BuscarLivros(livros),
        "disp": ConsultarDisponibilidade(livros, lojas, estoque, prefs),
        "ver_loja": VerLoja(lojas),
        "favoritar": DefinirLojaFavorita(lojas, prefs),
        "favorita": ObterLojaFavorita(prefs),
        "aviso": CadastrarAvisoReposicao(livros, lojas, estoque, avisos),
        "estoque": AtualizarEstoque(livros, lojas, estoque, avisos, notificacoes, RelogioFixo()),
        "notificacoes": ListarNotificacoes(notificacoes),
        "avisos_repo": avisos,
    }


# ----- MVP -----

def test_buscar_por_autor(ctx):
    assert [l.titulo for l in ctx["buscar"].executar("machado")] == ["Dom Casmurro"]


def test_estoque_e_preco_por_loja(ctx):
    livro, itens = ctx["disp"].executar("dom")
    assert livro.preco == 29.90
    assert [(i["loja"].id, i["estoque"].quantidade) for i in itens] == [("paulista", 3), ("pinheiros", 0)]


def test_livro_inexistente(ctx):
    with pytest.raises(NaoEncontrado, match="Livro não encontrado"):
        ctx["disp"].executar("000")


def test_ver_loja(ctx):
    assert ctx["ver_loja"].executar("paulista").horario == "10h às 22h"
    with pytest.raises(NaoEncontrado, match="Loja não encontrada"):
        ctx["ver_loja"].executar("centro")


def test_favorita_aparece_primeiro(ctx):
    ctx["favoritar"].executar("ana", "pinheiros")
    assert ctx["favorita"].executar("ana") == "pinheiros"
    _, itens = ctx["disp"].executar("hora", "ana")
    assert itens[0]["loja"].id == "pinheiros" and itens[0]["favorita"]


def test_favorita_e_por_cliente(ctx):
    ctx["favoritar"].executar("ana", "pinheiros")
    _, itens = ctx["disp"].executar("hora", "bia")
    assert itens[0]["loja"].id == "paulista"


# ----- Nova feature: aviso de reposição -----

def test_notifica_quando_volta_ao_estoque(ctx):
    ctx["aviso"].executar("ana", "dom", "pinheiros")
    _, notificados = ctx["estoque"].executar("dom", "pinheiros", 4)
    assert notificados == 1
    [n] = ctx["notificacoes"].executar("ana")
    assert n.mensagem == "O livro Dom Casmurro voltou ao estoque na Livraria Pinheiros."
    assert ctx["avisos_repo"].lista == []  # aviso encerrado


def test_estoque_atualizado(ctx):
    ctx["estoque"].executar("dom", "pinheiros", 4)
    _, itens = ctx["disp"].executar("dom")
    assert itens[1]["estoque"].quantidade == 4


def test_sem_aviso_nao_notifica(ctx):
    ctx["estoque"].executar("dom", "pinheiros", 4)
    assert ctx["notificacoes"].executar("ana") == []


def test_aviso_de_livro_disponivel(ctx):
    with pytest.raises(ErroDeNegocio, match="O livro está disponível nesta loja"):
        ctx["aviso"].executar("ana", "dom", "paulista")


def test_aviso_em_loja_que_nao_trabalha_com_o_livro(ctx):
    with pytest.raises(ErroDeNegocio, match="Esta loja não trabalha com este livro"):
        ctx["aviso"].executar("ana", "sertao", "paulista")


def test_aviso_repetido(ctx):
    ctx["aviso"].executar("ana", "dom", "pinheiros")
    with pytest.raises(ErroDeNegocio, match="Aviso já cadastrado"):
        ctx["aviso"].executar("ana", "dom", "pinheiros")


def test_quantidade_negativa_nao_altera_estoque(ctx):
    with pytest.raises(ErroDeNegocio, match="Quantidade inválida"):
        ctx["estoque"].executar("dom", "paulista", -1)
    _, itens = ctx["disp"].executar("dom")
    assert itens[0]["estoque"].quantidade == 3
