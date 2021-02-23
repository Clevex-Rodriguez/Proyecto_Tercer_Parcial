from kivy.app import App
from kivy.lang import Builder
#from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.config import Config
from kivy.uix.popup import Popup

import winsound

Config.set('graphics', 'width', 1000)
Config.set('graphics', 'height', 600)


class TercerParcialWindow(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = FadeTransition()



class Pantalla1(Screen):
    pass

class Estudiantes_Administrativos(Screen):
    pass
class Resultado_Busqueda(Screen):
    pass
class Solicitante(Screen):
    pass
class Estudiante_UNT(Screen):
    pass
class Estudiante_Externo(Screen):
    pass

class Estudiantes(Screen):
    def mostrar_busqueda(self, *args):
        MostrarBusqueda().open()

class PantallaAdministrativos(Screen):
    def checkbox_click(self, instance, value):
        if value == True:
            self.ids.contr.password = False
        else:
            self.ids.contr.password = True

    def contr_avisos(self, *args):
        if self.ids.contr.text == '':
            winsound.PlaySound("SystemExit", winsound.SND_ASYNC)
            Contras_vacia().open()
        else:
            winsound.PlaySound("SystemExit", winsound.SND_ASYNC)
            Contras_incorrecta().open()

class Contras_vacia(Popup):
    pass

class Contras_incorrecta(Popup):
    pass

class MostrarBusqueda(Popup):
    pass

kv = Builder.load_file("tercerparcial.kv")
class TercerParcialApp(App):
    def build(self):
        self.title = 'BIBLIOTECA UNT'
        self.icon = 'imagenes/logo_unt.png'
        #return TercerParcialWindow()
        return kv

if __name__=='__main__':
    TercerParcialApp().run()