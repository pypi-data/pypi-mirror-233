import os
from sys import platform

def new_settings_is_valid(new_settings):
    if type(new_settings.EVENTS) != bool:
        return "events_setting_error"
    if type(new_settings.DEBUG) != bool:
        return "debug_setting_error"
    if new_settings.TEXT_FOR_KEY_WORDS != "command" and new_settings.TEXT_FOR_KEY_WORDS != "original_utterance":
        return "text_for_key_word_setting_error"
    if new_settings.STARTING_MESSAGE is None:
        return "starting_dialog_setting_error"
    if new_settings.SOURCE_TEXT is None and (new_settings.SOURCE_TEXT != "commands" or new_settings.SOURCE_TEXT != "original_utterance"):
        return "source_text_setting_error"
    return "success"


def end_alice_event(event, cls):
    cls.end_session_alice()

def clear_console():
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        os.system("clear")
    elif platform == "win32":
        os.system("cls") 

def from_str_bool_to_py_bool(boolean):
    if type(boolean) is str:
        if boolean == "true":
            return True
        elif boolean == "false":
            return False
    elif type(boolean) is bool:
        return boolean
    return -1


def pass_fun(*args, **kwargs):
    pass