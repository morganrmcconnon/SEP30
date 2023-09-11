from googletrans import Translator

TRANSLATOR = Translator()


def detect_and_translate_language(text, dest: str = "en", src: str = "auto"):
    """
    Detect the language of a string of text.

    Input:
    - `text`: a string of text
    - `dest`: the destination language code (default: 'en')
    - `src`: the source language code (default: 'auto')

    Output: a tuple of (`translated text`, `detected source language code`, `pronunciation`, `extra data`)
    """

    translated = TRANSLATOR.translate(text, dest="en")
    return (
        translated.text,
        translated.src,
        translated.pronunciation,
        translated.extra_data,
    )