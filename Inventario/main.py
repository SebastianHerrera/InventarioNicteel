import tkinter
import customtkinter
from PIL import Image
import csv
from tkinter import StringVar,IntVar,DoubleVar
from tkinter import ttk,messagebox
from model.conexion_db import ConexionDB
#from telas import Tela
from model.tela_dao import Tela,guardar, CrearTabla,listar,sumar,eliminar
customtkinter.set_appearance_mode("light")

#TELAS LIST
telas = []
        
"""CrearTabla()"""

##VENTANA

ventana = tkinter.Tk()
ventana.title("Inventario Nicteel")
ventana.state("zoomed")
ventana.iconbitmap("img/N.ico")



##FRAME

frame = tkinter.Frame(ventana)
frame.config(bg="white")

#LOGO
logo = tkinter.PhotoImage(file="img/Logo.png")
img = tkinter.Label(frame, image=logo, width=600,height=150,bg="white")
img.place(relx=0.5,y=140, anchor=tkinter.CENTER)
frame.pack(expand=1,fill=tkinter.BOTH)



    #LECTOR DE ARCHIVOS
"""def lectorInventario():
    with open("inventario ofi.csv","r") as archivo:
        lector = csv.reader(archivo, delimiter=";")
        for fila in lector:
            #AHORA QUE TENEMOS LA LISTA, ASIGNAREMOS POSICIONES
            estanteRepisa = str(fila[0])
            codigo = str(fila[1])
            nombre = str(fila[2])
            tipo = str(fila[3])
            precioYarda = str(fila[4])  
            precioVenta = str(fila[5])
            stock = float(fila[7])         
            print(estanteRepisa,codigo,nombre,tipo,precioVenta,precioYarda,stock)           

            tela = Tela(estanteRepisa,codigo,nombre,tipo,precioYarda,precioVenta,stock)
            guardar(tela)"""
            

#LÓGICA



def inventario():
    lista = listar()
    lista.reverse()
    inventarioWindow = tkinter.Toplevel(frame) 
    inventarioWindow.title("Inventario")   
    inventarioWindow.iconbitmap("img/N.ico")

    tabla = ttk.Treeview(inventarioWindow,columns=("Codigo","Nombre","Tipo","PrecioYarda","PrecioVenta","Stock"),selectmode="browse",height=34)
    headingStyle = ttk.Style()
    headingStyle.configure("Treeview.Heading",font=("Roboto Black",16))
    columnStyle = ttk.Style()
    columnStyle.configure("Treeview",font=("Roboto Medium",10))
    vsb = ttk.Scrollbar(inventarioWindow, orient="vertical", command=tabla.yview)

    tabla.configure(yscrollcommand=vsb.set)
    tabla.column("#0",width=195,anchor=tkinter.CENTER)
    tabla.column("Codigo",width=195,anchor=tkinter.CENTER)
    tabla.column("Nombre",width=195,anchor=tkinter.CENTER)
    tabla.column("Tipo",width=195,anchor=tkinter.CENTER)
    tabla.column("PrecioYarda",width=195,anchor=tkinter.CENTER)
    tabla.column("PrecioVenta",width=195,anchor=tkinter.CENTER)
    tabla.column("Stock",width=195,anchor=tkinter.CENTER)
    #SCROLLABAR

    tabla.heading("#0",text="Estante y Repisa",anchor=tkinter.CENTER)
    tabla.heading("#1",text="Código",anchor=tkinter.CENTER)
    tabla.heading("#2",text="Nombre",anchor=tkinter.CENTER)
    tabla.heading("#3",text="Tipo",anchor=tkinter.CENTER)
    tabla.heading("#4",text="Precio por Yarda",anchor=tkinter.CENTER)
    tabla.heading("#5",text="Precio de Venta",anchor=tkinter.CENTER)
    tabla.heading("#6",text="Stock",anchor=tkinter.CENTER)

    for objeto in lista:
        tabla.insert("",0,text=objeto[0],values=(objeto[1],objeto[2],objeto[3],objeto[4],objeto[5],objeto[6]))
    vsb.place(relx=0.988, rely=0, height=(inventarioWindow.winfo_screenheight()-60))
    tabla.pack()

    inventarioWindow.state("zoomed")
    inventarioWindow.config(bg="white")



