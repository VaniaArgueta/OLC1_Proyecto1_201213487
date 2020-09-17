from Error import *
from Token import *
from tkinter import messagebox
import webbrowser

class LexicoHTML:
  def __init__(self):
    self.longitud = 0
    self.listaSignos = ['>', '/', '=']  
    self.listaReservadas = ['body', 'h1','h2','h3','h4','h5','h6','p', 'br', 'img','src','a','href','ul','li','style','table','border','caption','tr','th','td','colorgroup','col','thead','tbody','tfoot']
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

  def analizar(self, cadena, estado):
    command= messagebox.showinfo(message= cadena, title="Análisis HTML")
    cadena = cadena.lower() + '  '
    self.estado = 0
    caracter = ''
    lim = len(cadena)
    for i in range(lim):
      caracter = cadena[i]
      command= messagebox.showinfo(message= "Estado->" + str(self.estado) + ' Pos->' + str(i)+ "->"+ caracter, title="Análisis HTML")

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
          self.insertarToken('Signo' + caracter, caracter, self.fila, self.columna) 
          self.estado = 0
          self.columna = self.columna + 1   
        elif caracter == '<':
          self.lexema = self.lexema + caracter
          self.estado = 1
          self.columna = self.columna + 1           
        elif caracter.isalpha():
          self.lexema = self.lexema + caracter
          self.estado = 4
          self.columna = self.columna + 1
        elif caracter == '"':
          self.lexema = caracter
          self.estado = 5
          self.columna = self.columna + 1
        elif caracter == '\'':
          self.lexema = caracter
          self.estado = 14
          self.columna = self.columna + 1
        else:
          self.insertarError('El caracter '+  caracter + ' no pertenece al lenguaje', self.fila, self.columna)
          self.columna = self.columna + 1
          self.estado = 0

      elif self.estado ==1:
        if caracter == '!':
          self.lexema = self.lexema + caracter
          self.estado = 7
          self.columna = self.columna + 1
        else:
          self.insertarToken('Signo'+self.lexema,self.lexema, self.fila, self.columna)
          self.columna = self.columna + 1
          self.estado = 0
          i = i-1
          self.aux = True
      elif self.estado == 7:
        if caracter == '-':
          self.lexema = self.lexema + caracter
          self.estado = 8
          self.columna = self.columna + 1
        else:
          self.insertarError('El caracter '+  caracter + ' no pertenece al lenguaje', self.fila, self.columna)
          self.columna = self.columna + 1
          self.estado = 0
          i = i-1
          self.aux = True
      elif self.estado ==8:
        if caracter == '-':
          self.lexema = self.lexema + caracter
          self.estado = 9
          self.columna = self.columna + 1
        else:
          self.lexema = self.lexema + caracter
          self.insertarError('El lexema '+  self.lexema + ' no pertenece al lenguaje', self.fila, self.columna)
          self.columna = self.columna + 1
          self.estado = 0
      elif self.estado ==9:
        if caracter == '-':
          self.lexema = self.lexema + caracter
          self.estado = 10
          self.columna = self.columna + 1
        else:
          self.lexema = self.lexema + caracter
          self.estado = 9
          self.columna = self.columna + 1
      elif self.estado == 10:
        if caracter == '-':
          self.lexema = self.lexema + caracter
          self.estado = 11
          self.columna = self.columna + 1
        else:
          self.lexema = self.lexema + caracter
          self.estado = 9
          self.columna = self.columna + 1
      elif self.estado == 11:
        if caracter == '>':
          self.lexema = self.lexema + caracter
          self.insertarToken('Comentario',self.lexema, self.fila, self.columna)
          self.columna = self.columna + 1
          self.estado = 0
        else:
          self.lexema = self.lexema + caracter
          self.estado = 9
          self.columna = self.columna + 1
      elif self.estado == 4:
        if caracter.isalpha():
          #command= messagebox.showinfo(message= "Estado 4 isalpha " + caracter + " Pos "+ str(i), title="Análisis RMT")
          self.lexema = self.lexema + caracter
          self.estado = 4
          self.columna = self.columna + 1
        elif caracter.isdigit():
          #command= messagebox.showinfo(message= "Estado 4 isdigit " + caracter + " Pos "+ str(i), title="Análisis RMT")
          self.lexema = self.lexema + caracter
          self.estado = 4
          self.columna = self.columna + 1
        else:                        
          command= messagebox.showinfo(message= "Aceptó " + caracter, title="Análisis RMT")
          self.verificarReservadas(self.lexema, self.fila, self.columna)
          self.estado = 0
          i = i-1
          self.aux = True
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
      elif self.estado == 14:
        if caracter == '\'':
          self.lexema = self.lexema + caracter
          self.insertarToken('Cadena', self.lexema, self.fila, self.columna) 
          self.estado = 0
          self.columna = self.columna + 1 
        elif caracter != '\n':
          self.lexema = self.lexema + caracter
          self.estado = 14
          self.columna = self.columna + 1
        else: #caracter es salto de línea
          self.lexema = self.lexema + caracter
          self.insertarError('El lexema '+  self.lexema + ' no pertenece al lenguaje', self.fila, self.columna)
          self.columna = self.columna + 1
          self.estado = 0

    self.imprimir()
    return self.resultadoToken + '\n' + self.resultadoError

  def verificarReservadas(self,lex, fila, columna):
    if(lex in self.listaReservadas):
      command= messagebox.showinfo(message= "Es reservada", title="Análisis RMT")
      self.insertarToken('Reservada '+lex, lex,fila, columna)
    else:
      command= messagebox.showinfo(message= "Es ID", title="Análisis RMT")
      self.insertarToken('Palabra/Identificador', lex, fila, columna)

        
  def insertarToken(self, tipo, lex, fila, columna):
    command= messagebox.showinfo(message= "Aceptó " + lex, title="Análisis RMT")
    self.resultadoToken = self.resultadoToken + "Token->"+str(tipo)+" Lexema->" + self.lexema + "\n"
    self.tablaToken = self.tablaToken + "<TR><TD>"+tipo+"</TD><TD>"+self.lexema+"</TD><TD>"+str(fila)+"</TD><TD>"+str(columna)+"</TD></TR>"
    token = Token(tipo, lex, 0, columna)
    self.listaTokens.append(token)
    print('Token ' + tipo +' '+ lex )
    self.lexema = ''
    self.estado = 0        
    
  def insertarError(self, descripcion, fila, columna):  
    self.resultadoError = self.resultadoError + "Descripción->"+ str(descripcion)+" Fila->" +str(fila)+" Columna->" +str(columna) + "\n"
    command= messagebox.showinfo(message= "Error " + descripcion, title="Análisis RMT")  
    self.tablaError = self.tablaError + "<TR><TD>"+ str(descripcion)+"</TD><TD>"+str(fila)+"</TD><TD>"+str(columna)+"</TD></TR>"
    error = Error(descripcion, fila, columna)
    print('Error ' + descripcion)
    self.listaErrores.append(error)
    self.lexema = ''
    self.estado = 0

    
  def imprimir(self):
    tabla = "<HTML><HEAD></HEAD><BODY><H1>Reporte de Tokens HTML</H1><TABLE border = \"1\"><font face=\"Arial\"><TR><TH>Tipo</TH><TH>Lexema</TH><TH>Fila</TH><TH>Columna</TH></TR>" + self.tablaToken + "</font></table><BR><BR><H1>Reporte de Errores Léxicos</H1><TABLE border = \"1\"><TR><TH>Descripción</TH><TH>Fila</TH><TH>Columna</TH></TR>" + self.tablaError + "</table></body></html>"
    rutaToken = "/home/vania/reporteHTML.html"
    archivoGuardado_=open(rutaToken, "w",encoding="utf-8")
    archivoGuardado_.write(tabla)
    archivoGuardado_.close() 
    self.tablaError = ''
    self.tablaToken = ''
    webbrowser.open_new_tab(rutaToken)
