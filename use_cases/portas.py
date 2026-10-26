"""Portas de saída (DIP): os casos de uso dependem destas abstrações, e não de TXT,
banco de dados ou qualquer tecnologia. Quem implementa fica no círculo mais externo."""
from abc import ABC, abstractmethod


class RepositorioLivros(ABC):
    @abstractmethod
    def listar(self): ...

    @abstractmethod
    def buscar_por_isbn(self, isbn): ...


class RepositorioLojas(ABC):
    @abstractmethod
    def listar(self): ...

    @abstractmethod
    def buscar_por_id(self, loja_id): ...


class RepositorioEstoque(ABC):
    @abstractmethod
    def do_livro(self, isbn):
        """Lista de ItemEstoque das lojas que trabalham com o livro."""

    @abstractmethod
    def buscar(self, isbn, loja_id): ...

    @abstractmethod
    def salvar(self, item): ...


class RepositorioPreferencias(ABC):
    @abstractmethod
    def loja_favorita(self, cliente_id): ...

    @abstractmethod
    def definir_loja_favorita(self, cliente_id, loja_id): ...


class RepositorioAvisos(ABC):
    @abstractmethod
    def existe(self, aviso): ...

    @abstractmethod
    def salvar(self, aviso): ...

    @abstractmethod
    def pendentes(self, isbn, loja_id): ...

    @abstractmethod
    def remover(self, aviso): ...


class RepositorioNotificacoes(ABC):
    @abstractmethod
    def salvar(self, notificacao): ...

    @abstractmethod
    def do_cliente(self, cliente_id): ...


class Relogio(ABC):
    @abstractmethod
    def agora(self): ...
