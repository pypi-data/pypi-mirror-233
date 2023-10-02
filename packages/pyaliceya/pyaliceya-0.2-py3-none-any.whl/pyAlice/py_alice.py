"""

PyAlice v0.2

"""



import datetime, json

from pyAlice.base import Base
from pyAlice.key_word import KeyWord
from pyAlice.errors.errors import SettingsErrors, KeyWordsErrors
from pyAlice.functions import new_settings_is_valid, clear_console, from_str_bool_to_py_bool


class PyAlice(Base):
    def __init__(self, params_alice, settings):
        """
        Create a new PyAlice
        """
        clear_console()

        self.params_alice = params_alice if type(params_alice) is dict else json.loads(params_alice)
        self.start_time = datetime.datetime.now()

        settings_is_valid = new_settings_is_valid(settings)
        if settings_is_valid != "success":
            raise SettingsErrors(settings_is_valid, language=settings.DEBUG_LANGUAGE)
        self.settings = settings
        self.add_log("configuration_options_log", color="yellow", start_time=self.start_time)

        self.__processing_params()
        self.conversion_buttons()


    def init_key_word(self):
        try:
            if self.settings.TEXT_FOR_KEY_WORDS in self.params_alice["request"].keys():
                text_for_key_words = self.params_alice["request"][self.settings.TEXT_FOR_KEY_WORDS]
            elif "nlu" in self.params_alice["request"].keys():
                text_for_key_words = " ".join(self.params_alice["request"]["nlu"]["tokens"])
            else:
                text_for_key_words = ""
            key_words = KeyWord(text=text_for_key_words, settings=self.settings, start_time=self.start_time).key_word()
            if key_words["key_words"] == []:
                self.add_log("key_word_not_found_log", color="green", start_time=self.start_time)
            else:
                self.key_words = key_words["key_words"]
                self.add_messages(key_words["messages"], where="KeyWords")
                for item in key_words["events"]:
                    self.add_event({"event":item}, "KeyWord")
                self.add_buttons(key_words["buttons"])
                self.add_log("key_word_log", color="green", start_time=self.start_time)
        except KeyWordsErrors as exc:
            raise


    def __processing_params(self):
        self.add_buttons(self.settings.CONSTANT_BUTTONS)

        if self.settings.SOURCE_TEXT in self.params_alice["request"].keys():
            self.came_message = self.params_alice["request"][self.settings.SOURCE_TEXT]
        elif "nlu" in self.params_alice["request"].keys():
            self.came_message = " ".join(self.params_alice["request"]["nlu"]["tokens"])
        else:
            self.came_message = ""

        temp_new = from_str_bool_to_py_bool(self.params_alice["session"]["new"])
        if temp_new != -1:
            self.new = temp_new
        else:
            raise SettingsErrors("new_boolean_setting_error", language=self.settings.DEBUG_LANGUAGE)
        self.intents = self.params_alice["request"]["nlu"]["intents"]

        if self.params_alice.get("state") is not None:
            self.storage = self.params_alice["state"]["session"]
            self.add_log("storage_fill", color="green", start_time=self.start_time)
            self.add_event({
                            "event": "storageFillEvent",
                            "storage": self.storage
                            }, "__init__")
        else:
            self.add_log("storage_not_fill", color="yellow", start_time=self.start_time)
        
        if self.new:
            self.add_message(self.settings.STARTING_MESSAGE)
            self.add_buttons(self.settings.STARTING_BUTTONS)
            self.add_log("first_starting_end", color="green", start_time=self.start_time)
            return
        
        self.init_key_word()
    
    def get_params_for_alice(self, type="json"):
        """
        Get parameters for the alice
        """
        self.conversion_buttons()
        params_for_alice = {
            "state": {
                "session": self.storage
            },
            "session_state": self.storage,
            'version': self.params_alice['version'],
            'session': self.params_alice['session'],
            'response': {
                "buttons": self.alice_buttons,
                'text': self.result_message,
                'end_session': self.end_session
            },
        }
        if self.more_data_message != {}:
            for key, value in self.more_data_message.items():
                params_for_alice["response"][key] = value
        if type == "json":
            return json.dumps(params_for_alice)
        elif type == "dict":
            return params_for_alice
    
    def end_session_alice(self):
        self.end_session = True
        self.add_log("session_end", color="purple", start_time=self.start_time)

#