def addYardas():
    agregarWindow = tkinter.Toplevel(ventana) 
    agregarWindow.title("Agregar yardas")   
    ancho_frame= 600
    alto_frame= 400
    x_frame = frame.winfo_screenwidth()//2-ancho_frame//2
    y_frame = frame.winfo_screenheight()//2-alto_frame//2
    posicion=str(ancho_frame)+"x"+str(alto_frame)+"+"+str(x_frame)+"+"+str(y_frame)
    agregarWindow.geometry(posicion)
    agregarWindow.config(bg="white")
    agregarWindow.resizable(0,0)

    ##LABELS

    codigoTela = tkinter.Label(agregarWindow, text="Código de la tela",width=14,anchor=tkinter.E)
    codigoTela.place(relx=0.2,rely=0.2)
    codigoTela.config(bg="white", fg="black",anchor=tkinter.E,font=("Roboto Black",18))
    
    cantidadAgregar = tkinter.Label(agregarWindow, text="Yardas a agregar")
    cantidadAgregar.place(relx=0.215,rely=0.4)
    cantidadAgregar.config(bg="white", fg="black",anchor=tkinter.W,font=("Roboto Black",18))

    ##VARIABLES DE LOS ENTRYS

    codigo_var = StringVar()
    agregar = DoubleVar()
    agregar.set(0)

    ##ENTRYS

    codigo_entry = customtkinter.CTkEntry(agregarWindow, textvariable=codigo_var,width=150,height=50,justify="right",font=("Roboto Black",32))
    codigo_entry.place(relx=0.55,rely=0.18)

    nombre = customtkinter.CTkEntry(agregarWindow, textvariable=agregar,width=150,height=50,justify="right",font=("Roboto Black",32))
    nombre.place(relx=0.55,rely=0.38)


    def añadir():
        lista = listar()
        estado = False
        for x in lista:
            if x[1]==codigo_var.get():
                tela = Tela(x[0],x[1],x[2],x[3],x[4],x[5],(x[6]+agregar.get()))
                sumar(tela)
                codigo_var.set("")
                agregar.set(0)
                estado = True
                messagebox.showinfo("Sumado con éxito","Las yardas han sido sumadas del código con éxito.")
        if estado == False:
            messagebox.showerror("Error","El codigo que has ingresado o el valor a agregar es incorrecto.")


        
        

    #BUTTON

    buttonAddTela = customtkinter.CTkButton(master=agregarWindow,text="Agregar", command=añadir,fg_color=("#0e1111"),hover_color="#000000")
    buttonAddTela.configure(width=200,height=35)
    buttonAddTela.configure(font=("Roboto Black",24))
    imgAddTela = customtkinter.CTkImage(light_image=Image.open("img/plus.png"),size=(35,35))
    buttonAddTela.configure(image=imgAddTela)
    buttonAddTela.configure(border_spacing=14)
    buttonAddTela.place(relx=0.5, rely=0.74, anchor=tkinter.CENTER)


    
