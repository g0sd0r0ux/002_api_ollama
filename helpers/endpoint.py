from typing import List

class Endpoint:
    """
    Clase que representa un endpoint en una API.
    Contiene la ruta y los métodos HTTP permitidos.
    """
    def __init__(self, route: str = '/default', methods: List[str] = None):
        """
        Constructor de la clase Endpoint.

        :param route: Ruta del endpoint (por defecto: '/default').
        :param methods: Lista de métodos HTTP permitidos (por defecto: ['GET']).
        """
        self.route = route
        self.methods = methods if methods is not None else ['GET']

    @staticmethod
    def isList(value) -> bool:
        """
        Verifica si un valor es una lista.

        :param value: Valor a verificar.
        :return: True si es una lista, False en caso contrario.
        """
        return isinstance(value, list)

    def info(self) -> None:
        """
        Muestra información sobre el endpoint en la terminal.
        """
        print(f'----- INFO ENDPOINT -----\nRuta: {self.route}\nMétodos: {self.methods}')