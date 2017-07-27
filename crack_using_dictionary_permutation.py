#!/usr/bin/env python3

from itertools import product
from functools import reduce
import vigenere
import crack5
import utils
import operator


CIPHER_TEXT = 'Ccoheal ieu w qwu tcb'
DICTIONARY_FILE = 'dictionary.txt'
KEY_LENGHTS = {15}
LOG_PERIOD = 10000


@utils.log_nth_call(LOG_PERIOD)
def check_key(key, decrypted):
    shortest_key = vigenere.find_shortest_key(key, decrypted)
    if not len(shortest_key) in KEY_LENGHTS:
        return
    return crack5.check_online(shortest_key)


def _print_winner(key, phrase):
    print("Key found!\nKey:{}\nPhrase:{}".format(key, phrase))


def check_all_keys_for_words(encrypted, words):
    all_possible_phrases = product(*words)
    for phrase in all_possible_phrases:
        decrypted = ''.join(phrase)
        key = vigenere.find_shortest_key(encrypted, decrypted)
        if check_key(key, decrypted):
            _print_winner(key, ' '.join(phrase))
            break


def select_by_len(length, words):
    return [w for w in words if len(w) == length]


def sequence_of_possible_words(dictionary, word_lenghts):
    return [select_by_len(lenght, dictionary.words) for lenght in word_lenghts]


def _print_combinations(comb):
    multi = '*'.join(str(c) for c in comb)
    combinations = reduce(operator.mul, comb, 1)
    print('Possible combinations: {}={}'.format(multi, str(combinations)))


if __name__ == "__main__":
    print("Starting '{}' deciphering".format(CIPHER_TEXT))
    encrypted = CIPHER_TEXT.lower().replace(' ', '')
    word_lenghts = list(map(len, CIPHER_TEXT.lower().split()))
    dictionary = crack5.Dictionary(DICTIONARY_FILE, set(word_lenghts))
    all_possible_words = sequence_of_possible_words(dictionary, word_lenghts)
    _print_combinations([len(s) for s in all_possible_words])
    check_all_keys_for_words(encrypted, all_possible_words)
    print("All done")