def lessYardas():
    quitarWindow = tkinter.Toplevel(ventana) 
    quitarWindow.title("Restar yardas")   
    ancho_frame= 600
    alto_frame= 400
    x_frame = frame.winfo_screenwidth()//2-ancho_frame//2
    y_frame = frame.winfo_screenheight()//2-alto_frame//2
    posicion=str(ancho_frame)+"x"+str(alto_frame)+"+"+str(x_frame)+"+"+str(y_frame)
    quitarWindow.geometry(posicion)
    quitarWindow.config(bg="white")
    quitarWindow.resizable(0,0)

    ##LABELS

    codigoTela = tkinter.Label(quitarWindow, text="Código de la tela",width=14,anchor=tkinter.E)
    codigoTela.place(relx=0.2,rely=0.2)
    codigoTela.config(bg="white", fg="black",anchor=tkinter.E,font=("Roboto Black",18))
    
    cantidadAgregar = tkinter.Label(quitarWindow, text="Yardas a restar")
    cantidadAgregar.place(relx=0.25,rely=0.4)
    cantidadAgregar.config(bg="white", fg="black",anchor=tkinter.W,font=("Roboto Black",18))

    ##VARIABLES DE LOS ENTRYS

    codigo_var = StringVar()
    quitar = DoubleVar()
    quitar.set(0)

    ##ENTRYS

    codigo = customtkinter.CTkEntry(quitarWindow, textvariable=codigo_var,width=150,height=50,justify="right",font=("Roboto Black",32))
    codigo.place(relx=0.55,rely=0.18)

    nombre = customtkinter.CTkEntry(quitarWindow, textvariable=quitar,width=150,height=50,justify="right",font=("Roboto Black",32))
    nombre.place(relx=0.55,rely=0.38)


    def less():
        lista = listar()
        estado = False
        for x in lista:
            if x[1]==codigo_var.get():
                tela = Tela(x[0],x[1],x[2],x[3],x[4],x[5],(x[6]-quitar.get()))
                sumar(tela)
                codigo_var.set("")
                quitar.set(0)
                estado = True
                messagebox.showinfo("Restado con éxito","Las yardas han sido restadas del código con éxito.")

        if estado == False:
            messagebox.showerror("Error","El codigo que has ingresado o el valor a agregar es incorrecto.")



    #BUTTON

    buttonLessTela = customtkinter.CTkButton(master=quitarWindow,text="Restar", command=less,fg_color=("#0e1111"),hover_color="#000000")
    buttonLessTela.configure(width=200,height=35)
    buttonLessTela.configure(font=("Roboto Black",24))
    imgLessTela = customtkinter.CTkImage(light_image=Image.open("img/less.png"),size=(35,35))
    buttonLessTela.configure(image=imgLessTela)
    buttonLessTela.configure(border_spacing=14)
    buttonLessTela.place(relx=0.5, rely=0.74, anchor=tkinter.CENTER)



