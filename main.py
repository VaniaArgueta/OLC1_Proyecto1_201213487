__author__ = "Vania Argueta - 201213487"

from LexicoHTML import *
from LexicoRMT import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os.path

class Principal:
    def __init__(self,window):
        self.analisisRMT = LexicoRMT()
        self.extension = ''
        self.ruta = ''
        self.ventana = window
        self.ventana.title("Proyecto 1 - 201213487")
        self.ventana.geometry("1300x600")
        self.ventana.configure(bg='#596d82')
        frame = LabelFrame(self.ventana, text = 'ML WEB', bg='#596d82', font=('Helvetica', 18, 'bold'), foreground='#f3d8e0')
        frame.grid(row=5,column=5,columnspan=3,pady=20)
        etiquetaCursor = Label(frame, text = 'Cursor',font=('Helvetica', 14, 'bold'), foreground='#f3d8e0', bg='#596d82')
        etiquetaCursor.grid(row=6, column=2)
        #Menú------------------------------------------------------------------------------------------------------------
        menubar = Menu(self.ventana, bg='#f3d8e0')
        self.ventana.config(menu=menubar)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Nuevo", command= lambda: self.nuevoArchivo())
        filemenu.add_command(label="Abrir",command= lambda: self.abrirArchivo())
        filemenu.add_command(label="Guardar",command= lambda: self.guardarArchivo())
        filemenu.add_command(label="Guardar como",command= lambda: self.guardarComo())
        filemenu.add_separator()
        filemenu.add_command(label="Salir", command=self.ventana.quit)

        ejecmenu = Menu(menubar, tearoff=0)
        ejecmenu.add_command(label="Analizar archivo", command = lambda: self.analizarArchivo())
        #ejecmenu.add_command(label="Analizar CSS")
        #ejecmenu.add_command(label="Analizar JavaScript")
        
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Manual de usuario", command = lambda: etiquetaCursor.config(text = 'hosdfasdf'))
        #lbl.["text"] = "New text"
        helpmenu.add_command(label="Manual técnico")
        helpmenu.add_separator()
        helpmenu.add_command(label="Acerca del proyecto", command = lambda: self.mostrarMensajeAcercaDe())

        menubar.add_cascade(label="Archivo", menu=filemenu)
        menubar.add_cascade(label="Ejecutar", menu=ejecmenu)
        menubar.add_cascade(label="Ayuda", menu=helpmenu)
        
        #TextArea----------------------------------------------
        self.editor = Text(frame, height=30, width=90, background='#cfd3ca', font='Helvetica')
        self.editor.grid(row=7,column=2)

        self.consola = Text(frame, height=30, width=40, background = '#303750', foreground = '#f3d8e0', font='Helvetica')
        self.consola.grid(row=7,column=110)

        ################################__BOTON__#################################
        self.boton = Button(frame, text ="RMT", command = lambda: self.analisisRMT.analizarLexico(self.editor.get("0.0","end"))) # , command = self.metodo
        self.boton.grid(row=32,column=2)

    def mostrarMensajeAcercaDe(self):
        mensaje = 'Proyecto 1 - Organización de Lenguajes y Compiladores1\nVania Argueta Rodríguez\nCarné 2012-13487'
        command= messagebox.showinfo(message= mensaje, title="Acerca del proyecto")

    def nuevoArchivo(self):
        self.editor.delete("1.0","end")
        self.extension = ''
        self.ruta = ''
        messagebox.showinfo(message= self.extension, title="Extensión del archivo")

    def abrirArchivo(self):
        filename = filedialog.askopenfilename(initialdir = "/",title = "Abrir Archivo",filetypes = (("HTML files","*.html;*.HTML"),("CSS files","*.css;*.CSS"),("JS files","*.js;*.JS"),("RMT files","*.rmt;*.RMT"),("All files","*.*")))
        #print(filedialog.askopenfilename(initialdir = "/",title = "Open file",filetypes = (("HTML files","*.html;*.HTML"),("CSS files","*.css;*.CSS"),("JS files","*.js;*.JS"),("All files","*.*"))))
        f=open(filename)    
        txt = f.read()  
        self.editor.delete("1.0","end")
        self.editor.insert('0.0',txt)
        f.close()
        self.extension = os.path.splitext(filename)[1]
        command= messagebox.showinfo(message= 'Se abrió un archivo con extensión ' + self.extension, title="Extensión del archivo")
        #command= messagebox.showinfo(message= f.name, title="Extensión del archivo") todo el path
        self.ruta = os.path.splitext(filename)[0]

    def guardarArchivo(self):
        if(self.ruta != ''):
            archivoGuardado_=open(self.ruta, "w", encoding="utf-8")
            archivoGuardado_.write(self.editor.get("0.0","end"))
            self.extension = os.path.splitext(self.ruta)[1]
            archivoGuardado_.close()            
            command= messagebox.showinfo(message= "Archivo guardado en path " + self.ruta, title="Archivo Guardado")
            command= messagebox.showinfo(message= "Archivo con extensión " + self.extension, title="Archivo Guardado")
        else:
            self.guardarComo()

    def guardarComo(self):
        guardarC = filedialog.asksaveasfilename(initialdir = "/media/vania/",title = "Guardar como", defaultextension = ".txt", filetypes = (("HTML files","*.html;*.HTML"),("CSS files","*.css;*.CSS"),("JS files","*.js;*.JS"),("RMT files","*.rmt;*.RMT"),("All files","*.*")))
        archivoGuardado=open(guardarC, "w", encoding="utf-8") 
        archivoGuardado.write(self.editor.get("0.0", "end"))
        self.extension = os.path.splitext(guardarC)[1]
        archivoGuardado.close()
        print(guardarC)
        self.ruta = guardarC        
        command= messagebox.showinfo(message= "Archivo guardado en path " + self.ruta, title="Archivo Guardado")
        command= messagebox.showinfo(message= "Archivo con extensión " + self.extension, title="Archivo Guardado")

    def analizarArchivo(self):
        print("AnalizarArchivo")
        if self.extension == '.html' or self.extension == '.HTML':
            command= messagebox.showinfo(message= "Se analizará un archivo con extensión " + self.extension, title="Análisis HTML")
        elif self.extension == '.css' or self.extension == '.CSS':
            command= messagebox.showinfo(message= "Se analizará un archivo con extensión " + self.extension, title="Análisis CSS")
        elif self.extension == '.js' or self.extension == '.JS':
            command= messagebox.showinfo(message= "Se analizará un archivo con extensión " + self.extension, title="Análisis JavaScript")
        elif self.extension == '.rmt' or self.extension == '.RMT':
            command= messagebox.showinfo(message= "Se analizará un archivo con extensión " + self.extension, title="Análisis RMT")
            #command= messagebox.showinfo(message= "EJecutar análisis " + self.analisisRMT.analisisLexico('jelou'), title="Análisis RMT")
            if self.editor.get("0.0","end") != '':
                self.analisisRMT.analizarLexico(self.editor.get("0.0","end"))
        else:
            command= messagebox.showinfo(message= "Debe abrir un archivo con extensión HTML, CSS, JS o RMT", title="Error")

            

if __name__ == '__main__':
    window = Tk()
    app = Principal(window)
    window.mainloop()
