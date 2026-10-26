"""Implementações das portas de use_cases/portas.py usando arquivos TXT.
Trocar por SQLite, por exemplo, exige apenas novas classes com os mesmos métodos."""
from datetime import datetime
from pathlib import Path

from entities import AvisoReposicao, ItemEstoque, Livro, Loja, Notificacao
from use_cases.portas import (RepositorioAvisos, RepositorioEstoque, RepositorioLivros,
                              RepositorioLojas, RepositorioNotificacoes,
                              RepositorioPreferencias)

from .arquivo_txt import ArquivoTxt

FORMATO_DATA = "%Y-%m-%d %H:%M:%S"


class RepositorioLivrosTxt(RepositorioLivros):
    """livros.txt → isbn|titulo|autor|preco"""

    def __init__(self, pasta):
        self._arquivo = ArquivoTxt(Path(pasta) / "livros.txt")

    def listar(self):
        return [Livro(i, t, a, float(p)) for i, t, a, p in self._arquivo.ler()]

    def buscar_por_isbn(self, isbn):
        return next((l for l in self.listar() if l.isbn == isbn), None)


class RepositorioLojasTxt(RepositorioLojas):
    """lojas.txt → id|nome|endereco|horario"""

    def __init__(self, pasta):
        self._arquivo = ArquivoTxt(Path(pasta) / "lojas.txt")

    def listar(self):
        return [Loja(*campos) for campos in self._arquivo.ler()]

    def buscar_por_id(self, loja_id):
        return next((l for l in self.listar() if l.id == loja_id), None)


class RepositorioEstoqueTxt(RepositorioEstoque):
    """estoque.txt → isbn|loja_id|quantidade"""

    def __init__(self, pasta):
        self._arquivo = ArquivoTxt(Path(pasta) / "estoque.txt")

    def _todos(self):
        return [ItemEstoque(i, l, int(q)) for i, l, q in self._arquivo.ler()]

    def do_livro(self, isbn):
        return [item for item in self._todos() if item.isbn == isbn]

    def buscar(self, isbn, loja_id):
        return next((i for i in self._todos() if (i.isbn, i.loja_id) == (isbn, loja_id)), None)

    def salvar(self, item):
        itens = self._todos()
        chave = (item.isbn, item.loja_id)
        posicao = next((n for n, i in enumerate(itens) if (i.isbn, i.loja_id) == chave), None)
        if posicao is None:
            itens.append(item)
        else:
            itens[posicao] = item
        self._arquivo.gravar([[i.isbn, i.loja_id, i.quantidade] for i in itens])


class RepositorioPreferenciasTxt(RepositorioPreferencias):
    """preferencias.txt → cliente_id|loja_favorita"""

    def __init__(self, pasta):
        self._arquivo = ArquivoTxt(Path(pasta) / "preferencias.txt")

    def loja_favorita(self, cliente_id):
        return dict(self._arquivo.ler()).get(cliente_id)

    def definir_loja_favorita(self, cliente_id, loja_id):
        prefs = dict(self._arquivo.ler())
        prefs[cliente_id] = loja_id
        self._arquivo.gravar([[c, l] for c, l in prefs.items()])


class RepositorioAvisosTxt(RepositorioAvisos):
    """avisos.txt → cliente_id|isbn|loja_id"""

    def __init__(self, pasta):
        self._arquivo = ArquivoTxt(Path(pasta) / "avisos.txt")

    def _todos(self):
        return [AvisoReposicao(*campos) for campos in self._arquivo.ler()]

    def existe(self, aviso):
        return aviso in self._todos()

    def salvar(self, aviso):
        self._arquivo.acrescentar([aviso.cliente_id, aviso.isbn, aviso.loja_id])

    def pendentes(self, isbn, loja_id):
        return [a for a in self._todos() if (a.isbn, a.loja_id) == (isbn, loja_id)]

    def remover(self, aviso):
        restantes = [a for a in self._todos() if a != aviso]
        self._arquivo.gravar([[a.cliente_id, a.isbn, a.loja_id] for a in restantes])


class RepositorioNotificacoesTxt(RepositorioNotificacoes):
    """notificacoes.txt → cliente_id|data_hora|mensagem"""

    def __init__(self, pasta):
        self._arquivo = ArquivoTxt(Path(pasta) / "notificacoes.txt")

    def salvar(self, n):
        self._arquivo.acrescentar([n.cliente_id, n.criada_em.strftime(FORMATO_DATA), n.mensagem])

    def do_cliente(self, cliente_id):
        return [Notificacao(c, datetime.strptime(d, FORMATO_DATA), m)
                for c, d, m in self._arquivo.ler() if c == cliente_id]
