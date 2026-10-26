"""Main: o único ponto que conhece todos os círculos. Cria as implementações concretas
(TXT, relógio, Flask) e as injeta nos casos de uso – a "cola" da Clean Architecture."""
import os

from frameworks_drivers.persistencia import (RepositorioAvisosTxt, RepositorioEstoqueTxt,
                                             RepositorioLivrosTxt, RepositorioLojasTxt,
                                             RepositorioNotificacoesTxt,
                                             RepositorioPreferenciasTxt, criar_dados_iniciais)
from frameworks_drivers.relogio import RelogioDoSistema
from frameworks_drivers.web import criar_servidor_web
from use_cases import (AtualizarEstoque, BuscarLivros, CadastrarAvisoReposicao,
                       ConsultarDisponibilidade, DefinirLojaFavorita, ListarLojas,
                       ListarNotificacoes, ObterLojaFavorita, VerLoja)


def montar_casos_de_uso(pasta_dados):
    criar_dados_iniciais(pasta_dados)
    livros, lojas = RepositorioLivrosTxt(pasta_dados), RepositorioLojasTxt(pasta_dados)
    estoque, prefs = RepositorioEstoqueTxt(pasta_dados), RepositorioPreferenciasTxt(pasta_dados)
    avisos, notificacoes = RepositorioAvisosTxt(pasta_dados), RepositorioNotificacoesTxt(pasta_dados)
    return {
        "buscar_livros": BuscarLivros(livros),
        "consultar_disponibilidade": ConsultarDisponibilidade(livros, lojas, estoque, prefs),
        "listar_lojas": ListarLojas(lojas),
        "ver_loja": VerLoja(lojas),
        "definir_loja_favorita": DefinirLojaFavorita(lojas, prefs),
        "obter_loja_favorita": ObterLojaFavorita(prefs),
        "cadastrar_aviso": CadastrarAvisoReposicao(livros, lojas, estoque, avisos),
        "atualizar_estoque": AtualizarEstoque(livros, lojas, estoque, avisos, notificacoes,
                                              RelogioDoSistema()),
        "listar_notificacoes": ListarNotificacoes(notificacoes),
    }


def create_app(pasta_dados=None):
    pasta_dados = pasta_dados or os.environ.get("PASTA_DADOS", "data")
    return criar_servidor_web(montar_casos_de_uso(pasta_dados))


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000, debug=True)
