"""Regra da dependência da Clean Architecture: o código só aponta para dentro."""
import ast
import pathlib

import pytest

RAIZ = pathlib.Path(__file__).resolve().parent.parent
CIRCULOS = ["entities", "use_cases", "interface_adapters", "frameworks_drivers"]
PERMITIDO = {
    "entities": set(),
    "use_cases": {"entities"},
    "interface_adapters": {"entities", "use_cases"},
    "frameworks_drivers": {"entities", "use_cases", "interface_adapters"},
}
TECNOLOGIAS = {"flask", "sqlite3", "pathlib", "os", "io", "open"}


def imports(pasta):
    nomes = set()
    for arquivo in (RAIZ / pasta).rglob("*.py"):
        for no in ast.walk(ast.parse(arquivo.read_text(encoding="utf-8"))):
            if isinstance(no, ast.Import):
                nomes |= {a.name.split(".")[0] for a in no.names}
            elif isinstance(no, ast.ImportFrom) and no.level == 0 and no.module:
                nomes.add(no.module.split(".")[0])
    return nomes


@pytest.mark.parametrize("circulo", CIRCULOS)
def test_dependencias_apontam_para_dentro(circulo):
    assert (imports(circulo) & set(CIRCULOS)) - {circulo} <= PERMITIDO[circulo]


@pytest.mark.parametrize("circulo", ["entities", "use_cases"])
def test_nucleo_independente_de_tecnologia(circulo):
    assert not imports(circulo) & TECNOLOGIAS
