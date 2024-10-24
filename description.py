from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup


class Description(BoxLayout):
    pass
class SelectionDate(BoxLayout):
    def __init__(self,**kwargs):
        super(SelectionDate,self).__init__(**kwargs)
    def focus_next(self, instance):
        instance.focus = True

class Validation1(FloatLayout):
    def __init__(self,**kwargs):
        super(Validation1,self).__init__(**kwargs)
    def valider(self):
        app = App.get_running_app()
        chemin_depart=app.manager.ids.description.ids.selectiondepartdestination.ids.depart
        chemin_destination=app.manager.ids.description.ids.selectiondepartdestination.ids.destination
        self.depart=''
        self.destination=''
        departs=[chemin_depart.ids.antananarivo,chemin_depart.ids.fianarantsoa,chemin_depart.ids.toliara]
        destinations = [chemin_destination.ids.antananarivo, chemin_destination.ids.fianarantsoa, chemin_destination.ids.toliara]
        self.date = app.manager.ids.description.ids.selectiondate
        self.jour = self.date.ids.jour.text
        self.mois = self.date.ids.mois.text
        self.annee = self.date.ids.annee.text
        chemin_heure = app.manager.ids.description.ids.selectionheure
        heures = [chemin_heure.ids.heure1, chemin_heure.ids.heure2,chemin_heure.ids.heure3]
        for depart in departs:
            if depart.state == 'down':
                self.depart = depart.text
        for destination in destinations:
            if destination.state == 'down':
                self.destination = destination.text
        if self.depart == '':self.erreur("Aucun Depart séléctionné",300)
        elif self.destination =='':self.erreur("aucune destination séléctionnée",300)
        elif self.depart==self.destination:self.erreur("le depart ne peut pas être le\n  même que la destination",300)
        else:
            app.manager.depart =self.depart
            app.manager.destination = self.destination
            app.manager.table = self.depart+self.destination
            if self.jour=='' or  not 0<int(self.jour)<=31:
                self.erreur("Jour invalide",350)
                self.suppr("jour")
            elif self.mois=='' or not 0<int(self.mois)<=12:
                self.erreur("mois invalide",350)
                self.suppr('mois')
            elif self.annee=='' or not 2023<int(self.annee)<=2100:
                self.erreur("année invalide",300)
                self.suppr("annee")
            elif int(self.mois)==2 and self.bissextile(self.annee) and int(self.jour)>28:
                self.erreur("le mois est bissextile",300)
                self.suppr('jour')
            elif int(self.mois)==2 and (not self.bissextile(self.annee)) and int(self.jour)>29:
                self.erreur("c'est le mois de fevrier",300)
                self.suppr('jour')
            else:
                for heure in heures:
                    if heure.state=='down':
                        self.heure = heure.text
                        print(self.heure)
                        app.manager.date_heure = f'{self.jour}-{self.mois}-{self.annee} {self.heure}'
                        #print(app.manager.table + '\n' + app.manager.date_heure)
                        Window.set_system_cursor('wait')
                        app.manager.ids.show.ids.boxlayoutshow.ids.showw.show()


                        #self.on_button_click()
                        app.manager.push("show")
                        Window.set_system_cursor('arrow')
                        self.suppr('jour')
                        self.suppr('mois')
                        self.suppr('annee')
                        for depart in [App.get_running_app().manager.ids.description.ids.selectiondepartdestination.ids.depart.ids.antananarivo,App.get_running_app().manager.ids.description.ids.selectiondepartdestination.ids.depart.ids.fianarantsoa,App.get_running_app().manager.ids.description.ids.selectiondepartdestination.ids.depart.ids.toliara]:depart.state="normal"
                        for destination in [App.get_running_app().manager.ids.description.ids.selectiondepartdestination.ids.destination.ids.antananarivo,App.get_running_app().manager.ids.description.ids.selectiondepartdestination.ids.destination.ids.fianarantsoa,App.get_running_app().manager.ids.description.ids.selectiondepartdestination.ids.destination.ids.toliara]:destination.state='normal'
                        for heure in [app.manager.ids.description.ids.selectionheure.ids.heure1,app.manager.ids.description.ids.selectionheure.ids.heure2,app.manager.ids.description.ids.selectionheure.ids.heure3]:heure.state='normal'
                        break
                else:
                    self.erreur("aucune heure séléctionnée",300)


    """def on_button_click(self):
        Window.set_system_cursor('wait')
        Clock.schedule_once(self.reset_cursor,3)
    def reset_cursor(self,*args):
        Window.set_system_cursor('arrow')"""










    def erreur(self, text, width):
        contenu = BoxLayout(orientation='vertical')
        contenu.add_widget(Label(text=text))
        btn = Button(text='d\'accord...', size_hint=(.5, 1), pos_hint={'center_x': 0.5, 'y': 0})
        contenu.add_widget(btn)
        popup = Popup(title="Erreur", content=contenu, size_hint=(None, None), size=(width, 200))
        popup.open()
        btn.bind(on_press=popup.dismiss)
    def suppr(self,instance):
        App.get_running_app().manager.ids.description.ids.selectiondate.ids[instance].text = ''
        App.get_running_app().manager.ids.description.ids.selectiondate.ids[instance].hint_text = instance+'...'
    def bissextile(self,annee):

        if int(annee) % 100 == 0:
            if int(annee) % 400 == 0:
                return True
            else:
                return False
        elif int(annee) % 4 == 0:
            return True
        else:
            return False
