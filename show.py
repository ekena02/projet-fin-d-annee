import json
import sqlite3

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel


class Show(TabbedPanel):
    def __init__(self,**kwargs):
        super(Show,self).__init__(**kwargs)
    def show(self):
        app = App.get_running_app()
        self.table=f"\'{app.manager.table} {app.manager.date_heure}"
        conn = sqlite3.connect('reservation.db')
        c = conn.cursor()
        c.execute(f"""
                               CREATE TABLE IF NOT EXISTS {self.table}\'(
                               id INTEGER PRIMARY KEY,
                               num_place TEXT,
                               id_nom INTEGER)
                       """)
        c.execute(f'SELECT num_place, id_nom FROM {self.table}\'')
        rows = c.fetchall()
        #print(rows)
        for row in rows:
            lists_deserial = json.loads(row[0])
            for list_deserial in lists_deserial:
                self.ajouter(int(list_deserial),int(row[1]))
        conn.commit()
        conn.close()
        print(self.table)
        app.manager.tabletemp = self.table+'temp\''
        conn = sqlite3.connect('reservation.db')
        c = conn.cursor()
        c.execute(f"""
                            CREATE TABLE IF NOT EXISTS {self.table}temp\'(
                            num_place INTEGER, id INTEGER)
                            """)
        conn.commit()
        conn.close()
        App.get_running_app().manager.ids.show.ids.boxlayoutshow.ids.show1.ids.showvoiture1.afficher()
        App.get_running_app().manager.ids.show.ids.boxlayoutshow.ids.show2.ids.showvoiture2.afficher()
        App.get_running_app().manager.ids.show.ids.boxlayoutshow.ids.show3.ids.showvoiture3.afficher()
        App.get_running_app().manager.ids.show.ids.pageliste.afficher()
    def ajouter(self,num_place,id):
        conn = sqlite3.connect('reservation.db')
        c = conn.cursor()
        c.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.table}temp\'(
                    num_place INTEGER, id INTEGER)
                    """)
        c.execute(f"""
                    INSERT INTO {self.table}temp\' VALUES(?,?)
                    """,(num_place, id))
        c.execute(f'SELECT * from {self.table}temp\'')
        print(c.fetchall())
        conn.commit()
        conn.close()
    def effacer(self):
        conn = sqlite3.connect('reservation.db')
        c = conn.cursor()
        try:
            c.execute(f'DROP TABLE {App.get_running_app().manager.tabletemp}')
        except:
            print(f'la table {App.get_running_app().manager.tabletemp} n\'existe pas encore')
        conn.commit()
        conn.close()
        App.get_running_app().manager.ids.show.ids.boxlayoutshow.ids.show1.ids.showvoiture1.effacer()
        App.get_running_app().manager.ids.show.ids.boxlayoutshow.ids.show2.ids.showvoiture2.effacer()
        App.get_running_app().manager.ids.show.ids.boxlayoutshow.ids.show3.ids.showvoiture3.effacer()
        App.get_running_app().manager.ids.show.ids.pageliste.effacer()



class PageListe(BoxLayout):
    def __init__(self,**kwargs):
        super(PageListe,self).__init__(**kwargs)
    def afficher(self):
        print('PageListe')
        app = App.get_running_app()
        listes_id = []
        self.listes=[]
        listes_recuperees = app.manager.liste_voiture1 + app.manager.liste_voiture2 + app.manager.liste_voiture3
        for liste_recuperee in listes_recuperees:
            if liste_recuperee not in listes_id:listes_id.append(liste_recuperee)
        listes_id.sort()

        print(listes_recuperees)
        for liste in listes_id:
            row = self.recuperer(liste)
            text= f"{row[0]%100} : {row[2]} | cin:{row[3]} | tel:{row[4]}"
            #self.listes.append(Label(text = text,color=(0,0,0),size_hint=(1,1),text_size=(None,None)))
            self.listes.append(Label(text=text, color=(0, 0, 0),size_hint_y=None,height=30))
            #self.listes[-1].bind(size= self.adjust_text_size)
            self.add_widget(self.listes[-1])
    def adjust_text_size(self,instance,value):
        instance.text_size = instance.size
    def effacer(self):
        try:
            for liste in self.listes:
                self.remove_widget(liste)
            self.listes.clear()
        except:print('rien')


    def recuperer(self,id):
        table = App.get_running_app().manager.table
        conn = sqlite3.connect('reservation.db')
        c = conn.cursor()
        c.execute(f"SELECT id, nom, prenom ,cin, tel FROM {table} WHERE id=? ",(id,))
        row = c.fetchone()
        conn.commit()
        conn.close()
        return row
