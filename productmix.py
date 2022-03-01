
def limpiar(lista):
    """
    Está función limpia los caracteres especiales y convierte los str a int
    """
    aux = lista.pop()
    if len(aux) != 1:
        aux = aux[:-1]
    lista.append(aux)
    list_aux = []
    for i in range(len(lista)):
        if i == 0:
            list_aux.append(lista[i])
        else:
            list_aux.append(int(lista[i]))
    return list_aux

class ProductMix:
    def __init__(self, filename):
        file1 = open(filename, 'r')
        lines = [limpiar(e.split(' ')) for e in file1.readlines()]
        self.valor_panel = lines[0]
        self.restrictions = lines[1:-1]
        self.mayor = lines[5]
        self.size = 4
        self.low = 15
        self.high = 30
        self.tweak = 5

    def evaluate(self, cells):
        fitness = 0
        for i in range(len(cells)):
          fitness += cells[i] * self.valor_panel[i+1]
        return fitness

    def check_restrictions(self, cells):
      for restriction in self.restrictions:
        suma = 0
        for i in range(len(cells)):
          suma += cells[i] * restriction[i+2]
        if suma > restriction[1]:
          return False
      return True