import googletrans
from googletrans import Translator
from google_trans_new import google_translator
from textblob import TextBlob
from translate import Translator as trans
import goslate
from time import sleep

class MTS(object):

    def __init__(self):
        # translator Initiated
        self.__translator = Translator()
        self.__google_translator = google_translator()   
        self.sleep_time = 0.5     
        print("Translator Initiated")

    def _translator(self, _text = None, _lang="en"):
        if _text == None:
            return None
        print("Translating...")
        txtBlob = TextBlob(_text)
        _text = str(txtBlob.correct())        
        sleep(self.sleep_time) #short Time
        try:
            _translated = self.__translator.translate(_text, dest=_lang)
            sleep(self.sleep_time) #short Time
            _translated = self.__translator.translate(_text, dest="en")
            _text = _translated.text
        except:
            try:
                _text = self.__google_translator.translate(
                    _text, lang_tgt=_lang)
                sleep(self.sleep_time) #short Time
                _text = self.__google_translator.translate(
                    _text, lang_tgt="en")
            except:
                try:
                    _gs = goslate.Goslate()                    
                    _text = _gs.translate(_text, 'en')
                except:
                    try:
                        _translator = trans(to_lang="en")
                        _text = _translator.translate(_text)        
                    except:
                        try:
                            _text = str(txtBlob.translate(to='en'))    
                        except:
                            _text = None
        _text = str(txtBlob.correct())
        print("Translating Completed.")
        return _text
