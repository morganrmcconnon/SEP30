from m3inference import M3Twitter
from m3inference.consts import UNKNOWN_LANG, LANGS
from translate_text import detect_and_translate_language

M3TWITTER = M3Twitter(
    cache_dir="./m3twitter_cache", use_full_model=False, use_cuda=True, parallel=True
)


def detect_demographics(users : list[dict]):
    """
    Detect demographics of users using the m3inference model.

    Input: a user json entry or a list of user json entries

    For each json entry, the following keys are required: `id`, `name`, `screen_name`, `description`, `lang`.
    When using the full model, the `img_path` key is also required .

    Output: a dictionary of demographics, with id as key and a dictionary of demographics as value

    Example output:
    ```
    OrderedDict([
        ('720389270335135745',
            {
                'age': {
                    '19-29': 0.1546,
                    '30-39': 0.114,
                    '<=18': 0.0481,
                    '>=40': 0.6833
                },
                'gender': {
                    'female': 0.0066, 
                    'male': 0.9934
                },
                'org': {
                    'is-org': 0.7508, 
                    'non-org': 0.2492
                }
            }
        ),
        ('21447363',
            {
                'age': {
                    '19-29': 0.0157,
                    '30-39': 0.9837,
                    '<=18': 0.0004,
                    '>=40': 0.0002
                },
                'gender': {
                    'female': 0.9866, 
                    'male': 0.0134
                },
                'org': {
                    'is-org': 0.0002, 
                    'non-org': 0.9998
                }
            }
        )
        ])
    ```
    """
    return M3TWITTER.infer(users)



def preprocess_user_object_for_m3inference(
    user: dict,
    id_key="id_str",
    name_key="name",
    screen_name_key="screen_name",
    description_key="description",
    lang_key="lang",
    use_translator_if_necessary=True
):
    """
    Preprocess a user object that is compatible with the input data structure required by the m3inference model.

    Input: a user json entry

    Output: a dictionary of user information, with the following keys: `id`, `name`, `screen_name`, `description`, `lang`

    Since m3inference only supports a number of languages, the description will be translated to English if the language code is not in the supported languages.

    Furthermore, often the language code is not set for a user. In this case, the language of the description will be detected. and translated to English if the language code is not in the supported languages.
    """
    # Initialize a new user object
    new_user = {
        "id": "",
        "name": "",
        "screen_name": "",
        "description": "",
        "lang": UNKNOWN_LANG,
    }

    # Set up values for the new user object
    new_user["id"] = user.get(id_key, "")
    new_user["name"] = user.get(name_key, "")
    new_user["screen_name"] = user.get(screen_name_key, "")

    # Detect language and description
    user_origninal_description = user.get(description_key, "")
    user_origninal_lang = user.get(lang_key, None)

    if user_origninal_lang == None or (not (user_origninal_lang in LANGS)):

        # Detect language of description and translate to English
        if user_origninal_description != '' and use_translator_if_necessary:
            user_english_description, user_detected_lang, _, _ = detect_and_translate_language(user_origninal_description, dest="en")

            if type(user_english_description) == list:
                user_english_description = user_english_description[0]

            if type(user_detected_lang) == list:
                user_detected_lang = user_detected_lang[0]
            

            if not (user_detected_lang in LANGS):
                new_user["lang"] = "en"
                new_user["description"] = user_english_description
            else:
                new_user["lang"] = user_detected_lang
                new_user["description"] = user_origninal_description
        else:
            new_user["lang"] = UNKNOWN_LANG
            new_user["description"] = user_origninal_description

    else:
        new_user["lang"] = user_origninal_lang
        new_user["description"] = user_origninal_description

    return new_user