def search():
    buscarWindow = tkinter.Toplevel(ventana) 
    buscarWindow.title("Buscar tela")   
    ancho_frame= 900
    alto_frame= 500
    x_frame = frame.winfo_screenwidth()//2-ancho_frame//2
    y_frame = frame.winfo_screenheight()//2-alto_frame//2
    posicion=str(ancho_frame)+"x"+str(alto_frame)+"+"+str(x_frame)+"+"+str(y_frame)
    buscarWindow.geometry(posicion)
    buscarWindow.config(bg="white")
    buscarWindow.resizable(0,0)

    ##LABELS

    codigoTela = tkinter.Label(buscarWindow, text="Código a buscar",width=14,anchor=tkinter.E)
    codigoTela.place(relx=0.02,rely=0.1)
    codigoTela.config(bg="white", fg="black",anchor=tkinter.E,font=("Roboto Black",18))
    
    cantidadAgregar = tkinter.Label(buscarWindow, text="Estante y repisa",width=14,anchor=tkinter.E)
    cantidadAgregar.place(relx=0.02,rely=0.3)
    cantidadAgregar.config(bg="white", fg="#1b1b1b",anchor=tkinter.E,font=("Roboto Black",18))

    nombreTela = tkinter.Label(buscarWindow, text="Nombre",width=14,anchor=tkinter.E)
    nombreTela.place(relx=0.02,rely=0.5)
    nombreTela.config(bg="white", fg="#1b1b1b",anchor=tkinter.E,font=("Roboto Black",18))
    
    tipoTela = tkinter.Label(buscarWindow, text="Tipo",width=14,anchor=tkinter.E)
    tipoTela.place(relx=0.02,rely=0.7)
    tipoTela.config(bg="white", fg="#1b1b1b",anchor=tkinter.E,font=("Roboto Black",18))

    yardaTela = tkinter.Label(buscarWindow, text="Precio por Yarda",width=14,anchor=tkinter.E)
    yardaTela.place(relx=0.5,rely=0.1)
    yardaTela.config(bg="white", fg="#1b1b1b",anchor=tkinter.E,font=("Roboto Black",18))

    ventaTela = tkinter.Label(buscarWindow, text="Precio de Venta",width=14,anchor=tkinter.E)
    ventaTela.place(relx=0.5,rely=0.3)
    ventaTela.config(bg="white", fg="#1b1b1b",anchor=tkinter.E,font=("Roboto Black",18))

    stockTela = tkinter.Label(buscarWindow, text="Stock",width=14,anchor=tkinter.E)
    stockTela.place(relx=0.5,rely=0.5)
    stockTela.config(bg="white", fg="#1b1b1b",anchor=tkinter.E,font=("Roboto Black",18))

    ##VARIABLES DE LOS ENTRYS

    codigoVar = StringVar()
    estanteVar = StringVar()
    nombreVar = StringVar()
    tipoVar = StringVar()
    yardaVar = StringVar()
    ventaVar = StringVar()
    stockVar = StringVar()


    ##ENTRYS

    codigo = customtkinter.CTkEntry(buscarWindow, textvariable=codigoVar,width=150,height=50,justify="right",font=("Roboto Black",32))
    codigo.place(relx=0.3,rely=0.08)

    estante = customtkinter.CTkEntry(buscarWindow, state=tkinter.DISABLED,textvariable=estanteVar,width=150,height=50,justify="right",font=("Roboto Black",32))
    estante.place(relx=0.3,rely=0.28)

    nombre = customtkinter.CTkEntry(buscarWindow, state=tkinter.DISABLED,textvariable=nombreVar,width=150,height=50,justify="right",font=("Roboto Black",32))
    nombre.place(relx=0.3,rely=0.48)

    tipo = customtkinter.CTkEntry(buscarWindow, state=tkinter.DISABLED,textvariable=tipoVar,width=150,height=50,justify="right",font=("Roboto Black",32))
    tipo.place(relx=0.3,rely=0.68)

    yarda = customtkinter.CTkEntry(buscarWindow, state=tkinter.DISABLED,textvariable=yardaVar,width=150,height=50,justify="right",font=("Roboto Black",32))
    yarda.place(relx=0.77,rely=0.08)

    venta = customtkinter.CTkEntry(buscarWindow, state=tkinter.DISABLED,textvariable=ventaVar,width=150,height=50,justify="right",font=("Roboto Black",32))
    venta.place(relx=0.77,rely=0.28)

    stock = customtkinter.CTkEntry(buscarWindow, state=tkinter.DISABLED,textvariable=stockVar,width=150,height=50,justify="right",font=("Roboto Black",32))
    stock.place(relx=0.77,rely=0.48)

    lista = listar()
    def searching():
        result = False
        for x in lista:
            if x[1]==codigo.get():
                estanteVar.set(x[0])
                nombreVar.set(x[2])
                tipoVar.set(x[3])
                yardaVar.set(x[4])
                ventaVar.set(x[5])
                if x[6]<5:
                    stock.configure(text_color="#CB4335")
                    stockVar.set(x[6])
                elif x[6]<10:
                    stock.configure(text_color="#D4AC0D")
                    stockVar.set(x[6])
                else:
                    stock.configure(text_color="#27AE60")
                    stockVar.set(x[6])
                result = True
            
        if result == False:
            messagebox.showinfo("Sin resultados","El artículo que intenta buscar, no existe en la base de datos")
            buscarWindow.destroy()

    buttonSearch = customtkinter.CTkButton(master=buscarWindow,text="Buscar", command=searching,fg_color=("#0e1111"),hover_color="#000000")
    buttonSearch.configure(width=200,height=35)
    buttonSearch.configure(font=("Roboto Black",24))
    imgSearch = customtkinter.CTkImage(light_image=Image.open("img/search.png"),size=(35,35))
    buttonSearch.configure(image=imgSearch)
    buttonSearch.configure(border_spacing=14)
    buttonSearch.place(relx=0.5, rely=0.90, anchor=tkinter.CENTER)


