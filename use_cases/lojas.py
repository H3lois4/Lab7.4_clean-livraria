from .catalogo import obter_loja


class DefinirLojaFavorita:
    def __init__(self, repo_lojas, repo_preferencias):
        self._lojas, self._prefs = repo_lojas, repo_preferencias

    def executar(self, cliente_id, loja_id):
        loja = obter_loja(self._lojas, loja_id)
        self._prefs.definir_loja_favorita(cliente_id, loja.id)
        return loja


class ObterLojaFavorita:
    def __init__(self, repo_preferencias):
        self._prefs = repo_preferencias

    def executar(self, cliente_id):
        return self._prefs.loja_favorita(cliente_id)
