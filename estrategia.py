from tipos import  Domino, Jogada, Pecas, Peca




def cola_pedra_maior(domino: Domino) -> Jogada | dict:
    esquerda = domino.mesa[0].get_lado('esquerda')
    direita = domino.mesa[-1].get_lado('direita')

    def _get_peca_maior(mao: Pecas, valor: int) -> Peca | None:
        maior = -1
        for peca in mao.filter(valor):
            if peca > maior:
                maior = peca
        return maior if not maior == -1 else None
    
    p_esq = _get_peca_maior(domino.mao, esquerda)
    p_dir = _get_peca_maior(domino.mao, direita)
    esq = p_esq is not None
    dir = p_dir is not None

    if esq and dir:
        if p_esq > p_dir:
            return Jogada(p_esq, 'esquerda', domino.jogador)
        else:
            return Jogada(p_dir, 'direita', domino.jogador)    
    else:
        if esq:
            return Jogada(domino.mao[0], 'esquerda', domino.jogador)
        elif dir:
            return Jogada(domino.mao[-1], 'direita', domino.jogador)
        else:
            return {}