def new_item():
    newWindow = tkinter.Toplevel(ventana) 
    newWindow.title("Nuevo item")   
    ancho_frame= 900
    alto_frame= 500
    x_frame = frame.winfo_screenwidth()//2-ancho_frame//2
    y_frame = frame.winfo_screenheight()//2-alto_frame//2
    posicion=str(ancho_frame)+"x"+str(alto_frame)+"+"+str(x_frame)+"+"+str(y_frame)
    newWindow.geometry(posicion)
    newWindow.config(bg="white")
    newWindow.resizable(0,0)

    ##LABELS

    codigoTela = tkinter.Label(newWindow, text="Nuevo código",width=14,anchor=tkinter.E)
    codigoTela.place(relx=0.02,rely=0.1)
    codigoTela.config(bg="white", fg="black",anchor=tkinter.E,font=("Roboto Black",18))
    
    cantidadAgregar = tkinter.Label(newWindow, text="Estante y repisa",width=14,anchor=tkinter.E)
    cantidadAgregar.place(relx=0.02,rely=0.3)
    cantidadAgregar.config(bg="white", fg="#1b1b1b",anchor=tkinter.E,font=("Roboto Black",18))

    nombreTela = tkinter.Label(newWindow, text="Nombre",width=14,anchor=tkinter.E)
    nombreTela.place(relx=0.02,rely=0.5)
    nombreTela.config(bg="white", fg="#1b1b1b",anchor=tkinter.E,font=("Roboto Black",18))
    
    tipoTela = tkinter.Label(newWindow, text="Tipo",width=14,anchor=tkinter.E)
    tipoTela.place(relx=0.02,rely=0.7)
    tipoTela.config(bg="white", fg="#1b1b1b",anchor=tkinter.E,font=("Roboto Black",18))

    yardaTela = tkinter.Label(newWindow, text="Precio por Yarda",width=14,anchor=tkinter.E)
    yardaTela.place(relx=0.5,rely=0.1)
    yardaTela.config(bg="white", fg="#1b1b1b",anchor=tkinter.E,font=("Roboto Black",18))

    ventaTela = tkinter.Label(newWindow, text="Precio de Venta",width=14,anchor=tkinter.E)
    ventaTela.place(relx=0.5,rely=0.3)
    ventaTela.config(bg="white", fg="#1b1b1b",anchor=tkinter.E,font=("Roboto Black",18))

    stockTela = tkinter.Label(newWindow, text="Stock",width=14,anchor=tkinter.E)
    stockTela.place(relx=0.5,rely=0.5)
    stockTela.config(bg="white", fg="#1b1b1b",anchor=tkinter.E,font=("Roboto Black",18))

    ##VARIABLES DE LOS ENTRYS

    codigoVar = StringVar()
    estanteVar = StringVar()
    nombreVar = StringVar()
    tipoVar = StringVar()
    yardaVar = StringVar()
    ventaVar = StringVar()
    stockVar = DoubleVar()


    ##ENTRYS

    codigo = customtkinter.CTkEntry(newWindow, textvariable=codigoVar,width=150,height=50,justify="right",font=("Roboto Black",32))
    codigo.place(relx=0.3,rely=0.08)

    estante = customtkinter.CTkEntry(newWindow,textvariable=estanteVar,width=150,height=50,justify="right",font=("Roboto Black",32))
    estante.place(relx=0.3,rely=0.28)

    nombre = customtkinter.CTkEntry(newWindow,textvariable=nombreVar,width=150,height=50,justify="right",font=("Roboto Black",32))
    nombre.place(relx=0.3,rely=0.48)

    tipo = customtkinter.CTkEntry(newWindow,textvariable=tipoVar,width=150,height=50,justify="right",font=("Roboto Black",32))
    tipo.place(relx=0.3,rely=0.68)

    yarda = customtkinter.CTkEntry(newWindow,textvariable=yardaVar,width=150,height=50,justify="right",font=("Roboto Black",32))
    yarda.place(relx=0.77,rely=0.08)

    venta = customtkinter.CTkEntry(newWindow,textvariable=ventaVar,width=150,height=50,justify="right",font=("Roboto Black",32))
    venta.place(relx=0.77,rely=0.28)

    stock = customtkinter.CTkEntry(newWindow,textvariable=stockVar,width=150,height=50,justify="right",font=("Roboto Black",32))
    stock.place(relx=0.77,rely=0.48)

    def create_new():
        try:
            object = Tela(estanteVar.get(),codigoVar.get(),nombreVar.get(),tipoVar.get(),yardaVar.get(),ventaVar.get(),stockVar.get())
            guardar(object)
            messagebox.showinfo("Item creado con exito","El item fue creado de manera exitosa, y fue añadido a la base de datos.")
            
        except:
            messagebox.showinfo("Sin resultados","El artículo que intenta buscar, no existe en la base de datos")
            newWindow.destroy()

    buttonNew = customtkinter.CTkButton(master=newWindow,text="Crear", command=create_new,fg_color=("#0e1111"),hover_color="#000000")
    buttonNew.configure(width=200,height=35)
    buttonNew.configure(font=("Roboto Black",24))
    imgSearch = customtkinter.CTkImage(light_image=Image.open("img/add.png"),size=(35,35))
    buttonNew.configure(image=imgSearch)
    buttonNew.configure(border_spacing=14)
    buttonNew.place(relx=0.5, rely=0.90, anchor=tkinter.CENTER)


