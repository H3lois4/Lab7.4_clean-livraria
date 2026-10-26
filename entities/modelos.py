import unicodedata
from dataclasses import dataclass
from datetime import datetime

from .excecoes import ErroDeNegocio


def normalizar(texto):
    sem_acentos = unicodedata.normalize("NFKD", texto or "")
    return "".join(c for c in sem_acentos if not unicodedata.combining(c)).casefold().strip()


@dataclass(frozen=True)
class Loja:
    id: str
    nome: str
    endereco: str
    horario: str


@dataclass(frozen=True)
class Livro:
    isbn: str
    titulo: str
    autor: str
    preco: float

    def corresponde(self, termo):
        """Busca por trecho do título ou do autor, sem diferenciar maiúsculas e acentos."""
        termo = normalizar(termo)
        return termo in normalizar(self.titulo) or termo in normalizar(self.autor)


@dataclass(frozen=True)
class ItemEstoque:
    isbn: str
    loja_id: str
    quantidade: int

    def __post_init__(self):
        if self.quantidade < 0:
            raise ErroDeNegocio("Quantidade inválida")

    @property
    def disponivel(self):
        return self.quantidade > 0

    def com_quantidade(self, nova):
        return ItemEstoque(self.isbn, self.loja_id, nova)

    def voltou_ao_estoque(self, nova):
        """Regra da feature: houve reposição quando sai de zero para mais de zero."""
        return self.quantidade == 0 and nova > 0


@dataclass(frozen=True)
class AvisoReposicao:
    cliente_id: str
    isbn: str
    loja_id: str

    @staticmethod
    def pode_ser_criado(item_estoque):
        if item_estoque.disponivel:
            raise ErroDeNegocio("O livro está disponível nesta loja")


@dataclass(frozen=True)
class Notificacao:
    cliente_id: str
    criada_em: datetime
    mensagem: str

    @classmethod
    def de_reposicao(cls, aviso, livro, loja, agora):
        return cls(aviso.cliente_id, agora,
                   f"O livro {livro.titulo} voltou ao estoque na {loja.nome}.")
