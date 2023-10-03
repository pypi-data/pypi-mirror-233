# noinspection PyUnresolvedReferences
"""Module for speech recognition listener.

>>> Listener

"""
from typing import Union

from playsound import playsound
from pydantic import PositiveFloat, PositiveInt
from speech_recognition import (Microphone, Recognizer, RequestError,
                                UnknownValueError, WaitTimeoutError)

from jarvis.modules.exceptions import EgressErrors
from jarvis.modules.logger import logger
from jarvis.modules.models import models
from jarvis.modules.utils import support

recognizer = Recognizer()
microphone = Microphone(device_index=models.env.microphone_index)

if models.settings.pname == "JARVIS":
    recognizer.energy_threshold = models.env.recognizer_settings.energy_threshold
    recognizer.pause_threshold = models.env.recognizer_settings.pause_threshold
    recognizer.phrase_threshold = models.env.recognizer_settings.phrase_threshold
    recognizer.dynamic_energy_threshold = models.env.recognizer_settings.dynamic_energy_threshold
    recognizer.non_speaking_duration = models.env.recognizer_settings.non_speaking_duration


def listen(sound: bool = True,
           timeout: Union[PositiveInt, PositiveFloat] = models.env.listener_timeout,
           phrase_time_limit: Union[PositiveInt, PositiveFloat] = models.env.listener_phrase_limit) -> Union[str, None]:
    """Function to activate listener, this function will be called by most upcoming functions to listen to user input.

    Args:
        sound: Flag whether to play the listener indicator sound. Defaults to True unless set to False.
        timeout: Custom timeout for functions expecting a longer wait time.
        phrase_time_limit: Custom time limit for functions expecting a longer user input.

    Returns:
        str:
         - Returns recognized statement from the microphone.
    """
    with microphone as source:
        try:
            playsound(sound=models.indicators.start, block=False) if sound else None
            support.write_screen(text=f"Listener activated [{timeout}: {phrase_time_limit}]")
            listened = recognizer.listen(source=source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            playsound(sound=models.indicators.end, block=False) if sound else None
            support.flush_screen()
            recognized = recognizer.recognize_google(audio_data=listened)
            logger.info(recognized)
            return recognized
        except (UnknownValueError, RequestError, WaitTimeoutError):
            return
        except EgressErrors as error:
            logger.error(error)
