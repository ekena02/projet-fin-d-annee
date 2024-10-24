from kivy.uix.screenmanager import ScreenManager


class NavigationScreenManager(ScreenManager):
    screen_stack=[]

    def push(self,screen):
        self.screen_stack.append(self.current)
        self.current=screen
        self.transition.direction='left'

    def pop(self):
        self.current = self.screen_stack[-1]
        del self.screen_stack[-1]
        self.transition.direction = "right"
