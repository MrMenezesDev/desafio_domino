from json import load
from typing import List, Dict
from enum import Enum

class NomePeca(Enum):
    sena = 6
    quina = 5
    quadra = 4
    terno = 3
    duque = 2
    ás = 1
    branco = 0

class Lado(Enum):
    esquerda = 'esquerda'
    direita = 'direita'

class Peca:
    peca: List[int]
    def __init__(self, peca: str):
        self.peca = list(map(int, peca.split("-")))
        self.order = self.peca[0] > self.peca[-1]
        self.peca.sort()
        self.isBucha = self.peca[0] == self.peca[-1]

    def get_lado(self, lado: Lado) -> int:
        if lado == Lado.esquerda:
            return self.peca[0] if self.order else self.peca[-1]
        return self.peca[-1] if self.order else self.peca[0]

    def __str__(self):
        p1, p2 = self.peca[::-1] if self.order else self.peca
        if self.isBucha:
            return "Bucha de " + NomePeca(p1).name
        return NomePeca(p1).name.capitalize() + " de " + NomePeca(p2).name

    def __eq__(self, other):
        if isinstance(other, int):
            return other in self.peca
        return self.peca == other.peca
    
    def __lt__(self, other):
        if isinstance(other, int):
            return sum(self) < other
        return sum(self.peca) < sum(other.peca)
    
    def __gt__(self, other):
        if isinstance(other, int):
            return sum(self) > other
        return sum(self.peca) > sum(other.peca)
    
    def __le__(self, other):
        if isinstance(other, int):
            return sum(self) <= other
        return sum(self.peca) <= sum(other.peca)
    
    def __ge__(self, other):
        if isinstance(other, int):
            return sum(self) >= other
        return sum(self.peca) >= sum(other.peca)
    
    def __ne__(self, other):
        if isinstance(other, int):
            return sum(self) != other
        return sum(self.peca) != sum(other.peca)
    
    def get_str(self):
        return f"{self.peca[0]}-{self.peca[1]}"
    
    def get_ascii(self):
        p1, p2 = self.peca[::-1] if self.order else self.peca
        char_value = 0x1F031 
        if self.isBucha:
            return chr(char_value + p1 + (p1 * 7) + 50)
        else:
            return chr(char_value + p2 + (p1 * 7) )

    def __iter__(self):
        return iter(self.peca)

    def __add__(self, other):
        if isinstance(other, int):
            return sum(self) + other
        if not isinstance(other, Peca):
            raise TypeError("Operação não suportada")
        return sum(self.peca) + sum(other)
    
    def __radd__(self, other):
        return self.__add__(other)

class Pecas:
    def __init__(self, pecas: List[str]) -> None:
        self.pecas = list(map(Peca, pecas))

    def __str__(self) -> str:
        printar = ''
        for peca in self.pecas:
            printar +=  peca.get_ascii() + '\u200A'
        return printar
    
    def __len__(self) -> int:
        return len(self.pecas)
    
    def __getitem__(self, item):
        return self.pecas[item]
    
    def __setitem__(self, key, value):
        self.pecas[key] = value

    def __delitem__(self, key):
        del self.pecas[key]

    def __iter__(self):
        return iter(self.pecas)
    
    def __reversed__(self):
        return reversed(self.pecas)
    
    def __contains__(self, item):
        return item in self.pecas

    def __iter__(self):
        return iter(self.pecas)
    
    def filter(self, valor: int):
        return [peca for peca in self.pecas if valor in peca]

class Jogada:
    peca: Peca
    lado: Lado | None
    jogador: int

    def __init__(self, peca: Peca, lado: str, jogador: int):
        self.peca = peca
        self.lado = lado
        self.jogador = jogador

    def to_dict(self) -> Dict[str, str]:
        return {
            'pedra': self.peca.get_str(),
            'lado': self.lado,
        }

class Domino:
    jogador: int
    mao: Pecas
    mesa: Pecas
    jogadas: List[Jogada]

    def __init__(self, jogador: int, mao: List[Peca], mesa: List[Peca], jogadas: List[Dict[str, str]]):
        self.jogador = jogador
        self.mao = mao
        self.mesa = mesa
        self.jogadas = jogadas

    @classmethod
    def from_json(cls, json_str: str |dict) -> 'Domino':
        if isinstance(json_str, dict):
            data = json_str
        else:
            data = load(json_str)
        jogador = data['jogador']
        mao = Pecas(data['mao'])
        mesa = Pecas(data['mesa'])
        jogadas = []
        for jogada in data['jogadas']:
            peca = Peca(jogada['pedra'])
            lado = Lado(jogada['lado']) if 'lado' in jogada else None
            jogadas.append(Jogada(peca, lado, jogada['jogador']))
        return cls(jogador, mao, mesa, jogadas)
