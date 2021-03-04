from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.config import Config
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
import winsound
from kivy.uix.screenmanager import SlideTransition
import psycopg2
import datetime
x=datetime.datetime.now()

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
    codigo_result = StringProperty('')
    def on_pre_enter(self, *args): 
        self.codigo_result = self.manager.ids.Estud.codigo_1
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


class Estudiantes(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        codigo_1 = StringProperty('')

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
                            self.codigo_1 = cod
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
        
        #self.codigo_1 = 'cod'

#**********************************************************************************************************************************


class Estudiante_Externo(Estudiantes):
    #def __init__(self, **kwargs):
        #super().__init__(**kwargs)

    def nombres_externo(self):
        txt = self.ids.Nombres.text
        self.ids.Nombres_E.text = txt

    def apellidos_externo(self):
        txt = self.ids.Apellidos.text
        self.ids.Apellidos_E.text = txt

    def dni_externo(self):
        txt = self.ids.DNI.text
        self.ids.DNI_E.text = txt

    def submit(self, **kwargs):

        conn = None
        sql = """INSERT INTO libro_no_disponible (codigo) VALUES(%s);"""
        try:
            conn=psycopg2.connect(
				host="localhost",
				database="lab07",
				user="postgres",
				password="ladymendoza_prograII",
				port="5432")
            cur=conn.cursor()
            cur.execute(sql, (self.manager.ids.Estud.Codigo.text,))
            conn.commit()
            cur.close()
            if conn is not None:
                conn.close()
            print("Solicitud exitosa------------------")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error, "erroooooooooooor!!!!!!!!!")
        finally:
            if conn is not None:
                conn.close()
            
		#se envia a ficha de solicitud

        conn3 = None
        sql3 = """INSERT INTO ficha_solicitud (codigo, solicitante, fecha) VALUES(%s, %s, %s);"""

        dia=str(x.day)
        mes=str(x.month)
        año=str(x.year)
        fecha_actual=(año+"/"+mes+"/"+dia)

        try:
            conn3=psycopg2.connect(
				host="localhost",
				database="lab07",
				user="postgres",
				password="ladymendoza_prograII",
				port="5432")
            cur3=conn3.cursor()
            cur3.execute(sql3, (self.ids.Codigo.text, self.ids.DNI.text, fecha_actual,))
            conn3.commit()
            cur3.close()
            if conn3 is not None:
                conn3.close()
            print ("Solicitud exitosa*************")
        except (Exception, psycopg2.DatabaseError) as e:
            print(e, "erroooooooooooor!!!!!!!!!")
        finally:
            if conn3 is not None:
                conn3.close()

		#se envia a BASE ESTUDIANTE EXTERNO

        conn4 = None
        sql4 = """INSERT INTO estudiante_externo (dni, nombres, apellidos) VALUES(%s, %s, %s);"""
        try:
            conn4=psycopg2.connect(
				host="localhost",
				database="lab07",
				user="postgres",
				password="ladymendoza_prograII",
				port="5432")
            cur4=conn4.cursor()
            cur4.execute(sql4, (self.ids.DNI.text, self.ids.Nombres.text, self.ids.Apellidos.text,))
            conn4.commit()
            cur4.close()
            if conn4 is not None:
                conn4.close()
            print("Solicitud exitosa///////////////")
        except (Exception, psycopg2.DatabaseError) as e:
            print(e, "erroooooooooooo")
        finally:
            if conn4 is not None:
                conn4.close()

    def datos_base(self):
        self.submit()

    ###*******************

    def next(self, *args):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = self.manager.next()
        App.get_running_app().root.current = "pantalla1"


#**********************************************************************************************************************************

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