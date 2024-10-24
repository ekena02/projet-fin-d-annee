import json
import sqlite3

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.window import Window

class Formulaire(BoxLayout):
    def __init__(self, **kwargs):
        super(Formulaire, self).__init__(**kwargs)
        self.heure=None
    def valider(self):
        self.formulaire = self.ids.leformulaire.ids.lacompletion
        nom = self.formulaire.ids.nom.text.upper()
        prenom = self.formulaire.ids.prenom.text.title()
        cin = self.formulaire.ids.cin.text
        tel = self.formulaire.ids.tel.text
        jour = self.formulaire.ids.jour.text
        mois = self.formulaire.ids.mois.text
        annee = self.formulaire.ids.annee.text
        nb_place = self.formulaire.ids.nb_place.text
        if not nom.replace(" ","").isalpha():
            self.erreur('le nom ne doit contenir que\n des lettres et des espaces', 300)
            self.suppr("nom")
        elif not (prenom.replace(" ", "").isalpha()):
            self.erreur('le prénom ne doit contenir que\n des lettres et des espaces',300)
            self.suppr('prenom')
        elif not (cin.isdigit and len(cin) == 12):
            self.erreur("CIN incorrect",150)
            self.suppr('cin')
        elif not (tel.isdigit and len(tel) == 10):
            self.erreur("tel incorrect",150)
            self.suppr('tel')
        elif not (1 <= int(jour) <= 31 and 1 <= int(mois) <= 12 and int(annee) >= 2024):
            self.erreur("date incorrect",100)
            self.suppr("jour")
            self.suppr("mois")
            self.suppr("annee")        #elif not self.heure():
         #   print("aucune heure de départ séléctionnée")
        elif not self.heuree():
            self.erreur("aucune heure de départ séléctionné",300)
        elif not (nb_place.isdigit() and 0<int(nb_place)<10):
            self.erreur("nombre de places hors limite",300)
            self.suppr('nb_place')
        elif not self.paiement():
            self.erreur("aucun mode de paiement séléctionné",350)
        else:
            app = App.get_running_app().manager
            app.nb_place = nb_place
            app.nom = nom
            app.prenom = prenom
            app.cin = cin
            app.tel = tel
            date_heure = f'{jour}-{mois}-{annee} {self.heure}'
            app.date_heure = date_heure
            app.md_paiement=self.md_paiement
            self.enregistrer(nom,prenom,cin,tel,date_heure,nb_place)
            app.push('screen3')
            self.lists_deserial = self.recuperer()
            print(self.lists_deserial)
            self.places_occupees(self.lists_deserial)


    def capture_screen(self, instance):
        # Capture l'écran et sauvegarde l'image
        Window.screenshot('screenshot.png')
        print("Capture d'écran enregistrée sous 'screenshot.png'")

    def paiement(self):
        if self.formulaire.ids.chbx1.active:
            self.md_paiement = self.formulaire.ids.label1.text
            return True
        elif self.formulaire.ids.chbx2.active:
            self.md_paiement = self.formulaire.ids.label2.text
            return True
        else:
            self.md_paiement=''
            return False
    def heuree(self):
        t = 0
        for button in [self.formulaire.ids.heure1, self.formulaire.ids.heure2, self.formulaire.ids.heure3]:
            if button.state == 'down':
                self.heure = button.text
                print(self.heure)
                break
            else:
                t += 1
        return not t == 3

    def enregistrer(self, nom, prenom, cin, tel, date_heure, nb_place):
        conn = sqlite3.connect("reservation.db")
        c = conn.cursor()
        app = App.get_running_app().manager
        c.execute(f"""
                   INSERT INTO {app.table} (nom,prenom, cin, tel, date_heure, nb_place,md_paiement)VALUES(
                   ?,?,?,?,?,?,?) 
                    """, (nom, prenom,cin,tel,date_heure,nb_place,self.md_paiement))

        app.id=c.lastrowid
        conn.commit()
        conn.close()

        conn = sqlite3.connect("reservation.db")
        c = conn.cursor()
        app = App.get_running_app().manager

        table='\"'+app.table+' '+app.date_heure+'\"'

        c.execute(f"""
                        CREATE TABLE IF NOT EXISTS  {'\"'+app.table+' '+app.date_heure+'\"'} (
                        id INTEGER PRIMARY KEY,
                        num_place TEXT,
                        id_nom INTEGER)
                """)
        conn.commit()
        conn.close()

    def recuperer(self):
        conn = sqlite3.connect('reservation.db')
        c = conn.cursor()
        app = App.get_running_app().manager
        c.execute(f"""
                   SELECT num_place FROM {'\"'+app.table+' '+app.date_heure+'\"'}     
                  """)
        lists_serial = c.fetchall()
        conn.commit()
        conn.close()

        list_deserial_en_un = []
        for list_serial in lists_serial:
            list_deserial_en_un += json.loads(list_serial[0])
        return list_deserial_en_un
    def returne(self):
        self.heure=None
    def reinitialiser(self,boutons):
        for i in range(45):
            boutons[i].disabled=False
            boutons[i].state = 'normal'
            if i%15==0 or i%15==1:
                boutons[i].disabled = True
                boutons[i].background_color = (0,0,0,0)
                #App.get_running_app().manager.ids.place.ids.place1.remove_widget(boutons[i])
    def reinitialize_formulaire(self):
        self.suppr('nom')
        self.suppr('prenom')
        self.suppr("cin")
        self.suppr('jour')
        self.suppr('mois')
        self.suppr('annee')
        self.suppr('tel')
        self.suppr('nb_place')
        for button in [self.formulaire.ids.heure1, self.formulaire.ids.heure2, self.formulaire.ids.heure3]:
            button.state='normal'
    def suppr(self,instance):
        self.ids.leformulaire.ids.lacompletion.ids[instance].text=''
        self.ids.leformulaire.ids.lacompletion.ids[instance].hint_text = str(instance)

    def erreur(self, text, width):
        contenu = BoxLayout(orientation='vertical')
        contenu.add_widget(Label(text=text))
        btn = Button(text='d\'accord...', size_hint=(.5, 1), pos_hint={'center_x': 0.5, 'y': 0})

        contenu.add_widget(btn)
        popup = Popup(title="Erreur", content=contenu, size_hint=(None, None), size=(width, 200))
        popup.open()
        btn.bind(on_press=popup.dismiss)
    def places_occupees(self,lists_deserial):
        place1=App.get_running_app().manager.ids.place.ids.place1
        self.reinitialiser(place1.btn)
        for list_deserial in lists_deserial:
            place1.btn[list_deserial].disabled=True
        self.reinitialize_formulaire()


class LaCompletion(BoxLayout):
    def __init__(self, **kwargs):
        super(LaCompletion, self).__init__(**kwargs)

    def focus_next(self, instance):
        instance.focus = True
