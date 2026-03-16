def serializar_jogo(jogo):
    if jogo:
        jogo["_id"] = str(jogo["_id"])
    return jogo