def remove():
    agregarWindow = tkinter.Toplevel(ventana) 
    agregarWindow.title("Elminar item")   
    ancho_frame= 600
    alto_frame= 400
    x_frame = frame.winfo_screenwidth()//2-ancho_frame//2
    y_frame = frame.winfo_screenheight()//2-alto_frame//2
    posicion=str(ancho_frame)+"x"+str(alto_frame)+"+"+str(x_frame)+"+"+str(y_frame)
    agregarWindow.geometry(posicion)
    agregarWindow.config(bg="white")
    agregarWindow.resizable(0,0)

    ##LABELS

    codigoTela = tkinter.Label(agregarWindow, text="Código del item a eliminar",width=20,anchor=tkinter.CENTER)
    codigoTela.place(relx=0.25,rely=0.25)
    codigoTela.config(bg="white", fg="black",anchor=tkinter.CENTER,font=("Roboto Black",18))
    


    ##VARIABLES DE LOS ENTRYS

    codigo_var = StringVar()

    ##ENTRYS

    codigo_entry = customtkinter.CTkEntry(agregarWindow, textvariable=codigo_var,width=150,height=50,justify="center",font=("Roboto Black",32),text_color="#CB4335")
    codigo_entry.place(relx=0.5,rely=0.45,anchor=tkinter.CENTER)



    def remover():
        lista = listar()
        estado = False
        for x in lista:
            if x[1]==codigo_var.get():
                tela = x[1]
                print(tela)
                eliminar(tela)
                estado = True
                messagebox.showinfo("Elimnado","El item fue eliminado exitosamente.")
        if estado == False:
            messagebox.showerror("Error","El código que has ingresado o el valor a agregar es incorrecto.")


        
        

    #BUTTON

    buttonAddTela = customtkinter.CTkButton(master=agregarWindow,text="Eliminar", command=remover,fg_color=("#0e1111"),hover_color="#000000")
    buttonAddTela.configure(width=200,height=35)
    buttonAddTela.configure(font=("Roboto Black",24))
    imgAddTela = customtkinter.CTkImage(light_image=Image.open("img/delete.png"),size=(35,35))
    buttonAddTela.configure(image=imgAddTela)
    buttonAddTela.configure(border_spacing=14)
    buttonAddTela.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)


