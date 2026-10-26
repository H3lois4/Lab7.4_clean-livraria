"""Nova feature: ser avisado quando um livro esgotado voltar ao estoque."""
from entities import AvisoReposicao, ErroDeNegocio, ItemEstoque, Notificacao

from .catalogo import obter_livro, obter_loja


def obter_item(repo_estoque, isbn, loja_id):
    item = repo_estoque.buscar(isbn, loja_id)
    if item is None:
        raise ErroDeNegocio("Esta loja não trabalha com este livro")
    return item


class CadastrarAvisoReposicao:
    def __init__(self, repo_livros, repo_lojas, repo_estoque, repo_avisos):
        self._livros, self._lojas = repo_livros, repo_lojas
        self._estoque, self._avisos = repo_estoque, repo_avisos

    def executar(self, cliente_id, isbn, loja_id):
        livro = obter_livro(self._livros, isbn)
        loja = obter_loja(self._lojas, loja_id)
        AvisoReposicao.pode_ser_criado(obter_item(self._estoque, isbn, loja_id))
        aviso = AvisoReposicao(cliente_id, isbn, loja_id)
        if self._avisos.existe(aviso):
            raise ErroDeNegocio("Aviso já cadastrado")
        self._avisos.salvar(aviso)
        return livro, loja


class AtualizarEstoque:
    """Atualiza a quantidade e, se o livro voltou ao estoque, notifica e encerra os avisos."""

    def __init__(self, repo_livros, repo_lojas, repo_estoque, repo_avisos,
                 repo_notificacoes, relogio):
        self._livros, self._lojas, self._estoque = repo_livros, repo_lojas, repo_estoque
        self._avisos, self._notificacoes, self._relogio = repo_avisos, repo_notificacoes, relogio

    def executar(self, isbn, loja_id, quantidade):
        livro = obter_livro(self._livros, isbn)
        loja = obter_loja(self._lojas, loja_id)
        atual = obter_item(self._estoque, isbn, loja_id)
        novo = ItemEstoque(isbn, loja_id, quantidade)  # valida quantidade negativa

        notificados = 0
        if atual.voltou_ao_estoque(quantidade):
            for aviso in self._avisos.pendentes(isbn, loja_id):
                self._notificacoes.salvar(
                    Notificacao.de_reposicao(aviso, livro, loja, self._relogio.agora()))
                self._avisos.remover(aviso)
                notificados += 1

        self._estoque.salvar(novo)
        return novo, notificados


class ListarNotificacoes:
    def __init__(self, repo_notificacoes):
        self._notificacoes = repo_notificacoes

    def executar(self, cliente_id):
        return sorted(self._notificacoes.do_cliente(cliente_id),
                      key=lambda n: n.criada_em, reverse=True)
