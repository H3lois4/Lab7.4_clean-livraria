import pytest

from entities import AvisoReposicao, ErroDeNegocio, ItemEstoque, Livro


def test_busca_ignora_acentos():
    livro = Livro("1", "Memórias Póstumas", "Machado de Assis", 10)
    assert livro.corresponde("memorias") and livro.corresponde("MACHADO")


def test_quantidade_negativa_e_invalida():
    with pytest.raises(ErroDeNegocio, match="Quantidade inválida"):
        ItemEstoque("1", "a", -1)


def test_disponibilidade():
    assert ItemEstoque("1", "a", 2).disponivel and not ItemEstoque("1", "a", 0).disponivel


def test_regra_de_reposicao():
    assert ItemEstoque("1", "a", 0).voltou_ao_estoque(3)
    assert not ItemEstoque("1", "a", 2).voltou_ao_estoque(3)
    assert not ItemEstoque("1", "a", 0).voltou_ao_estoque(0)


def test_aviso_so_para_livro_esgotado():
    with pytest.raises(ErroDeNegocio, match="O livro está disponível nesta loja"):
        AvisoReposicao.pode_ser_criado(ItemEstoque("1", "a", 1))
