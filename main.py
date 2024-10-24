from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import *
from kivy_deps import sdl2, glew
#from departdestination import Depart_Destination
from navigationScreenManager import NavigationScreenManager
import os
Builder.load_file('formulaire.kv')
Builder.load_file('place.kv')
Builder.load_file('ticket.kv')
Builder.load_file('accueil.kv')
Builder.load_file('description.kv')
Builder.load_file('departdestination.kv')
Builder.load_file("show.kv")
Builder.load_file("show1.kv")
Builder.load_file("show2.kv")
Builder.load_file("show3.kv")
Builder.load_file("annulation.kv")
"""current_dir = os.path.dirname(__file__)

# Charger tous les fichiers .kv dans le répertoire
kv_files = [f for f in os.listdir(current_dir) if f.endswith('.kv')]
for kv_file in kv_files:
    kv_file_path = os.path.join(current_dir, kv_file)
    Builder.load_file(kv_file_path)
print('chargement du fichier: '+str(kv_files))
"""



class MyScreenManager(NavigationScreenManager):
    depart=StringProperty(None)
    destination=StringProperty(None)
    table= StringProperty(None)
    nom = StringProperty(None)
    prenom = StringProperty(None)
    cin = StringProperty()
    tel = StringProperty(None)
    date_heure=StringProperty(None)
    nb_place = NumericProperty(0)
    id = NumericProperty(0)
    list_place_serial = StringProperty(None)
    tabletemp = StringProperty(None)
    liste_voiture1 = ListProperty([])
    liste_voiture2 = ListProperty([])
    liste_voiture3 = ListProperty([])
    md_paiement = StringProperty(None)



class ReservationApp(App):
    manager=ObjectProperty(None)
    def build(self):
        self.manager = MyScreenManager()
        def prevent_resize(window,width,height):
            Window.size=(800,650)
        Window.resizable=False
        Window.bind(on_resize=prevent_resize)

        return self.manager
    def on_stop(self):
        print("l'application est sur le point de fermer")
        self.manager.ids.show.ids.boxlayoutshow.ids.showw.effacer()
        print(self.manager.ids.show.ids.boxlayoutshow.ids.showw.effacer())

if __name__=='__main__':
    ReservationApp().run()