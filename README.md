# Livraria – Clean Architecture

Evolução do MVP da livraria (repositório MVC do exercício 7.2) para **Clean Architecture**,
com persistência em **arquivos TXT**, aplicação do **DIP** e uma **nova feature: aviso de
reposição de estoque**.

## Círculos

```
Frameworks & Drivers   →  frameworks_drivers/  (Flask, templates, arquivos TXT, relógio)
  Interface Adapters   →  interface_adapters/  (controllers e presenters)
    Use Cases          →  use_cases/           (casos de uso + portas/interfaces)
      Entities         →  entities/            (Livro, Loja, ItemEstoque, AvisoReposicao, Notificacao)
```

`app.py` é o *main*: o único lugar que conhece todos os círculos. Ele cria os repositórios
TXT e os injeta nos casos de uso.

**Regra da dependência:** o código só aponta para dentro. `entities` não importa nada;
`use_cases` importa apenas `entities`. Isso é verificado em `tests/test_arquitetura.py`, que
também garante que o núcleo não usa Flask, `os`, `pathlib` nem nenhum recurso de arquivo.

## DIP – Princípio da Inversão de Dependência

Os casos de uso dependem de **abstrações** (`use_cases/portas.py`, por exemplo
`RepositorioEstoque`), e não de TXT. Quem implementa as portas está no círculo externo:

| Porta (núcleo) | Implementação TXT | Arquivo |
|---|---|---|
| `RepositorioLivros` | `RepositorioLivrosTxt` | `data/livros.txt` |
| `RepositorioLojas` | `RepositorioLojasTxt` | `data/lojas.txt` |
| `RepositorioEstoque` | `RepositorioEstoqueTxt` | `data/estoque.txt` |
| `RepositorioPreferencias` | `RepositorioPreferenciasTxt` | `data/preferencias.txt` |
| `RepositorioAvisos` | `RepositorioAvisosTxt` | `data/avisos.txt` |
| `RepositorioNotificacoes` | `RepositorioNotificacoesTxt` | `data/notificacoes.txt` |

Prova da independência: em `tests/test_use_cases.py` os mesmos casos de uso rodam com
repositórios em memória (`tests/fakes.py`), sem nenhum arquivo. Para trocar TXT por um
banco de dados, basta escrever novas classes que implementem as portas e mudar o `app.py`.

Formato dos arquivos: uma linha por registro, campos separados por `|`.

```
9788535902775|paulista|3
9788535902775|pinheiros|0
```

## Funcionalidades

- Consultar o estoque do livro em cada loja (MVP)
- Ver o preço praticado (MVP)
- Ver horário e endereço das lojas (MVP)
- Escolher loja favorita, salva em TXT e exibida primeiro (MVP)
- **Nova:** pedir aviso quando um livro esgotado voltar ao estoque; ao repor o estoque,
  o cliente recebe uma notificação e o aviso é encerrado

## Como rodar

```bash
pip install -r requirements.txt
pytest -v        # testes de cada círculo + persistência TXT + arquitetura
python app.py    # http://localhost:5000 (os dados ficam na pasta data/)
```

Para testar a nova feature: abra **Dom Casmurro**, toque em **Avisar quando chegar** na
Livraria Pinheiros, vá em **Repor estoque**, coloque 4 exemplares nessa loja e abra
**Notificações**.
