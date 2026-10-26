"""Driver de baixo nível: cada linha do arquivo é um registro, campos separados por '|'."""
from pathlib import Path

SEPARADOR = "|"


class ArquivoTxt:
    def __init__(self, caminho):
        self.caminho = Path(caminho)

    def ler(self):
        if not self.caminho.exists():
            return []
        linhas = self.caminho.read_text(encoding="utf-8").splitlines()
        return [linha.split(SEPARADOR) for linha in linhas if linha.strip()]

    def gravar(self, registros):
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        texto = "\n".join(
            SEPARADOR.join(str(campo).replace(SEPARADOR, "/").replace("\n", " ") for campo in r)
            for r in registros
        )
        self.caminho.write_text(texto + ("\n" if registros else ""), encoding="utf-8")

    def acrescentar(self, registro):
        self.gravar(self.ler() + [registro])
