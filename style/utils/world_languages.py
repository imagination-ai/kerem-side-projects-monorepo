import json
from os import mkdir, path
from typing import List, Set

from style.constants import WORLD_LANG_FILENAME, WORLD_LANG_PATH

LANG_RAW: str = (
    "Romani Romanian Russian Rwanda Samoan Sanskrit Serbian Shona Sindhi Sinhala Slovak Slovene Somali "
    "Spanish Swahili Swedish Tachelhit Tagalog Tajiki Tamil Tatar Telugu Thai Tibetic Languages Tigrigna "
    "Tok Pisin Turkish Turkmen Ukrainian Urdu Uyghur Uzbek Vietnamese Warlpiri Welsh Wolof Xhosa Yakut "
    "Yiddish Yoruba Yucatec Zapotec Zulu Afrikaans Albanian Amharic Arabic (Egyptian Spoken) Arabic ("
    "Levantine) Arabic (Modern Standard) Arabic (Moroccan Spoken) Arabic (Overview) Aramaic Armenian "
    "Assamese Aymara Azerbaijani Balochi Bamanankan Bashkort (Bashkir) Basque Belarusan Bengali Bhojpuri "
    "Bislama Bosnian Brahui Bulgarian Burmese Cantonese Catalan Cebuano Chechen Cherokee Croatian Czech "
    "Dakota Danish Dari Dholuo Dutch English Esperanto Estonian Éwé Finnish French Georgian German Gikuyu "
    "Greek Guarani Gujarati Haitian Creole Hausa Hawaiian Hawaiian Creole Hebrew Hiligaynon Hindi "
    "Hungarian Icelandic Igbo Ilocano Indonesian (Bahasa Indonesia) Inuit/Inupiaq Irish Gaelic Italian "
    "Japanese Jarai Javanese K’iche’ Kabyle Kannada Kashmiri Kazakh Khmer Khoekhoe Korean Kurdish Kyrgyz "
    "Lao Latin Latvian Lingala Lithuanian Macedonian Maithili Malagasy Malay (Bahasa Melayu) Malayalam "
    "Mandarin (Chinese) Marathi Mende Mongolian Nahuatl Navajo Nepali Norwegian Ojibwa Oriya Oromo Pashto "
    "Persian Polish Portuguese Punjabi Quechua "
)


def proper_lang_list(
    languages: str = LANG_RAW,
    missing_languages=("Chinese"),
    unnecessary_languages=("English"),
    sep=" ",
) -> List:
    """
        Takes a string that contains several names of languages,
    convert the string to a list (use one space as separator in default)
    adds/removes desirable and undesirable languages to the list
    clean the explanations and dialects by removing the elements that contain bracket characters
    returns a list
        Args:
            languages (str): The first argument. Defaults to LANG_RAW.
            missing_languages (tuple): The second argument. Defaults to ("Chinese").
            unnecessary_languages (tuple): The third argument. Defaults to ("English").
            sep: The fourth argument. By default one blank space.

        Returns:
            list: Returns a list that contains some of the names of world languages.

    """

    lang = languages.strip().split(sep)
    lang.extend(missing_languages)
    lang = [e for e in lang if e not in unnecessary_languages]
    lang = [
        lang_name
        for lang_name in lang
        if "(" not in lang_name and ")" not in lang_name
    ]
    return lang


def separate_and_add_alternative_lang_names(
    languages: List, sep: str = "/"
) -> Set:
    """
    Takes a language list then separate language name that contains two alternatives
        by searching elements have two names (in default names is separated by '/')
       returns a set obj
    Args:
        languages (list): The first argument. It takes the language names list that created proper_lang_list_function.
        sep: The second argument. Defaults to '/' character.

    Returns:
        set: Returns a set obj after cleaning two name elements.
    """

    lang_set = set(languages)
    removable_items = []
    for lang_name in lang_set:
        if "/" in lang_name:
            removable_items.append((lang_name, lang_name.split(sep)))

    for element_to_remove, elements_to_add in removable_items:
        lang_set.remove(element_to_remove)
        lang_set.update(elements_to_add)

    return lang_set


def save_languages_to_json(
    languages: Set,
    output_directory: str = WORLD_LANG_PATH,
    filename: str = WORLD_LANG_FILENAME,
):
    """
    Save a set file and write it as json file write the file in the resource folder under the project file.
      If there is no such directory, the function creates the directory by itself.
      Returns None.
      Args:
          filename: filename (e.g., "world-lang.json")
          languages (set): The first argument.
          output_directory (str):  The second argument. Default to WORLD_LANG_PATH variable.

      Returns:
          None.
    """

    if not path.isdir(output_directory):
        mkdir(output_directory)
    json_str = json.dumps(list(languages))
    with open(f"{output_directory} / {filename}", "w") as f:
        f.write(json_str)


def get_languages(filename: str = WORLD_LANG_FILENAME) -> Set:
    """
    It takes name of the world languages file as an argument returns a set of world languages as set obj.

    Args:
        filename (str): The first argument. The default to file_name variable.

    Returns:
        set: Ultimate set that contains world languages.

    """

    if not path.isfile(filename):
        lang = proper_lang_list()
        lang_clean = separate_and_add_alternative_lang_names(lang)
        save_languages_to_json(lang_clean)

    with open(filename, "r") as f:
        json_obj = json.load(f)

    return set(json_obj)
