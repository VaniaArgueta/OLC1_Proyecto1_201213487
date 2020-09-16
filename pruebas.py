def estado0(self,caracter):
        if caracter in self.listaSignos:
            print('Signo ' + caracter)
            self.lexema = self.lexema + caracter
            self.estado = 1
        elif caracter.isalpha():
            print('Letra ' + caracter)
            self.lexema = self.lexema + caracter
            self.estado = 2
        elif caracter.isdigit():
            print('Digito '+  caracter)
            self.lexema = self.lexema + caracter
            self.estado = 3
        elif caracter.isspace():
            self.lexema = ''
            self.estado = 0
        else:
            self.estado = -1
    
    def estado1(self,caracter):
        self.insertarToken('Signo ' + self.lexema, self.lexema, self.fila, self.columna)
        self.estado = 0
        if self.aux == True:
            self.estado0(caracter)

    
    def estado2(self,caracter):
        if caracter.isalpha() or caracter.isdigit() or caracter == '_':
            self.lexema = self.lexema + caracter
            self.estado = 2
        elif caracter in self.listaSignos:
            self.insertarToken('ID', self.lexema, self.fila, self.columna)
            self.lexema = self.lexema + caracter #aquí comienza un nuevo lexema
            self.aux = False
            self.estado1(caracter)
        else:
            self.insertarToken('ID', self.lexema, self.fila, self.columna)
            self.insertarError('El caracter ' + caracter + ' no pertenece al lenguaje.',self.fila, self.columna)
            self.estado = 0
    
    def estado3(self, caracter):
        if caracter.isdigit():
            self.lexema = self.lexema + caracter
            self.estado = 3
        elif caracter == '.':
            self.lexema = self.lexema + caracter
            self.estado = 4
        elif caracter in self.listaSignos:
            self.insertarToken('Numero', self.lexema, self.fila, self.columna)
            self.aux = False
            self.estado1(caracter)
        elif caracter.isalpha():
            self.insertarToken('Numero', self.lexema, self.fila, self.columna)
            self.aux = False
            self.estado2(caracter)
        else:
            self.insertarToken('Numero', self.lexema, self.fila, self.columna)
            self.insertarError('El caracter ' + caracter + ' no pertenece al lenguaje.',self.fila, self.columna)
            self.estado = 0
        
    def estado4(self,caracter):
        if caracter.isdigit():
            self.lexema = self.lexema + caracter
            self.estado = 3
        else:
            insertarError('No se reconoce el lexema ' + self.lexema, self.fila, self.columna)
            self.estado = 0
        

