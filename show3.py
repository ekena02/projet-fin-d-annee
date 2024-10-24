import sqlite3

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel


class Show3(BoxLayout):
    pass
class ShowVoiture3(GridLayout):
    def __init__(self,**kwargs):
        super(ShowVoiture3,self).__init__(**kwargs)
        self.cols = 3
        self.btns=[]
        self.listes=[]
        self.background_color=(.3,.8,.6)
        self.height_label = 30
        for i in range(15):
            self.btns.append(Button(text="Vide",disabled=True,background_color=self.background_color))
            self.add_widget(self.btns[-1])
    def afficher(self):
        self.btns[0].background_color = self.btns[1].background_color = (0, 0, 0, 0)
        self.btns[0].text = self.btns[1].text = ''
        self.liste = App.get_running_app().manager.ids.show.ids.boxlayoutshow.ids.show3.ids.liste
        id_nom = []
        app = App.get_running_app()
        print("tonge")
        print(App.get_running_app().manager.tabletemp)
        conn = sqlite3.connect('reservation.db')
        c = conn.cursor()
        c.execute(f"SELECT * FROM {app.manager.tabletemp} ORDER BY id")
        rows = c.fetchall()
        conn.commit()
        conn.close()
        self.labels_layout = BoxLayout(orientation='vertical',size_hint_y=None)
        self.complement = BoxLayout(size_hint=(1, 1))
        for row in rows:
            if row[0]//15==2:
                self.btns[row[0]%15].text = str(row[1]%100)
                self.btns[row[0]%15].background_color = (.9,.2,.3)
                if row[1] not in id_nom:
                    id_nom.append(row[1])
                    info_pers = self.info_pers(id_nom[-1])
                    self.listes.append(Label(text=f'{info_pers[3]%100} : {info_pers[0]}  {info_pers[1]}',size_hint_y=None,height=self.height_label,halign='left',valign='middle'))
                    self.listes[-1].bind(size=self.listes[-1].setter('text_size'))
                    #self.listes[-1].bind(size = self.adjust_text_size)
                    self.labels_layout.add_widget(self.listes[-1])
                    #liste.add_widget(Label(text=info_pers))
                    #print(info_pers)
        self.labels_layout.height = len(self.listes)*self.height_label
        self.liste.add_widget(self.labels_layout)
        self.liste.add_widget(self.complement)
        app.manager.liste_voiture3 = id_nom
    def adjust_text_size(self,instance,value):
        instance.text_size=instance.size
    def info_pers(self,id):
        app = App.get_running_app()
        conn=sqlite3.connect('reservation.db')
        c = conn.cursor()
        c.execute(f"""SELECT dd.nom,dd.prenom,dd.tel,dd.id 
                    FROM {app.manager.table} AS dd INNER JOIN 
                    {app.manager.tabletemp} 
                    AS ddtemp WHERE ddtemp.id=dd.id and dd.id=?""",(id,))

        info_pers = c.fetchone()
        conn.commit()
        conn.close()
        #print(info_pers)
        #print(app.manager.tabletemp,app.manager.table)

        return info_pers
    def effacer(self):
        """for liste in self.listes:
            self.liste.remove_widget(liste)
        self.listes.clear()"""
        try:
            self.liste.remove_widget(self.labels_layout)
            self.liste.remove_widget(self.complement)
            for btn in self.btns:
                btn.text='Vide'
                btn.background_color=(self.background_color)
        except:
            pass
class Liste(BoxLayout):
    def __init__(self,**kwargs):
        super(Liste,self).__init__(**kwargs)

