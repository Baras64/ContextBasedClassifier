import pytesseract
from PIL import Image
import re
import unicodedata

class ImageToText():

    def unicode_to_ascii(self, s):
        return ''.join(c for c in unicodedata.normalize('NFD', s)
                       if unicodedata.category(c) != 'Mn')

    def preprocess(self, w):
        w = self.unicode_to_ascii(w.lower().strip())
        w = re.sub(r"([?.!,¿,%])", r" \1 ", w)
        w = re.sub(r'[" "]+', " ", w)
        w = re.sub(r"newlinechar", "", w)
        w = re.sub(r"[^a-zA-Z?.!,¿]+", " ", w)
        w = w.rstrip().strip()

        return w

    def parse(self, path):
        pytesseract.pytesseract.tesseract_cmd = (r'C:\Users\HARSHAVARDHAN A\AppData\Local\Tesseract-OCR\tesseract.exe')
        path = pytesseract.image_to_string(
            Image.open(path))
        print(path)
        path1 = re.sub(r'\n', ' ', path)
        path1 = path1.split('.')
        print(path1)

        paths = []

        for path_ in path1:
            i = self.preprocess(path_)
            print(i)
            paths.append(i)

        app = []

        for i in paths:
            if 'if' in i or 'else' in i:
                app.append(i)

        print(app)
        print(len(app))
        return (self.predicting(app), app)

    def predicting(self, lists):
        import model_load
        pred_list = []
        for element in lists:
            pred_list.append(model_load.Model().predicton(element)[0][0])
        print(pred_list)
        return pred_list

if __name__ == "__main__":
    ImageToText().parse(r"C:\Users\HARSHAVARDHAN A\PycharmProjects\TsecHacks\whatsapplmao.jpeg")
