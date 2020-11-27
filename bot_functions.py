import os
import string
import discord
import random
from fuzzywuzzy import process

import bot_words_storage as st
import image_parser as parser


def word_lists_counter() -> int:
    """Function to get number of word lists from file 'bot_words_storage.py'."""
    lists_counter = 0
    storage_path = os.path.join(os.path.dirname(__file__), 'bot_words_storage.py')

    if os.path.exists(storage_path):
        with open('bot_words_storage.py') as file:
            raw_data = file.read().split(' ')
    else:
        exit(-1)

    for word in raw_data:
        if word.endswith('list'):
            lists_counter += 1

    return lists_counter


def discord_message_analysis(message: discord.MessageType) -> str:
    """Function to for processing words to get they meaning."""
    word_lists_number = word_lists_counter()
    referring_to_word_lists = [st.hello_words_list, st.bad_words_list, st.help_words_list]
    callback_from_word_lists = ['hello', 'bad', 'help']
    result = None

    message_content = message.content.lower()
    table = str.maketrans(dict.fromkeys(string.punctuation))
    message_content_clean = message_content.translate(table)
    message_content_list = message_content_clean.split()

    for word in message_content_list:
        for iteration in range(word_lists_number):
            if result is None:
                found_word, rating = process.extractOne(word, referring_to_word_lists[iteration])
                result = callback_from_word_lists[iteration] if rating > 75 else None

    return result


def bad_word_finder(message: discord.MessageType) -> str:
    """Function to find bad word in sentence."""
    message_content = message.content.lower()
    table = str.maketrans(dict.fromkeys(string.punctuation))
    message_content_clean = message_content.translate(table)
    message_content_list = message_content_clean.split()
    result = None

    for word in message_content_list:
        found_word, rating = process.extractOne(word, st.bad_words_list)
        if result is None:
            result = found_word if rating > 75 else None

    return result


def image_selection():
    """Function to randomize image choice."""
    start_of_link = 'http://babenki.info/'
    image_links_list = parser.get_images()
    image_count = len(image_links_list)
    choice = random.randint(0, image_count)

    link = start_of_link + image_links_list[choice]

    return link
