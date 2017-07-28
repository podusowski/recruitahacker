#!/usr/bin/env python3

from itertools import product
from functools import reduce
import vigenere
import crack5
import utils
import operator
from dictionary import PrincetonDictionary


CIPHER_TEXT = 'Ccoheal ieu w qwu tcb'
CIPHER_TEXT_LEN = len(CIPHER_TEXT.replace(' ', ''))

print(CIPHER_TEXT_LEN)

DICTIONARY_FILE = 'scrabble-dictionary.txt'
LOG_PERIOD = 10000


def sequence_of_possible_words(dictionary, word_lenghts):
    def select_by_len(length):
        return [w for w in dictionary.words if len(w) == length]
    return list(map(select_by_len, word_lenghts))


def print_combinations(comb):
    multi = '*'.join(str(c) for c in comb)
    combinations = reduce(operator.mul, comb, 1)
    print('Possible combinations: {}={}'.format(multi, str(combinations)))


@utils.log_nth_call(LOG_PERIOD)
def check_key(key, decrypted):
    return crack5.check_online(key)


def possible_words(cipherText, dictFile):
    word_lenghts = list(map(len, cipherText.lower().split()))
    dictionary = crack5.Dictionary(dictFile, set(word_lenghts))
    all_possible_words = sequence_of_possible_words(dictionary, word_lenghts)
    print_combinations([len(s) for s in all_possible_words])
    return all_possible_words


princeton_dictionary = PrincetonDictionary()


def check_all_keys_for_words(encrypted, words):
    def print_winner(key, phrase):
        print("Key found!\nKey:{}\nPhrase:{}".format(key, phrase))

    all_possible_phrases = product(*words)
    all_possible_phrases = filter(princeton_dictionary.words_make_sense_as_whole, all_possible_phrases)

    for phrase in all_possible_phrases:
        #print(phrase)
        decrypted = ''.join(phrase)
        key = vigenere.find_shortest_key(encrypted, decrypted)
        if check_key(key, decrypted):
            print_winner(key, ' '.join(phrase))
            break


if __name__ == "__main__":
    print("Starting '{}' deciphering".format(CIPHER_TEXT))
    encrypted = CIPHER_TEXT.lower().replace(' ', '')
    all_possible_words = possible_words(CIPHER_TEXT, DICTIONARY_FILE)

    check_all_keys_for_words(encrypted, all_possible_words)
    print("All done")
