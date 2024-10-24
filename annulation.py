import json
import sqlite3

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup


class Annulation(BoxLayout):
    def __init__(self,**kwargs):
        super(Annulation,self).__init__(**kwargs)
        self.orientation='vertical'
    def valider(self):
        app = App.get_running_app()
        self.annulation=app.manager.ids.annulation
        chemin_depart = self.annulation.ids.selectiondepartdestination.ids.depart
        chemin_destination = self.annulation.ids.selectiondepartdestination.ids.destination
        self.heuree = self.annulation.ids.selectionheure
        self.heure = ''
        self.depart = ''
        self.destination=''
        date = ''
        self.voiture = self.annulation.ids.voitureplace.ids.num_voiture.text
        self.dddateheure=''
        self.place = self.annulation.ids.voitureplace.ids.num_place.text
        print(self.place)
        self.jour=self.annulation.ids.selectiondate.ids.jour.text
        print(self.jour)
        self.mois = self.annulation.ids.selectiondate.ids.mois.text
        print(self.mois)
        self.annee = self.annulation.ids.selectiondate.ids.annee.text
        cin = self.annulation.ids.cin.text
        self.heure =''
        print(cin)
        departs = [chemin_depart.ids.antananarivo,chemin_depart.ids.fianarantsoa,chemin_depart.ids.toliara]
        destinations = [chemin_destination.ids.antananarivo, chemin_destination.ids.fianarantsoa, chemin_destination.ids.toliara]
        for depart in departs:
            if depart.state == 'down':
                self.depart = depart.text
            for destination in destinations:
                if destination.state =='down':
                    self.destination = destination.text
        if self.depart == '':
            self.erreur('Aucun depart séléctionné')
        elif self.destination=='':
            self.erreur('Aucune destination séléctionnée')
        elif self.destination==self.depart:
            self.erreur('le depart ne peut pas être le même\n      que la destination')
        elif not len(cin)==12:
            self.erreur('CIN invalide')
        elif not (self.jour.isdigit() and 0<int(self.jour)<31):
            self.erreur('jour invalide')
        elif not 0<int(self.mois)<12:
            self.erreur('mois invalide')
        elif int(self.annee)<2024:
            self.erreur('année invalide')
        elif self.voiture not in ['1','2','3']:
            self.erreur('numéro de voiture invalide')
        elif not (self.place.isdigit() and 0<int(self.place)<14):
            self.erreur('numero de place invalide')
        else:
            for heure in [self.heuree.ids.heure1, self.heuree.ids.heure2, self.heuree.ids.heure3]:
                if heure.state == 'down':
                    self.heure = heure.text
                    break
            else:
                self.heure=''
            if self.heure=='':
                self.erreur("aucune heure séléctionnée")
            else:

                self.date =f'{self.jour}-{self.mois}-{self.annee}'
                self.dateheure=f'{self.date} {self.heure}'
                self.dddateheure = f'{self.depart}{self.destination} {self.dateheure}'
                self.effacer(cin,self.voiture, self.place)
                #print(self.dddateheure)





    def erreur(self, text, width=300):
        contenu = BoxLayout(orientation='vertical')
        contenu.add_widget(Label(text=text))
        btn = Button(text='d\'accord...', size_hint=(.5, 1), pos_hint={'center_x': 0.5, 'y': 0})
        contenu.add_widget(btn)
        popup = Popup(title="Erreur", content=contenu, size_hint=(None, None), size=(width, 200))
        popup.open()
        btn.bind(on_press=popup.dismiss)

    def effacer(self,cin,v,p):
        conn = sqlite3.connect('reservation.db')
        c = conn.cursor()
        val = (int(v)-1)*15+(int(p)+1)
        param = f'%{str(val)}%'
        try:
            c.execute(f'SELECT num_place, id_nom FROM \'{self.depart+self.destination} {self.jour}-{self.mois}-{self.annee} {self.heure}\' WHERE num_place LIKE ?',(param,))
            req = c.fetchone()
            liste_serial=req[0]
            id = req[1]
            print(liste_serial)
            print(id)
            liste_deserial = json.loads(liste_serial)
            liste_deserial.remove(val)
            liste = json.dumps(liste_deserial)
            param = f'%{val}%'
            c.execute(f"SELECT cin FROM {self.depart+self.destination} WHERE id=?",(id,))
            if cin==c.fetchone()[0]:
                c.execute(f"UPDATE \'{self.depart+self.destination} {self.jour}-{self.mois}-{self.annee} {self.heure}\' SET num_place=? WHERE num_place LiKE ? and id_nom=? ",(liste,param,id))
                self.accomplissement("la place a été annuée\navec succès",300)
            else:
                self.erreur('le CIN ne correspond pas',300)
        except:
            self.erreur("ne figure pas dans la liste",320)
            print('le cin ne correspond pas')
        #print('liste à la fin : '+liste)
        """try:
            c.execute(f'SELECT dd.id FROM {self.depart+self.destination} AS dd INNER JOIN \'{self.depart+self.destination} {self.jour}-{self.mois}-{self.annee} {self.heure}\' AS dddh WHERE dddh.id_nom=dd.id AND cin=?',(cin,))
            id=c.fetchone()[0]
            print("id à effacer:"+str(id))
            try:
                c.execute(f'SELECT num_place FROM \'{self.depart+self.destination} {self.jour}-{self.mois}-{self.annee} {self.heure}\' WHERE id_nom=?',(id,))
                print(f"nom de a table : \'{self.depart+self.destination} {self.jour}-{self.mois}-{self.annee} {self.heure}\'")
                liste_serial = c.fetchone()[0]
                print("avant l'a suppression : " +liste_serial)
                liste_deserial = json.loads(liste_serial)
                val = int((int(v)-1)*15+(int(p)+1))
                try:
                    liste_deserial.remove(int(val))
                    print(liste_deserial)
                    liste = json.dumps(liste_deserial)
                    c.execute(f'UPDATE \'{self.depart+self.destination} {self.jour}-{self.mois}-{self.annee} {self.heure}\' SET num_place=? WHERE id=?',(liste,id))
                    print("execution réuissie")
                    print('après la suppression : '+liste)
                    Window.set_system_cursor("wait")
                    self.accomplissement("place annulée",300)
                    Window.set_system_cursor("arrow")

                except:
                    self.erreur(str(val)+' n\'est pas dans la liste')
            except:
                self.erreur('pas dans la liste')
        except:
            self.erreur('pas dans la liste')"""
        conn.commit()
        conn.close()

    def accomplissement(self, text, width):
        contenu = BoxLayout(orientation='vertical')
        contenu.add_widget(Label(text=text))
        btn = Button(text='d\'accord...', size_hint=(.5, 1), pos_hint={'center_x': 0.5, 'y': 0})

        contenu.add_widget(btn)
        popup = Popup(title="succès", content=contenu, size_hint=(None, None), size=(width, 200))
        popup.open()
        btn.bind(on_press=popup.dismiss)






class SelectionDate2(BoxLayout):
    def __init__(self,**kwargs):
        super(SelectionDate2,self).__init__(**kwargs)
    def focus_next(self,instance):
        instance.focus = True
