
# Creación de clase 'Endpoint'
class Endpoint:

    # Método constructor
    def __init__(self, route: str = '/default', methods: list = None) :
        self.route = route
        self.methods = methods if methods is not None else ['GET']

    @staticmethod
    def isList(value) -> bool :
        return isinstance(value, list)

    # Métodos propios de la clase
    def info(self) -> None :
        print(f'----- INFO ENDPOINT -----\nRuta: {self.route}\nMétodos: {self.methods}')
