from Error import *
from Token import *
from tkinter import messagebox
class LexicoRMT:
    
    def __init__(self):
        self.longitud = 0
        self.listaSignos = ['+', '-', '/', '*', '(', ')']  
        self.listaTokens = []
        self.listaErrores = []
        self.lexema = ''
        self.fila = 0
        self.columna = 0
        self.estado = 0
        self.aux = False #falso
        self.tablaToken = ''

    def analizarLexico(self, cadena):   
        cadena = cadena + ' '
        #command= messagebox.showinfo(message= cadena, title="Análisis RMT")
                 
        caracter = ''
        for i in range(len(cadena)):
            caracter = cadena[i]
            #command= messagebox.showinfo(message= "Estado " + str(self.estado) + '->' + caracter, title="Análisis RMT")
            print(caracter)            
            
            if self.estado == 0:
                if caracter == '\n':
                    self.fila = self.fila + 1
                    self.columna = 0
                    self.estado = 0
                elif caracter == '\t':
                    self.columna = self.columna + 1
                    self.columna = 0
                    self.estado = 0
                elif caracter == '\r':
                    self.columna = self.columna + 1
                    self.columna = 0
                    self.estado = 0
                elif caracter.isspace():
                    self.columna = self.columna + 1
                    self.estado = 0
                elif caracter in self.listaSignos:
                    self.insertarToken('Signo' + caracter, caracter, self.fila, self.columna) 
                    self.estado = 0
                    self.columna = self.columna + 1                   
                elif caracter.isalpha():
                    self.lexema = self.lexema + caracter
                    self.estado = 2
                    self.columna = self.columna + 1
                elif caracter.isdigit():
                    self.lexema = caracter
                    self.estado = 3
                    self.columna = self.columna + 1
                else:
                    self.insertarError('El caracter '+  caracter + ' no pertenece al lenguaje', self.fila, self.columna)
                    self.columna = self.columna + 1
                    self.estado = 0
                    
            elif self.estado == 2:
                    
                if caracter.isalpha():
                    #command= messagebox.showinfo(message= "Estado 2 isalpha " + caracter + " Pos "+ str(i), title="Análisis RMT")
                    self.lexema = self.lexema + caracter
                    self.estado = 2
                elif caracter.isdigit():
                    #command= messagebox.showinfo(message= "Estado 2 isdigit " + caracter + " Pos "+ str(i), title="Análisis RMT")
                    self.lexema = self.lexema + caracter
                    self.estado = 2
                elif caracter == '_':
                    #command= messagebox.showinfo(message= "Estado 2_ " + caracter + " Pos "+ str(i), title="Análisis RMT")
                    self.lexema = self.lexema + caracter
                    self.estado = 2
                else:                        
                    #command= messagebox.showinfo(message= "Aceptó " + caracter, title="Análisis RMT")
                    self.insertarToken('Identificador',self.lexema, self.fila, self.columna)
                    self.estado = 0
                    i = i-1

            elif self.estado == 3:
                if caracter.isdigit():
                    self.lexema = self.lexema + caracter
                elif caracter == '.':
                    self.lexema = self.lexema + caracter
                    estado = 4
                else:
                    self.insertarToken('Número',self.lexema, self.fila, self.columna)
                    self.estado = 0
                    i = i-1
            elif self.estado == 4:
                if caracter.isdigit():
                    self.lexema = self.lexema + caracter
                    estado = 3
                else:
                    self.insertarToken('Número',self.lexema, self.fila, self.columna)
                    self.estado = 0
                    i = i-1

        #self.imprimirListaTokens()
        rutaToken = "/home/vania/holis.html"
        archivoGuardado_=open(rutaToken, "w", encoding="utf-8")
        tabla = "<HTML><HEAD></HEAD><BODY><TABLE><TR><TH>Tipo</TH><TH>Lexema</TH></TR>" + self.tablaToken + "</table></body></html>"
        
        archivoGuardado_.write(tabla)
        archivoGuardado_.close() 
        #webbrowser.open_new_tab(rutaToken)
        #self.imprimirListaErrores()             
 
    
    def insertarToken(self, tipo, lex, fila, columna):
        command= messagebox.showinfo(message= "Aceptó " + lex, title="Análisis RMT")
        self.tablaToken = self.tablaToken + "<TR><TD>"+tipo+"</TD><TD>"+lex+"</TD></TR>"
        token = Token(tipo, lex, 0, columna)
        self.listaTokens.append(token)
        print('Token ' + tipo +' '+ lex )
        self.lexema = ''
        #self.estado = 0

        
    
    def insertarError(self, descripcion, fila, columna):  
        command= messagebox.showinfo(message= "Error " + descripcion, title="Análisis RMT")      
        error = Error(descripcion, fila, columna)
        print('Error ' + descripcion)
        self.listaErrores.append(error)
        self.lexema = ''
        #self.estado = 0
    
    def imprimirListaTokens(self):
        tabla = "<HTML><HEAD></HEAD><BODY><TABLE><TR><TH>Tipo</TH><TH>self.lexema</TH></TR>" + self.tablaToken + "</table></body></html>"
        
    
    def imprimirListaErrores(self):

        for error in self.listaErrores:
            print(error)
            






    




        

        