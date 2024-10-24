import json
import sqlite3

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.togglebutton import ToggleButton


class Place(BoxLayout):
    pass

class Place1(BoxLayout):
    def __init__(self,**kwargs):
        super(Place1,self).__init__(**kwargs)
        self.spacing=10
        self.orientation = 'horizontal'
        self.voiture = []
        #self.voiture.append(GridLayout(cols=3))
        self.btn=list()

        for i in range(3):
            self.voiture.append(GridLayout(cols=3))
            for j in range(15):
                self.btn.append(ToggleButton(text=str(j-1)))
                if j%15==0 or j%15==1:
                    self.btn[-1].disabled=True
                    self.btn[-1].text = ''
                self.voiture[-1].add_widget(self.btn[-1])
            self.add_widget(self.voiture[i])
        """list_serial = self.recuperer()
        list_deserial=json.loads(list_serial)
        for l in list_deserial:
            self.btn[l].state='down'
            self.btn[l].disabled=True

        #self.btn[20].disabled=True
        #self.btn[34].state = 'down'
    def recuperer(self):
        conn=sqlite3.connect('reservation.db')
        c=conn.cursor()
        app=App.get_running_app().manager
        c.execute(f
                   #SELECT num_place FROM {'\"'+app.table+' '+app.date_heure+'\"'}     
                )
        lists_serial = c.fetchall()
        conn.commit()
        conn.close()

        list_serial_en_un=[]
        for list_serial in lists_serial:
            list_serial_en_un +=list_serial
        return list_serial_en_un"""


class Valider(FloatLayout):
    def __init__(self,**kwargs):
        super(Valider,self).__init__(**kwargs)
    def valider(self):
        i=0
        inc=0
        places=list()
        list_place = []
        for btn in self.parent.ids.place1.btn:
            if btn.state=='down':
                i+=1
                places.append(inc)
            inc+=1
        app= App.get_running_app()
        if not i== app.manager.nb_place:
            self.erreur('nombre de place ne correspondant\n\t pas au nombre de selections')
            list_place.clear()
        else:
            for place in places:
                print(f"place numéro{place%15-1}, voiture {place//15+1}")
                list_place.append(place)
            list_place_serial = json.dumps(list_place)
            App.get_running_app().manager.list_place_serial = list_place_serial
            self.enregistrer()
            App.get_running_app().manager.push('screen4')
            App.get_running_app().manager.ids.ticket.ids.info.show()

    def erreur(self, text, width=300):
        contenu = BoxLayout(orientation='vertical')
        contenu.add_widget(Label(text=text))
        btn = Button(text='d\'accord...', size_hint=(.5, 1), pos_hint={'center_x': 0.5, 'y': 0})

        contenu.add_widget(btn)
        popup = Popup(title="Erreur", content=contenu, size_hint=(None, None), size=(width, 200))
        popup.open()
        btn.bind(on_press=popup.dismiss)

    def enregistrer(self):
        app=App.get_running_app().manager
        conn = sqlite3.connect('reservation.db')
        c = conn.cursor()
        c.execute(f"""
                    INSERT INTO {'\"'+app.table+' '+app.date_heure+'\"'} (num_place, id_nom) VALUES (?,?)
                    """,(app.list_place_serial,app.id))
        conn.commit()
        conn.close()

        """def __init__(self, **kwargs):
            super(Place1, self).__init__(**kwargs)
            self.spacing = 10
            self.orientation = 'horizontal'
            self.voiture = []
            # self.voiture.append(GridLayout(cols=3))
            self.btn = list()

            for i in range(3):
                self.voiture.append(GridLayout(cols=3))
                for j in range(12):
                    self.btn.append(ToggleButton(text=str(j + 1)))
                    # self.btn[-1].disabled=True
                    self.voiture[-1].add_widget(self.btn[-1])
                self.add_widget(self.voiture[i])"""








