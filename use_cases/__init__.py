"""Círculo 2 – Use Cases: regras da aplicação. Dependem apenas das Entities e das
portas (interfaces) definidas aqui mesmo – Princípio da Inversão de Dependência."""
from .avisos import AtualizarEstoque, CadastrarAvisoReposicao, ListarNotificacoes
from .catalogo import BuscarLivros, ConsultarDisponibilidade, ListarLojas, VerLoja
from .lojas import DefinirLojaFavorita, ObterLojaFavorita

__all__ = ["BuscarLivros", "ConsultarDisponibilidade", "ListarLojas", "VerLoja",
           "DefinirLojaFavorita", "ObterLojaFavorita", "CadastrarAvisoReposicao", "AtualizarEstoque",
           "ListarNotificacoes"]
