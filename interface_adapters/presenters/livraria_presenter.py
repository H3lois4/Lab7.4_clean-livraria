"""Transforma entidades em dados prontos para a tela (view models)."""


def moeda(valor):
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def apresentar_livro(livro):
    return {"isbn": livro.isbn, "titulo": livro.titulo, "autor": livro.autor,
            "preco": moeda(livro.preco)}


def apresentar_loja(loja, favorita=None):
    return {"id": loja.id, "nome": loja.nome, "endereco": loja.endereco,
            "horario": loja.horario, "favorita": loja.id == favorita}


def apresentar_disponibilidade(itens):
    return [{
        "loja_id": i["loja"].id,
        "nome": i["loja"].nome,
        "endereco": i["loja"].endereco,
        "quantidade": i["estoque"].quantidade,
        "disponivel": i["estoque"].disponivel,
        "favorita": i["favorita"],
    } for i in itens]


def apresentar_notificacao(n):
    return {"mensagem": n.mensagem, "data": n.criada_em.strftime("%d/%m/%Y %H:%M")}
