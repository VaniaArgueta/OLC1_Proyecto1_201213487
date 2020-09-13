__author__ = "Vania Argueta - 201213487"

from LexicoHTML import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

class Principal:
    def __init__(self,window):
        self.ventana = window
        self.ventana.title("Proyecto 1 - 201213487")
        self.ventana.geometry("1300x600")
        self.ventana.configure(bg='#596d82')
        frame = LabelFrame(self.ventana, text = 'ML WEB', bg='#596d82', font=('Helvetica', 18, 'bold'), foreground='#f3d8e0')
        frame.grid(row=5,column=5,columnspan=3,pady=20)
        etiquetaCursor = Label(frame, text = 'Cursor',font=('Helvetica', 14, 'bold'), foreground='#f3d8e0', bg='#596d82')
        etiquetaCursor.grid(row=6, column=2)
        menubar = Menu(self.ventana, bg='#f3d8e0')
        self.ventana.config(menu=menubar)
        filemenu = Menu(menubar, tearoff=1)
        filemenu.add_command(label="Nuevo")
        filemenu.add_command(label="Abrir",command=self.onOpen())
        filemenu.add_command(label="Guardar")
        filemenu.add_command(label="Guardar como")
        filemenu.add_command(label="Ejecutar análisis")
        filemenu.add_separator()
        filemenu.add_command(label="Salir", command=self.ventana.quit)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Manual de usuario")
        helpmenu.add_command(label="Manual técnico")
        helpmenu.add_separator()
        helpmenu.add_command(label="Acerca del proyecto", command = self.mostrarMensajeAcercaDe())

        menubar.add_cascade(label="Archivo", menu=filemenu)
        menubar.add_cascade(label="Ayuda", menu=helpmenu)
        
        #TextArea----------------------------------------------
        self.editor = Text(frame, height=30, width=90, background='#cfd3ca', font='Arial')
        self.editor.grid(row=7,column=2)

        self.consola = Text(frame, height=30, width=40, background = '#303750', foreground = '#f3d8e0', font='Arial')
        self.consola.grid(row=7,column=110)

        ################################__BOTON__#################################
        #self.boton = Button(frame, text ="Enviar") # , command = self.metodo
        #self.boton.grid(row=9,column=3)
    def mostrarMensajeAcercaDe(self):
        mensaje = 'Proyecto 1 - Organización de Lenguajes y Compiladores1\nVania Argueta Rodríguez\nCarné 2012-13487'
        command= messagebox.showinfo(message= mensaje, title="Acerca del proyecto")
    def onOpen(self):
        print(filedialog.askopenfilename(initialdir = "/",title = "Open file",filetypes = (("Python files","*.py;*.pyw"),("All files","*.*"))))


if __name__ == '__main__':
    window = Tk()
    app = Principal(window)
    window.mainloop()
