import sqlite3
import time

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

#Builder.load_file("departdestination.kv")
class Depart_Destination(BoxLayout):
    def __init__(self,**kwargs):
        super(Depart_Destination,self).__init__(**kwargs)
        self.destination=''
        self.depart=''
    def valider(self):
        chemin_depart=self.ids.selection.ids.depart
        chemin_destination=self.ids.selection.ids.destination
        self.departs=[chemin_depart.ids.antananarivo, chemin_depart.ids.fianarantsoa, chemin_depart.ids.toliara]
        self.destinations=[chemin_destination.ids.antananarivo, chemin_destination.ids.fianarantsoa,chemin_destination.ids.toliara]
        for depart in self.departs:
            if depart.state=='down':
                self.depart = depart.text
                App.get_running_app().manager.depart = self.depart
                break
        else:self.depart=''
            #print("aucun depart selectionné")
        for destination in self.destinations:
            if destination.state=='down':
                self.destination=destination.text
                App.get_running_app().manager.destination = self.destination
                break
        else:self.destination=''
            #print("aucune destination selectionné")
        if self.depart == '' or self.destination == '': self.erreur("Selection manquante",300)
        elif self.destination == self.depart:self.erreur("le lieu de départ ne peut pas être le même que la destination",560)
        else:
            print(f"depart:{self.depart}   ;   destination:{self.destination}")
            table=self.depart+self.destination
            App.get_running_app().manager.table=table
            conn=sqlite3.connect('reservation.db')
            c=conn.cursor()
            c.execute(f"""
                        CREATE TABLE IF NOT EXISTS {table}(
                        id INTEGER PRIMARY KEY,
                        nom TEXT,
                        prenom TEXT,
                        cin TEXT,
                        tel TEXT,
                        date_heure TEXT,
                        nb_place INTEGER,
                        md_paiement TEXT)            
                    """)
            print("table créé")
            conn.commit()
            conn.close()
            app=App.get_running_app()
            self.reinitialiser()
            app.manager.push('screen2')

    def erreur(self,text,width):
        contenu=BoxLayout(orientation='vertical')
        contenu.add_widget(Label(text=text))
        btn=Button(text='d\'accord...',size_hint=(.5,1),pos_hint={'center_x':0.5,'y':0})

        contenu.add_widget(btn)
        popup =  Popup(title="Erreur",content=contenu,size_hint=(None,None),size=(width,200))
        popup.open()
        btn.bind(on_press=popup.dismiss)

    def reinitialiser(self):
        for depart in self.departs:
            depart.state='normal'
        for destination in self.destinations:
            destination.state='normal'



