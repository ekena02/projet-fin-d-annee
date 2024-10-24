import json

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup


class Ticket(BoxLayout):
    def __init__(self,**kwargs):
        super(Ticket,self).__init__(**kwargs)
    def capturer(self):
        cin = App.get_running_app().manager.cin
        Window.screenshot(f'ImageTicket/{cin}.png')
        self.accomplissement('Ticket enregistré',200)

    def accomplissement(self, text, width):
        contenu = BoxLayout(orientation='vertical')
        contenu.add_widget(Label(text=text))
        btn = Button(text='d\'accord...', size_hint=(.5, 1), pos_hint={'center_x': 0.5, 'y': 0})

        contenu.add_widget(btn)
        popup = Popup(title="succès", content=contenu, size_hint=(None, None), size=(width, 200))
        popup.open()
        btn.bind(on_press=popup.dismiss)
class Info(BoxLayout):
    def __init__(self,**kwargs):
        super(Info,self).__init__(**kwargs)

    def show(self):
        app = App.get_running_app().manager
        self.nom=Label(text=app.nom,color=(1,.1,.4))
        self.prenom=Label(text=app.prenom,color=(1,.1,.4))
        self.nb_place=Label(text='Nombre de places: '+str(int(app.nb_place)),color=(1,.1,.4))
        self.list_deserial = json.loads(app.list_place_serial)
        self.md_paiement = Label(text=f'[i][color=#009900]$$$$$$[/color][/i]Paiement : [b][color=#4F12D3]{app.md_paiement}[/color][/b] [i][color=#009900]$$$$$$[/color][/i]',markup=True,color=(0,1,1))
        self.list_a_afficher=[]
        for l in self.list_deserial:
            text=f"----- Voiture {l//15+1} ; place num {l%15-1} -----"
            self.list_a_afficher.append(Label(text=text,font_size=20,color=(.7,.2,.6)))
        self.add_widget(self.nom)
        self.add_widget(self.prenom)
        self.add_widget(self.nb_place)
        for l_a_afficher in self.list_a_afficher:
            self.add_widget(l_a_afficher)
        self.add_widget(self.md_paiement)
        App.get_running_app().manager.ids.ticket.ids.sousticket.afficher()

    def reinitialiser(self):


        self.remove_widget(self.nom)
        self.remove_widget(self.md_paiement)
        self.remove_widget(self.prenom)
        self.remove_widget(self.nb_place)
        for l_a_afficher in self.list_a_afficher:
            self.remove_widget(l_a_afficher)
        self.parent.ids.sousticket.reinitialiser()

class SousTicket(BoxLayout):
    def __init__(self,**kwargs):
        super(SousTicket,self).__init__(**kwargs)

    def afficher(self):

        self.depart=App.get_running_app().manager.depart
        self.destination = App.get_running_app().manager.destination
        self.date_heure = App.get_running_app().manager.date_heure.split()
        self.date = self.date_heure[0]
        self.heure = self.date_heure[1]
        self.departdestination = Label(text=f'de {self.depart} à {self.destination}',color=(.5,.5,0),font_size=20)
        self.dateheure = Label(text=f'le {self.date} à {self.heure}',color=(.5,.5,0),font_size=20)
        self.add_widget(self.departdestination)
        self.add_widget(self.dateheure)


    def reinitialiser(self):
        self.remove_widget(self.departdestination)
        self.remove_widget(self.dateheure)


