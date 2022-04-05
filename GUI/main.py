import kivy
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen, Builder
import requests
import json

class MainScreen(Screen):
    def predict(self, api_key, text_data, prediction):
        prediction.text = ""
        URL = 'http://127.0.0.1:5000/api/'+api_key.text+'/'+text_data.text
        resjson = json.loads(requests.get(URL).text)
        reg = ['(', '{', '=', '>', '<', '}', ')']
        flag = False
        for r in reg:
            if r in text_data.text:
                flag = True
                break
        if flag:
            prediction.text = 'It is from the If-Else Chapter'
        else:
            prediction.text = resjson['predicted_text']

    def btn_touch_up(self):
        from subprocess import Popen, PIPE
        secondApp =Popen('python pdf_load.py', shell=True)
    def btn_touch_down(self):
        from subprocess import Popen, PIPE
        thirdApp = Popen('python txt_load.py', shell=True)



presentation = Builder.load_file('main.kv')

class FinalApp(App):
    def build(self):
        return presentation

if __name__ == "__main__":
    FinalApp().run()