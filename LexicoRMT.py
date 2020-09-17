from Error import *
from Token import *
from tkinter import messagebox
import webbrowser
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
        self.aux = False #falso normal, true retroceder caracter
        self.tablaToken = ''
        self.tablaError = ''

    def analizarLexico(self, cadena):   
        cadena = cadena.lower() + '           '
        #command= messagebox.showinfo(message= cadena, title="Análisis RMT")
                 
        caracter = ''
        lim = len(cadena)
        for i in range(lim):

            caracter = cadena[i]
            if self.aux == True:
                caracter = cadena[i-1]
                lim+=1
            #command= messagebox.showinfo(message= "Estado " + str(self.estado) + '->' + caracter, title="Análisis RMT")
            #print(caracter)            
            
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
                    self.columna = self.columna + 1
                elif caracter.isdigit():
                    #command= messagebox.showinfo(message= "Estado 2 isdigit " + caracter + " Pos "+ str(i), title="Análisis RMT")
                    self.lexema = self.lexema + caracter
                    self.estado = 2
                    self.columna = self.columna + 1
                elif caracter == '_':
                    #command= messagebox.showinfo(message= "Estado 2_ " + caracter + " Pos "+ str(i), title="Análisis RMT")
                    self.lexema = self.lexema + caracter
                    self.estado = 2
                    self.columna = self.columna + 1
                else:                        
                    #command= messagebox.showinfo(message= "Aceptó " + caracter, title="Análisis RMT")
                    self.insertarToken('Identificador',self.lexema, self.fila, self.columna)
                    self.estado = 0
                    i = i-1
                    self.aux = True
                    self.columna = self.columna + 1

            elif self.estado == 3:
                if caracter.isdigit():
                    self.lexema = self.lexema + caracter
                    self.columna = self.columna + 1
                elif caracter == '.':
                    self.lexema = self.lexema + caracter
                    self.columna = self.columna + 1
                    estado = 4
                else:
                    self.insertarToken('Número',self.lexema, self.fila, self.columna)
                    self.columna = self.columna + 1
                    self.estado = 0
                    i = i-1
                    self.aux = True
            elif self.estado == 4:
                if caracter.isdigit():
                    self.lexema = self.lexema + caracter
                    self.columna = self.columna + 1
                    estado = 3
                else:
                    self.insertarToken('Número',self.lexema, self.fila, self.columna)
                    self.columna = self.columna + 1
                    self.estado = 0
                    i = i-1
                    self.aux = True
        self.imprimir()  
        self.sintactico()

 
    
    def insertarToken(self, tipo, lex, fila, columna):
        command= messagebox.showinfo(message= "Aceptó " + lex, title="Análisis RMT")
        self.tablaToken = self.tablaToken + "<TR><TD>"+tipo+"</TD><TD>"+lex+"</TD><TD>"+str(fila)+"</TD><TD>"+str(columna)+"</TD></TR>"
        token = Token(tipo, lex, 0, columna)
        self.listaTokens.append(token)
        print('Token ' + tipo +' '+ lex )
        self.lexema = ''
        #self.estado = 0        
    
    def insertarError(self, descripcion, fila, columna):  
        command= messagebox.showinfo(message= "Error " + descripcion, title="Análisis RMT")  
        self.tablaError = self.tablaError + "<TR><TD>"+descripcion+"</TD><TD>"+str(fila)+"</TD><TD>"+str(columna)+"</TD></TR>"
        error = Error(descripcion, fila, columna)
        print('Error ' + descripcion)
        self.listaErrores.append(error)
        self.lexema = ''
        #self.estado = 0
    
    def imprimir(self):
        tabla = "<HTML><HEAD></HEAD><BODY><H1>Reporte de Tokens</H1><TABLE border = \"1\"><font face=\"Arial\"><TR><TH>Tipo</TH><TH>Lexema</TH><TH>Fila</TH><TH>Columna</TH></TR>" + self.tablaToken + "</font></table><BR><BR><H1>Reporte de Errores Léxicos</H1><TABLE border = \"1\"><TR><TH>Descripción</TH><TH>Fila</TH><TH>Columna</TH></TR>" + self.tablaError + "</table></body></html>"
        rutaToken = "/home/vania/reporteRMT.html"
        archivoGuardado_=open(rutaToken, "w", encoding="utf-8")
        archivoGuardado_.write(tabla)
        archivoGuardado_.close() 
        self.tablaError = ''
        self.tablaToken = ''
        webbrowser.open_new_tab(rutaToken)

    def sintactico(self):
        command= messagebox.showinfo(message= "entro al analisis sintactico")
        for n in self.listaTokens:
            command= messagebox.showinfo(message= "token " + n.tipo)

 

            






    




        

        