def search_name():
    lista = listar()
    lista.reverse()
    searchByNameWindow = tkinter.Toplevel(frame) 
    searchByNameWindow.title("Búsqueda por nombre")   
    searchByNameWindow.iconbitmap("img/N.ico")
    tabla = ttk.Treeview(searchByNameWindow,columns=("Codigo","Nombre","Tipo","PrecioYarda","PrecioVenta","Stock"),selectmode="browse",height=26)
    headingStyle = ttk.Style()
    headingStyle.configure("Treeview.Heading",font=("Roboto Black",16))
    columnStyle = ttk.Style()
    columnStyle.configure("Treeview",font=("Roboto Medium",10))
    vsb = ttk.Scrollbar(searchByNameWindow, orient="vertical", command=tabla.yview)
    vsb.place(relx=0.988, rely=0, height=(searchByNameWindow.winfo_screenheight()-60))

    nombreToSearch = tkinter.Label(searchByNameWindow, text="Nombre:",width=10,anchor=tkinter.CENTER)
    nombreToSearch.place(relx=0.23,rely=0.11)
    nombreToSearch.config(bg="white", fg="black",anchor=tkinter.CENTER,font=("Roboto Black",32))

    nombreVar = StringVar()
    nombre = customtkinter.CTkEntry(searchByNameWindow,textvariable=nombreVar,width=250,height=50,justify="right",font=("Roboto Black",22))
    nombre.place(relx=0.41,rely=0.118)

    


    tabla.configure(yscrollcommand=vsb.set)
    tabla.column("#0",width=195,anchor=tkinter.CENTER)
    tabla.column("Codigo",width=195,anchor=tkinter.CENTER)
    tabla.column("Nombre",width=195,anchor=tkinter.CENTER)
    tabla.column("Tipo",width=195,anchor=tkinter.CENTER)
    tabla.column("PrecioYarda",width=195,anchor=tkinter.CENTER)
    tabla.column("PrecioVenta",width=195,anchor=tkinter.CENTER)
    tabla.column("Stock",width=195,anchor=tkinter.CENTER)
    #SCROLLABAR

    tabla.heading("#0",text="Estante y Repisa",anchor=tkinter.CENTER)
    tabla.heading("#1",text="Código",anchor=tkinter.CENTER)
    tabla.heading("#2",text="Nombre",anchor=tkinter.CENTER)
    tabla.heading("#3",text="Tipo",anchor=tkinter.CENTER)
    tabla.heading("#4",text="Precio por Yarda",anchor=tkinter.CENTER)
    tabla.heading("#5",text="Precio de Venta",anchor=tkinter.CENTER)
    tabla.heading("#6",text="Stock",anchor=tkinter.CENTER)


    def searching():
        searched = []
        for i in tabla.get_children():
            tabla.delete(i)
        for x in lista:
            nombre = str(x[2])
            namecito = nombreVar.get()
            if nombre ==  namecito or nombre== namecito+" ":
                searched.append((x[0],x[1],x[2],x[3],x[4],x[5],x[6]))
            elif nombre==  namecito.upper() or nombre==  namecito.upper()+" ":
                searched.append((x[0],x[1],x[2],x[3],x[4],x[5],x[6]))
            elif nombre== namecito.lower() or nombre== namecito.lower()+" ":
                searched.append((x[0],x[1],x[2],x[3],x[4],x[5],x[6]))
            elif nombre== namecito.capitalize() or nombre== namecito.capitalize()+" ":
                searched.append((x[0],x[1],x[2],x[3],x[4],x[5],x[6]))

        for objeto in searched:
            tabla.insert("",0,text=objeto[0],values=(objeto[1],objeto[2],objeto[3],objeto[4],objeto[5],objeto[6]))
    

    buttonNew = customtkinter.CTkButton(master=searchByNameWindow,text="Buscar", command=searching,fg_color=("#0e1111"),hover_color="#000000")
    buttonNew.configure(width=160,height=25)
    buttonNew.configure(font=("Roboto Black",24))
    imgSearch = customtkinter.CTkImage(light_image=Image.open("img/search.png"),size=(35,35))
    buttonNew.configure(image=imgSearch)
    buttonNew.configure(border_spacing=14)
    buttonNew.place(relx=0.68, rely=0.15, anchor=tkinter.CENTER)
    
    tabla.place(relx=0,rely=0.3)
    searchByNameWindow.state("zoomed")
    searchByNameWindow.config(bg="white")

#BOTONES

