class ErroDeNegocio(Exception):
    """Violação de uma regra de negócio."""


class NaoEncontrado(ErroDeNegocio):
    """Livro, loja ou registro inexistente."""
