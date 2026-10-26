from entities import NaoEncontrado
from entities.modelos import normalizar


def obter_livro(repo_livros, isbn):
    livro = repo_livros.buscar_por_isbn(isbn)
    if livro is None:
        raise NaoEncontrado("Livro não encontrado")
    return livro


def obter_loja(repo_lojas, loja_id):
    loja = repo_lojas.buscar_por_id(loja_id)
    if loja is None:
        raise NaoEncontrado("Loja não encontrada")
    return loja


class BuscarLivros:
    def __init__(self, repo_livros):
        self._livros = repo_livros

    def executar(self, termo=""):
        livros = [l for l in self._livros.listar() if l.corresponde(termo)]
        return sorted(livros, key=lambda l: normalizar(l.titulo))


class ListarLojas:
    def __init__(self, repo_lojas):
        self._lojas = repo_lojas

    def executar(self):
        return sorted(self._lojas.listar(), key=lambda l: l.nome)


class VerLoja:
    def __init__(self, repo_lojas):
        self._lojas = repo_lojas

    def executar(self, loja_id):
        return obter_loja(self._lojas, loja_id)


class ConsultarDisponibilidade:
    """Estoque e preço do livro em cada loja; a loja favorita do cliente vem primeiro."""

    def __init__(self, repo_livros, repo_lojas, repo_estoque, repo_preferencias):
        self._livros, self._lojas = repo_livros, repo_lojas
        self._estoque, self._prefs = repo_estoque, repo_preferencias

    def executar(self, isbn, cliente_id=None):
        livro = obter_livro(self._livros, isbn)
        favorita = self._prefs.loja_favorita(cliente_id) if cliente_id else None
        itens = []
        for item in self._estoque.do_livro(isbn):
            loja = self._lojas.buscar_por_id(item.loja_id)
            if loja:
                itens.append({"loja": loja, "estoque": item, "favorita": loja.id == favorita})
        itens.sort(key=lambda i: (not i["favorita"], i["loja"].nome))
        return livro, itens
