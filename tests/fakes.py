"""Implementações em memória das portas. Mostram o DIP na prática: os casos de uso
rodam com elas sem saber que, em produção, os dados ficam em arquivos TXT."""
from datetime import datetime

from entities import ItemEstoque, Livro, Loja
from use_cases.portas import (RepositorioAvisos, RepositorioEstoque, RepositorioLivros,
                              RepositorioLojas, RepositorioNotificacoes,
                              RepositorioPreferencias, Relogio)


class LivrosMemoria(RepositorioLivros):
    def __init__(self, livros): self.d = {l.isbn: l for l in livros}
    def listar(self): return list(self.d.values())
    def buscar_por_isbn(self, isbn): return self.d.get(isbn)


class LojasMemoria(RepositorioLojas):
    def __init__(self, lojas): self.d = {l.id: l for l in lojas}
    def listar(self): return list(self.d.values())
    def buscar_por_id(self, loja_id): return self.d.get(loja_id)


class EstoqueMemoria(RepositorioEstoque):
    def __init__(self, itens): self.d = {(i.isbn, i.loja_id): i for i in itens}
    def do_livro(self, isbn): return [i for i in self.d.values() if i.isbn == isbn]
    def buscar(self, isbn, loja_id): return self.d.get((isbn, loja_id))
    def salvar(self, item): self.d[(item.isbn, item.loja_id)] = item


class PreferenciasMemoria(RepositorioPreferencias):
    def __init__(self): self.d = {}
    def loja_favorita(self, cliente_id): return self.d.get(cliente_id)
    def definir_loja_favorita(self, cliente_id, loja_id): self.d[cliente_id] = loja_id


class AvisosMemoria(RepositorioAvisos):
    def __init__(self): self.lista = []
    def existe(self, aviso): return aviso in self.lista
    def salvar(self, aviso): self.lista.append(aviso)
    def pendentes(self, isbn, loja_id):
        return [a for a in self.lista if (a.isbn, a.loja_id) == (isbn, loja_id)]
    def remover(self, aviso): self.lista.remove(aviso)


class NotificacoesMemoria(RepositorioNotificacoes):
    def __init__(self): self.lista = []
    def salvar(self, n): self.lista.append(n)
    def do_cliente(self, cliente_id): return [n for n in self.lista if n.cliente_id == cliente_id]


class RelogioFixo(Relogio):
    def agora(self): return datetime(2026, 10, 25, 14, 30)


def dados_exemplo():
    lojas = LojasMemoria([
        Loja("paulista", "Livraria Paulista", "Av. Paulista, 1000", "10h às 22h"),
        Loja("pinheiros", "Livraria Pinheiros", "Rua dos Pinheiros, 500", "9h às 21h"),
    ])
    livros = LivrosMemoria([
        Livro("dom", "Dom Casmurro", "Machado de Assis", 29.90),
        Livro("hora", "A Hora da Estrela", "Clarice Lispector", 39.90),
        Livro("sertao", "Grande Sertão: Veredas", "João Guimarães Rosa", 89.00),
    ])
    estoque = EstoqueMemoria([
        ItemEstoque("dom", "paulista", 3), ItemEstoque("dom", "pinheiros", 0),
        ItemEstoque("hora", "paulista", 1), ItemEstoque("hora", "pinheiros", 5),
        ItemEstoque("sertao", "pinheiros", 2),
    ])
    return livros, lojas, estoque