buttonInventario = customtkinter.CTkButton(master=frame,text="Inventario", command=inventario,fg_color=("#0e1111"),hover_color="#000000")
buttonInventario.configure(width=200,height=35)
buttonInventario.configure(font=("Roboto Black",24))
imgInventario = customtkinter.CTkImage(light_image=Image.open("img/inventario.png"),size=(35,35))
buttonInventario.configure(image=imgInventario)
buttonInventario.configure(border_spacing=14)
buttonInventario.place(relx=0.3, rely=0.62, anchor=tkinter.CENTER)

buttonAddTela = customtkinter.CTkButton(master=frame,text="Buscar tela", command=search,fg_color=("#0e1111"),hover_color="#000000")
buttonAddTela.configure(width=200,height=35)
buttonAddTela.configure(font=("Roboto Black",23))
imgAddTela = customtkinter.CTkImage(light_image=Image.open("img/search.png"),size=(35,35))
buttonAddTela.configure(image=imgAddTela)
buttonAddTela.configure(border_spacing=14)
buttonAddTela.place(relx=0.3, rely=0.74, anchor=tkinter.CENTER)

buttonAddTela = customtkinter.CTkButton(master=frame,text="Añadir tela", command=addYardas,fg_color=("#0e1111"),hover_color="#000000")
buttonAddTela.configure(width=200,height=35)
buttonAddTela.configure(font=("Roboto Black",24))
imgAddTela = customtkinter.CTkImage(light_image=Image.open("img/plus.png"),size=(35,35))
buttonAddTela.configure(image=imgAddTela)
buttonAddTela.configure(border_spacing=14)
buttonAddTela.place(relx=0.3, rely=0.86, anchor=tkinter.CENTER)

buttonAddTela = customtkinter.CTkButton(master=frame,text="Quitar tela", command=lessYardas,fg_color=("#0e1111"),hover_color="#000000")
buttonAddTela.configure(width=200,height=35)
buttonAddTela.configure(font=("Roboto Black",24))
imgAddTela = customtkinter.CTkImage(light_image=Image.open("img/less.png"),size=(35,35))
buttonAddTela.configure(image=imgAddTela)
buttonAddTela.configure(border_spacing=14)
buttonAddTela.place(relx=0.5, rely=0.62, anchor=tkinter.CENTER)

buttonInventario = customtkinter.CTkButton(master=frame,text="Nuevo item", command=new_item,fg_color=("#0e1111"),hover_color="#000000")
buttonInventario.configure(width=200,height=35)
buttonInventario.configure(font=("Roboto Black",24))
imgInventario = customtkinter.CTkImage(light_image=Image.open("img/new.png"),size=(35,35))
buttonInventario.configure(image=imgInventario)
buttonInventario.configure(border_spacing=14)
buttonInventario.place(relx=0.5, rely=0.74, anchor=tkinter.CENTER)

buttonAddTela = customtkinter.CTkButton(master=frame,text="Borrar item", command=remove,fg_color=("#0e1111"),hover_color="#000000")
buttonAddTela.configure(width=200,height=35)
buttonAddTela.configure(font=("Roboto Black",24))
imgAddTela = customtkinter.CTkImage(light_image=Image.open("img/delete.png"),size=(35,35))
buttonAddTela.configure(image=imgAddTela)
buttonAddTela.configure(border_spacing=14)
buttonAddTela.place(relx=0.5, rely=0.86, anchor=tkinter.CENTER)

buttonAddTela = customtkinter.CTkButton(master=frame,text="Por nombre", command=search_name,fg_color=("#0e1111"),hover_color="#000000")
buttonAddTela.configure(width=200,height=35)
buttonAddTela.configure(font=("Roboto Black",24))
imgAddTela = customtkinter.CTkImage(light_image=Image.open("img/search.png"),size=(35,35))
buttonAddTela.configure(image=imgAddTela)
buttonAddTela.configure(border_spacing=14)
buttonAddTela.place(relx=0.7, rely=0.62, anchor=tkinter.CENTER)

"""lectorInventario()"""
##MAINLOOP

ventana.mainloop()