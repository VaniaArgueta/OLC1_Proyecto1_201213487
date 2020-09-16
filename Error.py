class Error:
    def __init__(self, descripcion, fila, columna ):
        self.tipo = 'Léxico'
        self.descripcion = descripcion
        self.fila = fila
        self.columna = columna  
