from kivy.app import App
from kivy.uix.screenmanager import Builder, Screen, ScreenManager
import os
from GUI.image_to_text import ImageToText
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
import model_load

class MainScreen(Screen):
    def load(self, path, selection):
        print(selection[0])
        temp = []
        with open(selection[0], 'r') as f:
            temp = f.readlines()
        print(temp)
        #Pass temp to predict
        MainScreen.clear_widgets(self)
        bd = BoxLayout(orientation='vertical')
        for i in temp:
            texts = model_load.Model().predicton(str(i))
            print(texts[0][0])
            t = TextInput(text=str(texts[0][0]), readonly=True)
            bd.add_widget(t)
        self.add_widget(bd)

presentation = Builder.load_file('txt_load.kv')

class TxtLoad(App):
    def build(self):
        return presentation

if __name__ == "__main__":
    TxtLoad().run()