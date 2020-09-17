from Error import *
from Token import *
from tkinter import messagebox
import webbrowser

class LexicoCSS:
    def __init__(self):
        self.longitud = 0
        self.listaSignos = ['{','}',':',';','#','.',',','%']  
        self.listaReservadas = ['color', 'border','text-align','font-weight','padding-left','padding-top','line-height','margin-top', 'margin-left', 'display','top','float','min-width','background-color','opacity','font-family','font-size','padding-right','padding','width','margin-right','margin','position','right','clear','max-height','background-image','background','font-style','font','padding-bottom','display','height','margin-bottom','border-style','bottom','left','max-width','min-height']
        self.listaTokens = []
        self.listaErrores = []
        self.lexema = ''
        self.fila = 0
        self.columna = 0
        self.estado = 0
        self.aux = False #falso normal, true retroceder caracter
        self.tablaToken = ''
        self.tablaError = ''
        self.resultadoCadena = ''
        self.resultadoToken = ''
        self.resultadoError = ''
        self.resultadoReporte = ''

    def analizar(self, cadena, estado):
        #command= messagebox.showinfo(message= cadena, title="Análisis CSS")
        cadena = cadena.lower() + '  '
        self.estado = 0
        caracter = ''
        lim = len(cadena)
        for i in range(lim):
            caracter = cadena[i]
            #command= messagebox.showinfo(message= "Estado->" + str(self.estado) + ' Pos->' + str(i)+ "->"+ caracter, title="Análisis HTML")
            self.resultadoReporte += "Estado->" + str(self.estado) + "Caracter->" + str(caracter)+"\n"
            if self.aux == True:
                caracter = cadena[i-1]
                lim+=1
                self.aux == False
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
                    self.lexema = caracter
                    self.insertarToken('Signo' + caracter, self.lexema, self.fila, self.columna) 
                    self.estado = 0
                    self.columna = self.columna + 1   
                elif caracter == '/':
                    self.lexema = self.lexema + caracter
                    self.estado = 1
                    self.columna = self.columna + 1           
                elif caracter.isalpha():
                    self.lexema = self.lexema + caracter
                    self.estado = 9
                    self.columna = self.columna + 1
                elif caracter.isdigit():
                    self.lexema = caracter
                    self.estado = 7
                    self.columna = self.columna + 1
                elif caracter == '"':
                    self.lexema = caracter
                    self.estado = 5
                    self.columna = self.columna + 1
                else:
                    self.insertarError('El caracter '+  caracter + ' no pertenece al lenguaje', self.fila, self.columna)
                    self.columna = self.columna + 1
                    self.estado = 0
            elif self.estado==1:
                if caracter == '*':
                    self.lexema = self.lexema + caracter
                    self.estado = 2
                    self.columna = self.columna + 1
                else:
                    self.insertarError('El caracter / no pertenece al lenguaje', self.fila, self.columna)
                    self.columna = self.columna + 1
                    self.estado = 0
                    i = i-1
                    self.aux = True
            elif self.estado ==2:
                if caracter == '*':
                    self.lexema = self.lexema + caracter
                    self.estado = 3
                    self.columna = self.columna + 1
                else:
                    self.lexema = self.lexema + caracter
                    self.estado = 2
                    self.columna = self.columna + 1
            elif self.estado == 3:
                if caracter == '/':
                    self.lexema = self.lexema + caracter
                    self.insertarToken('Comentario',self.lexema, self.fila, self.columna)
                    self.columna = self.columna + 1
                    self.estado = 0
                else:
                    self.lexema = self.lexema + caracter
                    self.estado = 2
                    self.columna = self.columna + 1
            elif self.estado == 5:
                if caracter == '"':
                    self.lexema = self.lexema + caracter
                    self.insertarToken('Cadena', self.lexema, self.fila, self.columna) 
                    self.estado = 0
                    self.columna = self.columna + 1
                elif caracter != '\n':
                    self.lexema = self.lexema + caracter
                    self.estado = 5
                    self.columna = self.columna + 1
                else: #caracter es salto de línea
                    self.lexema = self.lexema + caracter
                    self.insertarError('El lexema '+  self.lexema + ' no pertenece al lenguaje', self.fila, self.columna)
                    self.columna = self.columna + 1
                    self.estado = 0
            elif self.estado == 9:
                if caracter.isalpha():
                    #command= messagebox.showinfo(message= "Estado 9 isalpha " + caracter + " Pos "+ str(i), title="Análisis RMT")
                    self.lexema = self.lexema + caracter
                    self.estado = 9
                    self.columna = self.columna + 1
                elif caracter.isdigit():
                    #command= messagebox.showinfo(message= "Estado 9 isdigit " + caracter + " Pos "+ str(i), title="Análisis RMT")
                    self.lexema = self.lexema + caracter
                    self.estado = 9
                    self.columna = self.columna + 1
                elif caracter == '-':
                    #command= messagebox.showinfo(message= "Estado 9 isdigit " + caracter + " Pos "+ str(i), title="Análisis RMT")
                    self.lexema = self.lexema + caracter
                    self.estado = 9
                    self.columna = self.columna + 1
                else:                        
                    #command= messagebox.showinfo(message= "Aceptó " + self.lexema, title="Análisis RMT")
                    self.verificarReservadas(self.lexema, self.fila, self.columna)
                    self.estado = 0
                    i = i-1
                    self.aux = True
                    self.columna = self.columna + 1
            elif self.estado==7:
                if caracter.isdigit():
                    self.lexema = self.lexema + caracter
                    self.columna = self.columna + 1
                elif caracter == '.':
                    self.lexema = self.lexema + caracter
                    self.columna = self.columna + 1
                    estado = 8
                else:
                    self.insertarToken('Número',self.lexema, self.fila, self.columna)
                    self.columna = self.columna + 1
                    self.estado = 0
                    i = i-1
                    self.aux = True
            elif self.estado == 8:
                if caracter.isdigit():
                    self.lexema = self.lexema + caracter
                    self.columna = self.columna + 1
                    estado = 7
                else:
                    self.insertarToken('Número',self.lexema, self.fila, self.columna)
                    self.columna = self.columna + 1
                    self.estado = 0
                    i = i-1
                    self.aux = True
                

        self.imprimir()        
        return self.resultadoToken + '\n' +"\n"+ self.resultadoError +'\n'+"\n" +self.resultadoReporte
    
    def verificarReservadas(self,lex, fila, columna):
        if(lex in self.listaReservadas):
            #command= messagebox.showinfo(message= "Es reservada", title="Análisis RMT")
            self.insertarToken('Reservada '+lex, lex,fila, columna)
        else:
            #command= messagebox.showinfo(message= "Es ID", title="Análisis RMT")
            self.insertarToken('Identificador', lex, fila, columna)
        
    def insertarToken(self, tipo, lex, fila, columna):
        self.resultadoReporte += "Estado->" + str(self.estado) + "Aceptó Token->" + str(tipo)+" Lexema->" + self.lexema+"\n"
        command= messagebox.showinfo(message= "Aceptó " + lex, title="Análisis CSS")
        self.resultadoToken = self.resultadoToken + "Token->"+str(tipo)+" Lexema->" + self.lexema + "\n"
        self.tablaToken = self.tablaToken + "<TR><TD>"+tipo+"</TD><TD>"+self.lexema+"</TD><TD>"+str(fila)+"</TD><TD>"+str(columna)+"</TD></TR>"
        token = Token(tipo, lex, 0, columna)
        self.listaTokens.append(token)
        print('Token ' + tipo +' '+ lex )
        self.lexema = ''
        self.estado = 0 

    def insertarError(self, descripcion, fila, columna):  
        self.resultadoReporte += "Estado->" + str(self.estado) + "Error->" + str(descripcion)+"\n"
        self.resultadoError = self.resultadoError + "Descripción->"+ str(descripcion)+" Fila->" +str(fila)+" Columna->" +str(columna) + "\n"
        command= messagebox.showinfo(message= "Error " + descripcion, title="Análisis CSS")  
        self.tablaError = self.tablaError + "<TR><TD>"+ str(descripcion)+"</TD><TD>"+str(fila)+"</TD><TD>"+str(columna)+"</TD></TR>"
        error = Error(descripcion, fila, columna)
        print('Error ' + descripcion)
        self.listaErrores.append(error)
        self.lexema = ''
        self.estado = 0
    
    def imprimir(self):
        tabla = "<HTML><HEAD></HEAD><BODY><H1>Reporte de Tokens CSS</H1><TABLE border = \"1\"><font face=\"Arial\"><TR><TH>Tipo</TH><TH>Lexema</TH><TH>Fila</TH><TH>Columna</TH></TR>" + self.tablaToken + "</font></table><BR><BR><H1>Reporte de Errores Léxicos</H1><TABLE border = \"1\"><TR><TH>Descripción</TH><TH>Fila</TH><TH>Columna</TH></TR>" + self.tablaError + "</table></body></html>"
        rutaToken = "/home/vania/reporteCSS.html"
        archivoGuardado_=open(rutaToken, "w",encoding="utf-8")
        archivoGuardado_.write(tabla)
        archivoGuardado_.close() 
        self.tablaError = ''
        self.tablaToken = ''
        webbrowser.open_new_tab(rutaToken)