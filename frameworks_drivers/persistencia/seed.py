"""Cria os arquivos TXT com os dados iniciais, apenas se ainda não existirem."""
from pathlib import Path

from .arquivo_txt import ArquivoTxt

LOJAS = [
    ["paulista", "Livraria Paulista", "Av. Paulista, 1000 – São Paulo",
     "Seg a sáb, 10h às 22h; dom, 12h às 20h"],
    ["pinheiros", "Livraria Pinheiros", "Rua dos Pinheiros, 500 – São Paulo",
     "Todos os dias, 9h às 21h"],
]
LIVROS = [
    ["9788535902775", "Dom Casmurro", "Machado de Assis", "29.90"],
    ["9788571641149", "Memórias Póstumas de Brás Cubas", "Machado de Assis", "34.50"],
    ["9788535914641", "Grande Sertão: Veredas", "João Guimarães Rosa", "89.00"],
    ["9788501114775", "A Hora da Estrela", "Clarice Lispector", "39.90"],
]
ESTOQUE = [
    ["9788535902775", "paulista", "3"], ["9788535902775", "pinheiros", "0"],
    ["9788571641149", "paulista", "0"], ["9788535914641", "pinheiros", "2"],
    ["9788501114775", "paulista", "1"], ["9788501114775", "pinheiros", "5"],
]


def criar_dados_iniciais(pasta):
    pasta = Path(pasta)
    for nome, registros in [("lojas.txt", LOJAS), ("livros.txt", LIVROS), ("estoque.txt", ESTOQUE)]:
        arquivo = ArquivoTxt(pasta / nome)
        if not arquivo.caminho.exists():
            arquivo.gravar(registros)
