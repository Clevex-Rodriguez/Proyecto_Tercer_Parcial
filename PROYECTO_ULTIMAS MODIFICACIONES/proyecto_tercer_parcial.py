from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.config import Config
from kivy.uix.popup import Popup
import winsound
from kivy.uix.screenmanager import SlideTransition
import psycopg2

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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def n_matricula(self):
        txt = self.ids.Matricula.text
        self.ids.N_matricula.text = txt

    def autenticar_unt(self):
        conn = None
        try:
            conn=psycopg2.connect(
                host="localhost",
                database="lab07",
                user="postgres",
                password="ladymendoza_prograII",
                port="5432")
            cur=conn.cursor()
            cur.execute("SELECT * FROM estudiante_unt WHERE n_matricula = %s", (self.ids.Matricula.text,))
            row = cur.fetchone()
            if row is not None:
                print ("si esta!!!!!!!!!!!!!!!!!!!!!!") #TEMPORAL
            elif row is None:
                print("El N° de matricula no existe")    #TEMPORAL
            else:
                pass
            if conn is not None:
                conn.close()
        except (Exception, psycopg2.DatabaseError) as e:
            print(e, "** ERROR!!!!")
        finally:
            if conn is not None:
                conn.close()

    def next(self, *args):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = self.manager.next()
        App.get_running_app().root.current = "pantalla03"


class Estudiante_Externo(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def nombres_externo(self):
        txt = self.ids.Nombres.text
        self.ids.Nombres_E.text = txt

    def apellidos_externo(self):
        txt = self.ids.Apellidos.text
        self.ids.Apellidos_E.text = txt

    def dni_externo(self):
        txt = self.ids.DNI.text
        self.ids.DNI_E.text = txt

    def submit(self, dni, nombres, apellidos):
        sql = """ INSERT INTO estudiante_externo (dni, nombres, apellidos) VALUES (%s, %s, %s);"""
        conn = None
        try:
            conn=psycopg2.connect(
				host="localhost",
				database="lab07",
				user="postgres",
				password="ladymendoza_prograII",
				port="5432")
            cur=conn.cursor()
            cur.execute(sql, (dni, nombres, apellidos,))
            conn.commit()
            cur.close()
            if conn is not None:
                conn.close()
            print("todo bien")
        except (Exception, psycopg2.DatabaseError) as e:
            print(e, "** ERROR!!!!")
        finally:
            if conn is not None:
                conn.close()

    def datos_base(self):
        nombre = self.ids.Nombres.text
        apellido = self.ids.Apellidos.text
        dni = self.ids.DNI.text
        self.submit(dni, nombre, apellido)

    def next(self, *args):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = self.manager.next()
        App.get_running_app().root.current = "pantalla1"

class Estudiantes(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def titulo(self):
        txt = self.ids.Titulo.text
        self.ids.Titulo_L.text = txt

    def codigo(self):
        txt = self.ids.Codigo.text
        self.ids.Codigo_L.text = txt

    def autor(self):
        txt = self.ids.Autor.text
        self.ids.Autor_L.text = txt

    def buscar_disponible(self):
        conn = None
        try:
            conn=psycopg2.connect(
                host="localhost",
                database="lab07",
                user="postgres",
                password="ladymendoza_prograII",
                port="5432")
            cur=conn.cursor()
            cur.execute("SELECT * FROM libro WHERE codigo = %s", (self.ids.Codigo.text,))
            row = cur.fetchone()
            if row is not None:
                conn = None
                try:
                    conn=psycopg2.connect(
						host="localhost",
						database="lab07",
						user="postgres",
						password="ladymendoza_prograII",
						port="5432")
                    cur=conn.cursor()
                    cur.execute("SELECT * FROM libro_no_disponible WHERE codigo = %s", (self.ids.Codigo.text,))
                    row1 = cur.fetchone()
                    if row1 is None:
                        while row is not None:
                            cod=str(row[0])
                            tit=str(row[1])
                            aut=str(row[2])
                            print(cod)
                            print(tit)
                            print(aut)
                            row = cur.fetchone()
                        conn.commit()
                        cur.close()
                    elif row1 is not None:
                        print("Este libro no esta disponible")
                except (Exception, psycopg2.DatabaseError) as error:
                    print(error)
                finally:
                    if conn is not None:
                        conn.close()
            elif row is None:
                print("Este libro no existe!!!!!!!!!!!!!!")
            else:
                pass
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

#*********************************************************************************************************

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
        return kv

if __name__=='__main__':
    TercerParcialApp().run()