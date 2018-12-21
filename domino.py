import random

from pprint import pprint
from copy import deepcopy

# TODO: Pasar información del juego a todos los jugadores
# TODO: Unittest

class Domino:
    """
    Instancia para jugar una partida de domino en parejas.
    Usualmente hay dos configuraciones con las que se juega.

    Doble 6:
        FICHA_MAXIMA = 6
        FICHAS_POR_JUGADOR = 7

    Doble 9:
        FICHA_MAXIMA = 9
        FICHAS_POR_JUGADOR = 10
    """

    FICHA_MAXIMA = 6
    FICHAS_POR_JUGADOR = 7

    def __init__(self):
        self.logs = []
        self.jugadores = None

        # Iniciar las fichas
        self.fichas = []
        for i in range(Domino.FICHA_MAXIMA + 1):
            for j in range(i + 1):
                self.fichas.append((i, j))

        self.cabezas = [-1, -1]
        self.puntos_finales = None

    def log(self, *data):
        """
            ("nuevo juego",)
            ("no lleva", puesto)
            ("salida", puesto, jugada, cabeza)
            ("jugada", puesto, jugada, cabeza)
            ("se pego", puesto)
            ("se tranco",)
            ("gano", equipo)

            puesto: [0, 1, 2, 3]
            equipo: [0, 1]
            jugada: (A, B)
                A: [0 .. FICHA_MAXIMA]
                B: [0 .. FICHA_MAXIMA]
            cabeza: [0, 1]
        """
        self.logs.append(data)
        for jugador in self.jugadores:
            jugador.log(deepcopy(data))

    def start(self, jugadores):
        self.logs.clear()

        # Inicializar mesa
        self.jugadores = jugadores
        for puesto, jugador in enumerate(self.jugadores):
            jugador.empieza_partida(puesto)

        self.cabezas = [-1, -1]
        self.log("nuevo juego")

        # Repartiendo las fichas
        random.shuffle(self.fichas)
        for i in range(Domino.FICHAS_POR_JUGADOR):
            for jugador in self.jugadores:
                jugador.repartiendo(self.fichas.pop(0))

        # Ejectuando el juego
        while True:
            se_tranco = True

            for puesto, jugador in enumerate(self.jugadores):
                # print(jugador.nombre)
                accion = jugador.jugar(self.cabezas)

                if not accion:
                    # El jugador no lleva ficha
                    self.log('no lleva', puesto)
                    continue

                se_tranco = False
                jugada, cabeza = accion

                if -1 in self.cabezas:
                    # Primera jugada de la partida
                    self.cabezas = list(jugada)
                    self.log('salida', puesto, jugada, cabeza)

                else:
                    assert self.cabezas[cabeza] in jugada

                    if jugada[0] == self.cabezas[cabeza]:
                        self.cabezas[cabeza] = jugada[1]
                    else:
                        self.cabezas[cabeza] = jugada[0]

                    self.log('jugada', puesto, jugada, cabeza)

                if len(jugador.fichas) == 0:
                    self.log('se pego', puesto)
                    self.log('gano', puesto % 2)

                    self.puntos_finales = [
                        jugador.sum() for jugador in self.jugadores
                    ]

                    return

            if se_tranco:
                self.log('se tranco')

                self.puntos_finales = [
                    jugador.sum() for jugador in self.jugadores
                ]

                equipo0 = min(self.puntos_finales[0], self.puntos_finales[2])
                equipo1 = min(self.puntos_finales[1], self.puntos_finales[3])

                if equipo0 < equipo1:
                    self.log('gano', 0)
                elif equipo1 < equipo0:
                    self.log('gano', 1)
                else:
                    self.log('empate')

                return

class JuegoSimple:
    """
    Se juega una sola partida. Si hay tablas gana el segundo jugador
    """

    def start(self, jugador0, jugador1):
        """
            Devuelve True si gano el jugador0 y False en caso contrario.
            Si la partida queda empate cuenta como victoria para el jugador1
        """
        jugadores = [jugador0(), jugador1(), jugador0(), jugador1()]
        domino = Domino()
        domino.start(jugadores)

        resultado = domino.logs[-1]
        # pprint(domino.logs)

        if resultado[0] == 'gano':
            return resultado[1] == 0
        return False

if __name__ == '__main__':
    from jugador import BotaGorda, Aleatorio, Cantidad
    from jugador_inteligente import Inteligente
    from jugador_flat import Flat
    from jugador_repr import Representative

    from functools import partial
    import json
    import numpy as np

    # Ejecuta un torneo todo contra todos entre varios jugadores
    # Para determinar la calidad de cada jugador.
    jugadores = [
        partial(BotaGorda, "1"),
        partial(Aleatorio, "2"),
        partial(Cantidad, "3"),
        partial(Inteligente, "4.1", [0.36761, 0.07985, 0.06829, 0.61909, 0.15015, 0.94147]),
        partial(Inteligente, "4.2", [0.50319, 0.89254, 0.05187, 0.42541, 0.19633, 0.92883]),
        partial(Inteligente, "4.3", [0.50329, 0.89258, 0.05183, 0.42549, 0.19591, 0.92901]),
        partial(Inteligente, "4.4", [0.613, 0.075, 0.171, 0.562, 0.007, 2.127]),
    ]

    # # Load Flat player
    # with open('flat.json') as f:
    #     data = json.load(f)
    # jugadores.append(partial(Flat, "5", data[-1][0]))

    # Load Repr player
    coef = np.random.randn(36)
    jugadores.append(partial(Representative, "R", coef))

    juego = JuegoSimple()

    total = 100

    for ix, jugador0 in enumerate(jugadores):
        for iy, jugador1 in enumerate(jugadores):
            win = 0
            for _ in range(total):
                win += int(juego.start(jugador0, jugador1))

            print(f"{jugador0().nombre} {win} - {total - win} {jugador1().nombre}")
