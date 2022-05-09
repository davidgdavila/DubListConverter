import os
import subprocess
from tkinter import filedialog as fd
import tkinter as tk
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.config import Config

Window.size=(750,550)

class LayoutPrincipal(BoxLayout):

    texto=""
    ruta_abrir_archivo=""
    ruta_salvar_arhivo=""
    etiqueta=StringProperty("Arrastra Los Archivos Aquí...")
    ruta_inicio = os.path.expanduser("~") + "\\documents\\"
    operador=""

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        Window.bind(on_drop_file=self.on_drop_file)

    def on_drop_file(self, Window, file_path, *args):
        self.ruta_abrir_archivo=file_path.decode(encoding="utf-8")
        self.seleccionar_salvar_archivo()


    def seleccionar_archivo(self):
        root = tk.Tk()
        root.withdraw()
        filename = fd.askopenfilename(
                title='Abrir archivo',
                initialdir=self.ruta_inicio,
                filetypes=(('text files', '*.txt'),('All files', '*.*')))
        self.ruta_abrir_archivo=filename
        if filename:
            self.seleccionar_salvar_archivo()
        else:
            pass

    def cargar_archivo(self,path):
        self.texto = ""
        try:
            with open(path,encoding='utf-16-le') as file:
                for lineas in file:
                    termino = lineas.split("\t", )
                    self.texto += termino[31] + "\t" + termino[32] + "\t" + termino[2] + "\n"
            self.guardar_archivo()
        except IndexError:
            self.ids.eti1.text="El formato no es correcto. Vuelve a intentarlo."
        except UnicodeDecodeError:
            self.ids.eti1.text="Error: El archivo que intentas cargar no es un txt"
        except:
            self.ids.eti1.text = "Ocurrio un error desconocido. Contacta al programador"

    def seleccionar_salvar_archivo(self):
        root = tk.Tk()
        root.withdraw()
        nombre_archivo=os.path.basename(self.ruta_abrir_archivo)
        rutabase = os.path.dirname(self.ruta_abrir_archivo)
        filename= fd.asksaveasfilename(
            initialfile = "DubList_" + nombre_archivo,
            title = 'Salvar archivo',
            initialdir = rutabase,
            filetypes = (('text files', '*.txt'),('All files', '*.*')))
        self.ruta_salvar_arhivo=filename
        if filename:
            self.cargar_archivo(self.ruta_abrir_archivo)
        else:
            pass


    def guardar_archivo(self):
        if ".txt" in self.ruta_salvar_arhivo:
            self.ruta_salvar_arhivo.replace(".txt","")
        else:
            self.ruta_salvar_arhivo += ".txt"
        with open(self.ruta_salvar_arhivo, 'w',encoding='utf-8') as stream:
            stream.write(self.texto)
        self.etiqueta = "¡Se ha convertido el archivo!\n"+self.ruta_salvar_arhivo

    def show_acerca_de(self):
        contenido = Acerca_de()
        self._popup = Popup(
            title='Acerca de Dub List Converter',
            content=contenido,
            size_hint=(None, None), size=(400, 400))
        self._popup.open()

    def convertir_archivo(self,path):
        self.texto=""
        self.ruta=path
        try:
            with open(self.ruta,encoding='utf-16-le') as file:
                for lineas in file:
                    termino=lineas.split("\t",)
                    self.texto+=termino[31]+"\t"+termino[32]+"\t"+termino[2]+"\n"
            self.seleccionar_salvar_archivo()
        except IndexError:
            self.ids.eti1.text="El formato no es correcto"
        except UnicodeDecodeError:
            self.ids.eti1.text="Error:El archivo no es un txt o el formato es incorrecto"
        except:
            self.ids.eti1.text = "Error desconocido. Vuelva a intentarlo"

    def limpiar(self):
        self.etiqueta = "Arrastra Los Archivos Aquí..."

    def tutorial(self):
        #os.system("Tutorial.pdf")S
        path="Tutorial.pdf"
        subprocess.Popen([path], shell=True)



class Acerca_de(MDBoxLayout):
    texto_etiqueta = StringProperty("Autor: David Israel Gonzalez Davila.\n\n"
                                "Versión: 1.1\n\n"
                                "Fecha: 27/marzo/2022\n\n"
                                "Descripción: Generar el formato correcto para\n"
                                "dar de alta de una forma mas eficiente los \n"
                                "materiales ingestados en los Nexios mediante\n"
                                "el ADC\n\n"
                                "Agradecimientos:\n"
                                "*Elizabeth Maldonado\n"
                                "*Christopher Collazo")
class DubListConverterApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Config.set("kivy","window_icon","dlc.ico")
        self.title = "DubListConverter"
        self.icon = "dlc.ico"

    def build(self):
        self.theme_cls.primary_palette = "Gray"
        self.root= Builder.load_file("DubListConverterw7.kv")

Factory.register('Acerca_de', cls=Acerca_de)

DubListConverterApp().run()

