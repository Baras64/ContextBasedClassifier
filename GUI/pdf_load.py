from kivy.app import App
from kivy.uix.screenmanager import Builder, Screen, ScreenManager
import os
from GUI.image_to_text import ImageToText
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
class MainScreen(Screen):
    def load(self, path, selection):
        print(path, selection)
        pred_lists, app = ImageToText().parse(selection[0])
        MainScreen.clear_widgets(self)
        img = Image(source=selection[0])
        bd = BoxLayout(orientation='vertical')
        bd.add_widget(img)
        string = ""
        for element in app:
            string = string +'>'+element+'\n'
        text = TextInput(text=string, readonly=True)
        bd.add_widget(text)
        avg = sum(pred_lists)/len(pred_lists)
        t = "It belongs to the If-Else Chapter" if avg>0.5 else "It does not belong to the If-Else Chapter"
        string2 = f"Since the probability of the document belonging to the If-Else Chapter is {avg}\n"+t
        text2 = TextInput(text=string2, readonly=True)
        bd.add_widget(text2)
        self.add_widget(bd)

presentation = Builder.load_file('pdf_load.kv')

class PdfLoad(App):
    def build(self):
        return presentation

if __name__ == "__main__":
    PdfLoad().run()