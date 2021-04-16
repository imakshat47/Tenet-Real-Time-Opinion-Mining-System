from google_trans_new import google_translator
from googletrans import Translator
translator = Translator(service_urls=[
    'translate.google.com',
    'translate.google.co.kr',
    'translate.googleapis.com',
])


class Translate(object):
    def __init__(self):
        # translator Initiated
        self.__translator = google_translator()

    def _translate(self, text, lang="en"):
        # Text translated
        text = self.__translator.translate(text, lang_tgt=lang)
        return self.__translator.translate(text, lang_tgt="en")
